from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    slug: str
    name: str
    category: str
    price_cents: int
    badge: str
    image: str
    subtitle: str
    description: str
    material: str
    dimensions: str
    palette: str
    featured: bool = False


PRODUCTS = [
    Product(
        slug="aurora-desk-lamp",
        name="Aurora Desk Lamp",
        category="Lighting",
        price_cents=18900,
        badge="Studio Pick",
        image="https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=1200&q=80",
        subtitle="A sculpted brass lamp for late-night focus.",
        description=(
            "Aurora balances a brushed brass arm with a warm smoked-glass shade. "
            "It was chosen for workspaces that need concentration without cold office aesthetics."
        ),
        material="Brass, smoked glass, linen cable",
        dimensions="W 28 cm x H 44 cm",
        palette="Honey brass / umber smoke",
        featured=True,
    ),
    Product(
        slug="moss-lounge-chair",
        name="Moss Lounge Chair",
        category="Seating",
        price_cents=42500,
        badge="New Arrival",
        image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
        subtitle="Soft geometry with a deep olive boucle finish.",
        description=(
            "Moss Lounge Chair is designed for reading corners, hotel lobbies, and homes "
            "that want one piece with enough presence to hold a room together."
        ),
        material="Oak frame, boucle upholstery, matte steel feet",
        dimensions="W 74 cm x D 78 cm x H 83 cm",
        palette="Olive / natural oak",
        featured=True,
    ),
    Product(
        slug="tidal-ceramic-vase",
        name="Tidal Ceramic Vase",
        category="Decor",
        price_cents=7600,
        badge="Limited Batch",
        image="https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=1200&q=80",
        subtitle="Hand-finished texture inspired by coastal stone.",
        description=(
            "Each Tidal vase carries slight variations in the glaze so floral arrangements "
            "and bare shelves both feel intentionally styled."
        ),
        material="Stoneware ceramic",
        dimensions="Dia 18 cm x H 31 cm",
        palette="Chalk / sea clay",
        featured=False,
    ),
    Product(
        slug="atlas-wall-shelf",
        name="Atlas Wall Shelf",
        category="Storage",
        price_cents=13200,
        badge="Best Seller",
        image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
        subtitle="Minimal steel shelving with gallery-like restraint.",
        description=(
            "Atlas is built for compact apartments and curated studios where every wall needs "
            "to contribute without looking overloaded."
        ),
        material="Powder-coated steel, walnut veneer",
        dimensions="W 90 cm x D 24 cm x H 26 cm",
        palette="Bone white / dark walnut",
        featured=False,
    ),
    Product(
        slug="ember-throw",
        name="Ember Throw",
        category="Textiles",
        price_cents=9800,
        badge="Editors' Choice",
        image="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
        subtitle="A heavyweight merino throw for colder rooms.",
        description=(
            "Woven with a rich rust tone and soft brushed finish, Ember brings warmth to neutral sofas "
            "and layered bedroom palettes."
        ),
        material="Merino wool",
        dimensions="130 cm x 180 cm",
        palette="Rust / clay",
        featured=True,
    ),
    Product(
        slug="harbor-side-table",
        name="Harbor Side Table",
        category="Tables",
        price_cents=15400,
        badge="Compact Favorite",
        image="https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?auto=format&fit=crop&w=1200&q=80",
        subtitle="Rounded oak joinery with a marble inlay top.",
        description=(
            "Harbor adds quiet luxury beside lounge chairs and beds without demanding much floor area."
        ),
        material="Solid oak, honed marble",
        dimensions="Dia 42 cm x H 50 cm",
        palette="Natural oak / cream stone",
        featured=False,
    ),
]


def get_all_products() -> list[Product]:
    return PRODUCTS


def get_featured_products() -> list[Product]:
    return [product for product in PRODUCTS if product.featured]


def get_categories() -> list[str]:
    return sorted({product.category for product in PRODUCTS})


def get_product_by_slug(slug: str) -> Product | None:
    return next((product for product in PRODUCTS if product.slug == slug), None)


def search_products(query: str = "", category: str = "") -> list[Product]:
    normalized_query = query.strip().lower()
    normalized_category = category.strip().lower()

    def matches(product: Product) -> bool:
        query_match = not normalized_query or any(
            normalized_query in field.lower()
            for field in (product.name, product.subtitle, product.description, product.category)
        )
        category_match = not normalized_category or product.category.lower() == normalized_category
        return query_match and category_match

    return [product for product in PRODUCTS if matches(product)]
