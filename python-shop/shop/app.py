from __future__ import annotations

import os
from typing import Any

from flask import Flask, flash, redirect, render_template, request, session, url_for

from .catalog import (
    Product,
    get_all_products,
    get_categories,
    get_featured_products,
    get_product_by_slug,
    search_products,
)
from .storage import create_order, get_order, get_order_items, init_db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SHOP_SECRET_KEY", "development-secret-key")
    app.config["SHIPPING_CENTS"] = 1800
    init_db()

    @app.context_processor
    def inject_globals() -> dict[str, Any]:
        cart = _build_cart()
        return {
            "categories": get_categories(),
            "cart_count": cart["item_count"],
            "cart_total_cents": cart["grand_total_cents"],
        }

    @app.template_filter("currency")
    def currency_filter(value: int) -> str:
        return f"${value / 100:,.2f}"

    @app.get("/")
    def home() -> str:
        query = request.args.get("q", "")
        category = request.args.get("category", "")
        products = search_products(query=query, category=category)
        return render_template(
            "home.html",
            products=products,
            featured_products=get_featured_products(),
            query=query,
            active_category=category,
            category_count=len(get_categories()),
            product_count=len(get_all_products()),
        )

    @app.get("/product/<slug>")
    def product_detail(slug: str) -> str:
        product = get_product_by_slug(slug)
        if product is None:
            return render_template("not_found.html"), 404
        related = [
            candidate
            for candidate in get_all_products()
            if candidate.category == product.category and candidate.slug != product.slug
        ][:3]
        return render_template("product_detail.html", product=product, related_products=related)

    @app.post("/cart/add/<slug>")
    def add_to_cart(slug: str):
        product = get_product_by_slug(slug)
        if product is None:
            flash("未找到该商品。", "error")
            return redirect(url_for("home"))

        quantity = max(1, _parse_quantity(request.form.get("quantity", "1")))
        cart = _get_cart_session()
        cart[slug] = cart.get(slug, 0) + quantity
        session["cart"] = cart
        flash(f"已将 {product.name} 加入购物车。", "success")
        return redirect(request.referrer or url_for("cart"))

    @app.get("/cart")
    def cart() -> str:
        cart_data = _build_cart()
        return render_template("cart.html", cart=cart_data)

    @app.post("/cart/update")
    def update_cart():
        cart = _get_cart_session()
        for slug, value in request.form.items():
            if not slug.startswith("quantity_"):
                continue
            product_slug = slug.removeprefix("quantity_")
            quantity = _parse_quantity(value)
            if quantity <= 0:
                cart.pop(product_slug, None)
            else:
                cart[product_slug] = quantity

        session["cart"] = cart
        flash("购物车已更新。", "success")
        return redirect(url_for("cart"))

    @app.post("/cart/remove/<slug>")
    def remove_from_cart(slug: str):
        cart = _get_cart_session()
        cart.pop(slug, None)
        session["cart"] = cart
        flash("商品已移除。", "success")
        return redirect(url_for("cart"))

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        cart_data = _build_cart()
        if cart_data["item_count"] == 0:
            flash("请先选择商品后再结账。", "error")
            return redirect(url_for("home"))

        errors: dict[str, str] = {}
        form_data = {
            "customer_name": "",
            "email": "",
            "address": "",
            "city": "",
            "note": "",
        }

        if request.method == "POST":
            form_data = {
                "customer_name": request.form.get("customer_name", "").strip(),
                "email": request.form.get("email", "").strip(),
                "address": request.form.get("address", "").strip(),
                "city": request.form.get("city", "").strip(),
                "note": request.form.get("note", "").strip(),
            }
            errors = _validate_checkout_form(form_data)
            if not errors:
                order_id = create_order(
                    customer_name=form_data["customer_name"],
                    email=form_data["email"],
                    address=form_data["address"],
                    city=form_data["city"],
                    note=form_data["note"],
                    subtotal_cents=cart_data["subtotal_cents"],
                    shipping_cents=cart_data["shipping_cents"],
                    total_cents=cart_data["grand_total_cents"],
                    items=cart_data["line_items"],
                )
                session["cart"] = {}
                flash("订单创建成功，我们已经为你保留库存。", "success")
                return redirect(url_for("order_success", order_id=order_id))

        return render_template("checkout.html", cart=cart_data, errors=errors, form_data=form_data)

    @app.get("/order/<int:order_id>/success")
    def order_success(order_id: int) -> str:
        order = get_order(order_id)
        if order is None:
            return render_template("not_found.html"), 404
        items = get_order_items(order_id)
        return render_template("order_success.html", order=order, items=items)

    return app


def _get_cart_session() -> dict[str, int]:
    raw = session.get("cart", {})
    return {slug: int(quantity) for slug, quantity in raw.items()}


def _parse_quantity(raw_value: str) -> int:
    try:
        return max(0, int(raw_value))
    except (TypeError, ValueError):
        return 1


def _build_cart() -> dict[str, Any]:
    line_items: list[dict[str, Any]] = []
    subtotal_cents = 0
    item_count = 0

    for slug, quantity in _get_cart_session().items():
        product = get_product_by_slug(slug)
        if product is None:
            continue

        line_total_cents = product.price_cents * quantity
        subtotal_cents += line_total_cents
        item_count += quantity
        line_items.append(
            {
                "product_slug": product.slug,
                "product_name": product.name,
                "product": product,
                "quantity": quantity,
                "unit_price_cents": product.price_cents,
                "line_total_cents": line_total_cents,
            }
        )

    shipping_cents = 0 if subtotal_cents >= 35000 or subtotal_cents == 0 else 1800
    grand_total_cents = subtotal_cents + shipping_cents

    return {
        "line_items": line_items,
        "item_count": item_count,
        "subtotal_cents": subtotal_cents,
        "shipping_cents": shipping_cents,
        "grand_total_cents": grand_total_cents,
        "free_shipping_gap_cents": max(0, 35000 - subtotal_cents),
    }


def _validate_checkout_form(form_data: dict[str, str]) -> dict[str, str]:
    errors: dict[str, str] = {}
    if len(form_data["customer_name"]) < 2:
        errors["customer_name"] = "请输入有效姓名。"
    if "@" not in form_data["email"] or "." not in form_data["email"]:
        errors["email"] = "请输入有效邮箱。"
    if len(form_data["address"]) < 8:
        errors["address"] = "请输入完整收货地址。"
    if len(form_data["city"]) < 2:
        errors["city"] = "请输入城市名称。"
    if len(form_data["note"]) > 240:
        errors["note"] = "备注请控制在 240 个字符内。"
    return errors
