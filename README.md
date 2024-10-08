# E-commerce — электронная торговля, или электронная коммерция.

## Описание:
На данном этапе работы мы не будем реализовывать систему платежей, однако подготовим всё для того, чтобы у нас появилось ядро для интернет-магазина. В дальнейшем для этого ядра возможно будет реализовать любой интерфейс — от сайта до телеграм-бота.

## Обновление функционала:
- 10.07.2024 - добавление классы `Category` и `Product`. Так же реализованно тестирование для данных классов.
Добавлена функция `load_json_file`, которая считывает данные из JSON - файла
- 15.07.2024 - Изменили тип атрибута с продуктами на приватный. Добавлены геттер для класса `Category` для вывода товаров. Добавлен класс-метод для создания нового товара. Реализованы геттер, сеттер и делитер для цены товара.
- 19.07.2024 - Для классов `Category` и `Product` реализовали методы `__str__`, `__len__` и отдельно для класса `Product` реализован метод `__add__`
- 26.07.2024 - Добавлены два дочерних класса `Smartphone` и `LawnGrass` которые наследуют объекты и методы от родительского класса `Product`. Доработан функционал сложения таким образом, что можно складывать товары только из одинаковых классов продуктов. Доработан метод добавления продукта в категорию таким образом, чтобы не было возможности добавить вместо продукта или его наследников любой другой объект.
- 30.07.2024 - Оптимизирована работа с родительскими классами путем создания абстрактных классов и классов-наследников.
- 03.08.2024 - Добавлен функционал, который при добавлении товара с нулевым количеством вызывает исключение ValueError , которое будет сообщать пользователю, что товар с нулевым количеством не может быть добавлен. При этом прерывать выполнение программы. В классе «Категории» реализован метод, который подсчитывает средний ценник всех товаров. 

## Установка:
1. Клонируйте репозиторий
```
git@github.com:MaxKuvshinov/Course_4.git
```
2. Установите зависимости (Для установки зависимостей используется Poetry):
```
poetry install
```
3. Активируйте виртуальное окружение:
```
poetry shell
```
## Тестирование:
Для обеспечения качества и надежности фичи будут проведены различные тесты с использованием pytest.

## Установка зависимостей для тестирования:
Убедитесь, что вы находитесь в активированном виртуальном окружении Poetry. Затем установите зависимости для тестирования:
```
poetry add --group dev pytest
```
## Запуск тестов:
Для запуска тестов выполните следующую команду в корневом каталоге проекта: Убедитесь, что вы находитесь в активированном виртуальном окружении Poetry. Затем установите зависимости для тестирования:
```
pytest
```

## Лицензия:
Этот проект лицензирован по [лицензии MIT](https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F_MIT).