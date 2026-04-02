from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from shop import create_app


class ShopAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test-shop.db"
        os.environ["SHOP_DB_PATH"] = str(self.db_path)
        os.environ["SHOP_SECRET_KEY"] = "test-secret"

        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        os.environ.pop("SHOP_DB_PATH", None)
        os.environ.pop("SHOP_SECRET_KEY", None)
        self.temp_dir.cleanup()

    def test_home_page_loads(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Northstar Atelier", response.get_data(as_text=True))

    def test_add_to_cart_and_view_cart(self) -> None:
        self.client.post("/cart/add/aurora-desk-lamp", data={"quantity": "2"})
        response = self.client.get("/cart")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Aurora Desk Lamp", page)
        self.assertIn("$378.00", page)

    def test_checkout_creates_order(self) -> None:
        self.client.post("/cart/add/ember-throw", data={"quantity": "1"})
        response = self.client.post(
            "/checkout",
            data={
                "customer_name": "Lin Chen",
                "email": "lin@example.com",
                "address": "88 Riverside Avenue",
                "city": "Shanghai",
                "note": "Please call on arrival",
            },
            follow_redirects=True,
        )
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("订单 #", page)
        self.assertIn("Lin Chen", page)
        self.assertIn("Ember Throw", page)


if __name__ == "__main__":
    unittest.main()
