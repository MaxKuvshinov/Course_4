import json
import os
from abc import ABC, abstractmethod
from typing import List


class MixinInfo:
    """Миксин для логирования создания объекта"""

    def __init__(self):
        print(self.__repr__())

    def __repr__(self) -> str:
        """Возвращает строку с названием класса и атрибутами"""
        attributes = ", ".join(repr(value) for value in self.__dict__.values())
        return f"{self.__class__.__name__}({attributes})"


class AbstractClass(MixinInfo, ABC):
    """Абстрактный класс"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity
        super().__init__()

    @abstractmethod
    def __str__(self) -> str:
        pass


class Product(AbstractClass):
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description, price, quantity)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена введена некорректная.")
        elif hasattr(self, "_price") and value < self._price:
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
        if not isinstance(other, Product):
            raise TypeError(
                f"Невозможно сложить объект типа '{type(self).__name__}' с объектом типа '{type(other).__name__}'"
            )
        if type(self) is not type(other):
            raise TypeError(
                f"Невозможно сложить объекты разных типов: '{type(self).__name__}' и '{type(other).__name__}'"
            )
        return self.price * self.quantity + other.price * other.quantity


class Category(MixinInfo):
    """Класс, представляющий категорию продуктов."""

    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.__products: List[Product] = []
        super().__init__()
        Category.total_categories += 1

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Объект не относится к классу 'Product' и его наследникам")
        if not issubclass(type(product), Product):
            raise TypeError("Объект не относится к классу 'Product' и его наследникам")

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


class Smartphone(Product):
    """Класс, предоставляющий смартфон"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        performance: str,
        model: str,
        memory_size: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.performance = performance
        self.model = model
        self.memory_size = memory_size
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name} (Модель: {self.model}, Память: {self.memory_size}, Цвет: {self.color}), "
            f"Цена: {self.price} руб. Остаток: {self.quantity}"
        )


class LawnGrass(Product):
    """Класс, представляющий газонную траву"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country_of_origin: str,
        germination_period: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country_of_origin = country_of_origin
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name} (Страна-производитель: {self.country_of_origin}, "
            f"Срок прорастания: {self.germination_period} дней, Цвет: {self.color}), Цена: {self.price} руб. "
            f"Остаток: {self.quantity}"
        )


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


if __name__ == "__main__":
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../products.json"))
    categories = load_json_file(file_path)

    for category in categories:
        print(f"Категория: {category.name}")
        print(f"Описание: {category.description}")
        print(f"Строковое представление категории: {category}")
        print(f"Количество продуктов в категории: {len(category)}")
        for product_info in category.products:
            print(f"Строковое представление продукта: {product_info}")
        print()

    if len(categories[0].get_product()) > 1:
        product1 = categories[0].get_product()[0]
        product2 = categories[0].get_product()[1]
        print(f"Сумма цен продуктов (учитывая количество на складе): {product1 + product2}")
    else:
        print("Не хватает продуктов для сложения.")

    smartphone = categories[0].get_product()[0]
    print(f"Текущая цена смартфона: {smartphone.price}")
    smartphone.price = 14000
    print(f"Обновленная цена смартфона: {smartphone.price}")


smartphone = Smartphone(
    "Samsung Galaxy C23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, "Высокая", "С23 Ultra", 256, "Black"
)

lawn_grass = LawnGrass("Трава газонная", "Описание травы", 5000.0, 10, "Россия", 10, "Зеленый")

print("Smartphone:")
print(smartphone)

print("LawnGrass:")
print(lawn_grass)
