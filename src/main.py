import json
import os
from typing import List


class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс, представляющий категорию продуктов."""

    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.products = []
        Category.total_categories += 1

    def add_product(self, product: Product) -> None:
        self.products.append(product)
        Category.total_unique_products += 1

    @classmethod
    def get_total_categories(cls) -> int:
        return cls.total_categories

    @classmethod
    def get_total_unique_products(cls) -> int:
        return cls.total_unique_products


def load_json_file(file_path: str) -> List[Category]:
    """Функция считывающая данные с JSON-файла и создает объекты Category и Product"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        category = Category(name=category_data["name"], description=category_data["description"])

        for product_data in category_data["products"]:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=float(product_data["price"]),
                quantity=int(product_data["quantity"]),
            )

            category.add_product(product)

        categories.append(category)

    return categories


# if __name__ == "__main__":
#     file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../products.json"))
#     categories = load_json_file(file_path)
#     for category in categories:
#         print(f"Категория: {category.name},\nОписание: {category.description}")
#         for product in category.products:
#             print(
#                 f"Название товара: {product.name},\nОписание: {product.description},\nЦена: {product.price},"
#                 f"\nКоличество: {product.quantity}"
#             )
#
#     print(f"Всего категорий: {Category.get_total_categories()}")
#     print(f"Количество уникальных категорий: {Category.get_total_unique_products()}")
