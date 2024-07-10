import pytest
import json
from src.main import Product, Category, load_json_file


@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.total_categories = 0
    Category.total_unique_products = 0


@pytest.fixture()
def sample_product():
    return Product(name="Iphone 15", description="512GB, Gray space", price=210000.0, quantity=8)


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
            "description": "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни",
            "products": [
                {
                    "name": "Samsung Galaxy C23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5
                },
                {
                    "name": "Iphone 15",
                    "description": "512GB, Gray space",
                    "price": 210000.0,
                    "quantity": 8
                },
                {
                    "name": "Xiaomi Redmi Note 11",
                    "description": "1024GB, Синий",
                    "price": 31000.0,
                    "quantity": 14
                }
            ]
        },
        {
            "name": "Телевизоры",
            "description": "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
            "products": [
                {
                    "name": "55\" QLED 4K",
                    "description": "Фоновая подсветка",
                    "price": 123000.0,
                    "quantity": 7
                }
            ]
        }
    ]

    file_path = tmp_path / "test_products.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(test_json, file)

    return str(file_path)


def test_load_json_file(sample_data):
    categories = load_json_file(sample_data)
    assert len(categories) == 2
    assert categories[0].name == "Смартфоны"
    assert categories[1].name == "Телевизоры"

    assert len(categories[0].products) == 3
    assert categories[0].products[0].name == "Samsung Galaxy C23 Ultra"

    assert len(categories[1].products) == 1
    assert categories[1].products[0].name == "55\" QLED 4K"


def test_total_counts_2(sample_data):
    load_json_file(sample_data)
    assert Category.get_total_categories() == 2
    assert Category.get_total_unique_products() == 4
