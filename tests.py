"""Module with unit tests"""
import unittest
import requests
unittest.TestLoader.sortTestMethodsUsing = None


class ApiTest(unittest.TestCase):
    """Class with Unit tests"""
    API_URL = 'http://127.0.0.1:5000/api'
    CATEGORY_URL = f'{API_URL}/category'
    CATEGORIES_URL = f'{API_URL}/categories'
    PRODUCT_URL = f'{API_URL}/product'
    PRODUCTS_URL = f'{API_URL}/products'
    SUM_URL = f'{CATEGORY_URL}/sum'
    SEARCH_URL = f'{API_URL}/search'
    CATEGORY_OBJ = {
        'title': 'category_test_title',
        'description': 'category_test_description'
    }
    PRODUCT_OBJ = {
        'title': 'product_test_title',
        'price': '100',
        'description': 'product_test_description',
        'sales_start': '2023-01-01',
        'amount': '3000',
        'category_id': '1'
    }

    def test_01_post_category(self):
        """POST request to /api/category; adds new item to database"""
        req = requests.post(ApiTest.CATEGORY_URL, params=ApiTest.CATEGORY_OBJ, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_02_post_product(self):
        """POST request to /api/product; adds new item to database"""
        req = requests.post(ApiTest.PRODUCT_URL, params=ApiTest.PRODUCT_OBJ, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_03_get_category(self):
        """GET request to /api/category; returns the details of certain category by id parameter"""
        req = requests.get(ApiTest.CATEGORY_URL, params={'id': 1}, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_04_put_category(self):
        """PUT request to /api/category with only 1 parameter (title) changes an item in database"""
        req = requests.put(ApiTest.CATEGORY_URL,
                           params={'id': 1, 'title': 'category_test_put'},
                           timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_05_put_category(self):
        """PUT request to /api/category with all possible parameters; changes an item in database"""
        req = requests.put(ApiTest.CATEGORY_URL,
                           params={'id': 1} | ApiTest.CATEGORY_OBJ,
                           timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_06_get_all_categories(self):
        """GET request to /api/categories; gets all categories from database"""
        req = requests.get(ApiTest.CATEGORIES_URL, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_07_get_product(self):
        """GET request to /api/product; returns the details of certain product by id parameter"""
        req = requests.get(ApiTest.PRODUCT_URL, params={'id': 1}, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_08_put_product(self):
        """PUT request to /api/product with only 1 parameter (title); changes an item in database"""
        req = requests.put(ApiTest.PRODUCT_URL,
                           params={'id': 1, 'title': 'product_test_put'},
                           timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_09_put_product(self):
        """PUT request to /api/product with all possible parameters; changes an item in database"""
        req = requests.put(ApiTest.PRODUCT_URL,
                           params={'id': 1} | ApiTest.PRODUCT_OBJ,
                           timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_10_get_all_products(self):
        """GET request to /api/products; gets all products from database"""
        req = requests.get(ApiTest.PRODUCTS_URL, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_11_category_sum(self):
        """GET request to /api/category/sum; returns the sum of all products in the certain category"""
        req = requests.get(ApiTest.SUM_URL, params={'id': 1}, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_12_search(self):
        """GET request to /api/search; returns products, available by certain date"""
        req = requests.get(ApiTest.SEARCH_URL, params={'date': '2023-03-16'}, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_13_delete_product(self):
        """DELETE request to /api/product; deletes item from database"""
        req = requests.delete(ApiTest.PRODUCT_URL, params={'id': 1}, timeout=5)
        self.assertEqual(req.status_code, 200)

    def test_14_delete_category(self):
        """DELETE request to /api/category; deletes item from database"""
        req = requests.delete(ApiTest.CATEGORY_URL, params={'id': 1}, timeout=5)
        self.assertEqual(req.status_code, 200)


if __name__ == '__main__':
    unittest.main()
