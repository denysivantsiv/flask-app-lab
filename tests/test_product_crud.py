import unittest
from app import app
from app.products.views import get_db

class ProductCRUDTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False # Вимикаємо CSRF для спрощення тестів
        self.client = app.test_client()

    def test_1_create_product(self):
        response = self.client.post("/products/add", data={
            "name": "Тестовий Ноутбук",
            "content": "Опис тестового ноутбука для перевірки TinyDB.",
            "price": "999.99",
            "category": "Computers",
            "quantity": "5"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий Ноутбук".encode('utf-8'), response.data)

    def test_2_read_product_detail(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)

    def test_3_update_product(self):
        response = self.client.post("/products/1/edit", data={
            "name": "Оновлений Ноутбук",
            "content": "Оновлений тестовий опис.",
            "price": "1050.00",
            "category": "Computers",
            "quantity": "3"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Оновлений Ноутбук".encode('utf-8'), response.data)

    def test_4_delete_product(self):
        response = self.client.post("/products/1/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Перевіряємо, що сторінка тепер повертає 404
        check_deleted = self.client.get("/products/1")
        self.assertEqual(check_deleted.status_code, 404)

if __name__ == "__main__":
    unittest.main()