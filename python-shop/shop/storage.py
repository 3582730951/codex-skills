from __future__ import annotations

import sqlite3
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "shop.db"


def get_db_path() -> Path:
    configured = os.environ.get("SHOP_DB_PATH")
    return Path(configured) if configured else DEFAULT_DB_PATH


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                note TEXT NOT NULL,
                subtotal_cents INTEGER NOT NULL,
                shipping_cents INTEGER NOT NULL,
                total_cents INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_slug TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price_cents INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
            """
        )


def create_order(
    *,
    customer_name: str,
    email: str,
    address: str,
    city: str,
    note: str,
    subtotal_cents: int,
    shipping_cents: int,
    total_cents: int,
    items: list[dict[str, int | str]],
) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO orders (
                customer_name,
                email,
                address,
                city,
                note,
                subtotal_cents,
                shipping_cents,
                total_cents
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_name,
                email,
                address,
                city,
                note,
                subtotal_cents,
                shipping_cents,
                total_cents,
            ),
        )
        order_id = int(cursor.lastrowid)
        connection.executemany(
            """
            INSERT INTO order_items (
                order_id,
                product_slug,
                product_name,
                quantity,
                unit_price_cents
            ) VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    order_id,
                    item["product_slug"],
                    item["product_name"],
                    item["quantity"],
                    item["unit_price_cents"],
                )
                for item in items
            ],
        )
        return order_id


def get_order(order_id: int) -> sqlite3.Row | None:
    with get_connection() as connection:
        return connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()


def get_order_items(order_id: int) -> list[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id ASC",
            (order_id,),
        ).fetchall()
