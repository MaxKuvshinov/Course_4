import json
import os
from typing import List


class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена введена некорректная.")
        elif value < self._price:
            user_confirm = input(f"Цена снижается с {self._price} до {value}. Вы уверены? (y/n): ").strip().lower()
            if user_confirm == "y":
                self._price = value
                print(f"Цена успешно снижена до {value}")
            else:
                print("Действие отменено")
        else:
            self._price = value

    @price.deleter
    def price(self) -> None:
        self._price = None

    @classmethod
    def creates_product(cls, name: str, description: str, price: float, quantity: int) -> "Product":
        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self._price} руб. Остаток {self.quantity} шт."

    def __add__(self, other: object) -> float:
        if isinstance(other, Product):
            return self._price * self.quantity + other._price * other.quantity
        raise TypeError(f"Невозможно сложить объект типа 'Product' с объектом типа '{type(other).__name__}'")


class Category:
    """Класс, представляющий категорию продуктов."""

    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.__products: List[Product] = []
        Category.total_categories += 1

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.total_unique_products += 1

    @property
    def products(self) -> List[str]:
        return [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products]

    def get_product(self) -> List[Product]:
        return self.__products

    @classmethod
    def get_total_categories(cls) -> int:
        return cls.total_categories

    @classmethod
    def get_total_unique_products(cls) -> int:
        return cls.total_unique_products

    def __len__(self) -> int:
        return sum(product.quantity for product in self.__products)

    def __str__(self) -> str:
        total_products = len(self)
        return f"{self.name}, количество продуктов: {total_products} шт."


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
#
#     for category in categories:
#         print(f"Категория: {category.name}")
#         print(f"Описание: {category.description}")
#         print(f"Строковое представление категории: {category}")
#         print(f"Количество продуктов в категории: {len(category)}")
#         for product_info in category.products:
#             print(f"Строковое представление продукта: {product_info}")
#         print()
#
#     if len(categories[0].get_product()) > 1:
#         product1 = categories[0].get_product()[0]
#         product2 = categories[0].get_product()[1]
#         print(f"Сумма цен продуктов (учитывая количество на складе): {product1 + product2}")
#     else:
#         print("Не хватает продуктов для сложения.")
#
#     smartphone = categories[0].get_product()[0]
#     print(f"Текущая цена смартфона: {smartphone.price}")
#     smartphone.price = 14000
#     print(f"Обновленная цена смартфона: {smartphone.price}")
