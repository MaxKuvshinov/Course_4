import json
from unittest.mock import patch

import pytest
from src.main import Category, Product, load_json_file


@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.total_categories = 0
    Category.total_unique_products = 0


@pytest.fixture()
def sample_product():
    return Product(name="Iphone 15", description="512GB, Gray space", price=210000.0, quantity=8)


@pytest.fixture()
def sample_product2():
    return Product(
        name="Samsung Galaxy C23 Ultra", description="256GB, Серый цвет, 200MP камера", price=180000.0, quantity=5
    )


@pytest.fixture()
def sample_category():
    return Category(name="Смартфоны", description="Смартфоны, как средство не только коммуникации")


def test_product_initialization(sample_product):
    assert sample_product.name == "Iphone 15"
    assert sample_product.description == "512GB, Gray space"
    assert sample_product.price == 210000.0
    assert sample_product.quantity == 8


def test_category_initialization(sample_category):
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == "Смартфоны, как средство не только коммуникации"
    assert len(sample_category.products) == 0


def test_add_product(sample_category, sample_product):
    initial_product_count = Category.get_total_unique_products()
    sample_category.add_product(sample_product)
    assert len(sample_category.products) == 1
    assert Category.total_unique_products == initial_product_count + 1


def test_total_categories():
    initial_category_count = Category.get_total_categories()
    new_category = Category(name="Телевизоры", description="Современный телевизор")
    assert Category.total_categories == initial_category_count + 1


@pytest.fixture()
def sample_data(tmp_path):
    test_json = [
        {
            "name": "Смартфоны",
            "description": "Смартфоны, как средство не только коммуникации, "
            "но и получение дополнительных функций для удобства жизни",
            "products": [
                {
                    "name": "Samsung Galaxy C23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5,
                },
                {"name": "Iphone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
                {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14},
            ],
        },
        {
            "name": "Телевизоры",
            "description": "Современный телевизор, "
            "который позволяет наслаждаться просмотром, станет вашим другом и помощником",
            "products": [
                {"name": '55" QLED 4K', "description": "Фоновая подсветка", "price": 123000.0, "quantity": 7}
            ],
        },
    ]

    file_path = tmp_path / "test_products.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(test_json, file)

    return str(file_path)


def test_load_json_file(sample_data):
    categories = load_json_file(sample_data)
    assert len(categories) == 2

    assert isinstance(categories[0], Category)
    assert isinstance(categories[1], Category)

    assert categories[0].name == "Смартфоны"
    assert categories[1].name == "Телевизоры"

    assert len(categories[0].get_product()) == 3
    assert isinstance(categories[0].get_product()[0], Product)
    assert categories[0].get_product()[0].name == "Samsung Galaxy C23 Ultra"

    assert len(categories[1].get_product()) == 1
    assert isinstance(categories[1].get_product()[0], Product)
    assert categories[1].get_product()[0].name == '55" QLED 4K'


def test_total_counts_2(sample_data):
    load_json_file(sample_data)
    assert Category.get_total_categories() == 2
    assert Category.get_total_unique_products() == 4


@patch("builtins.input", side_effect=["y"])
def test_price_setter(input_mock, sample_product):
    sample_product.price = 200000
    assert sample_product.price == 200000.0

    input_mock.side_effect = ["n"]
    sample_product.price = 150000
    assert sample_product.price == 200000.0


def test_price_deleter(sample_product):
    assert sample_product.price == 210000.0

    del sample_product.price

    assert sample_product._price is None
    assert sample_product.price is None


def test_product_str(sample_product):
    assert str(sample_product) == "Iphone 15, 210000.0 руб. Остаток 8 шт."


def test_category_str(sample_category, sample_product):
    sample_category.add_product(sample_product)
    assert str(sample_category) == "Смартфоны, количество продуктов: 8 шт."


def test_category_len(sample_category, sample_product):
    assert len(sample_category) == 0
    sample_category.add_product(sample_product)
    assert len(sample_category) == 8


def test_product_add(sample_product, sample_product2):
    assert (sample_product + sample_product2) == (
        sample_product.price * sample_product.quantity + sample_product2.price * sample_product2.quantity
    )


def test_average_price(sample_category, sample_product, sample_product2):
    sample_category.add_product(sample_product)
    sample_category.add_product(sample_product2)
    expected_average_price = (
        sample_product.price * sample_product.quantity + sample_product2.price * sample_product2.quantity
    ) / (sample_product.quantity + sample_product2.quantity)
    assert sample_category.average_price() == expected_average_price
