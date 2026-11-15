import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import get_book_data, scrape_books

TEST_BOOK_URL = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'


def test_get_book_data_returns_dict_with_expected_keys():
    """Проверяет, что данные возвращаются в виде словаря с нужными ключами."""
    data = get_book_data(TEST_BOOK_URL)
    assert isinstance(data, dict)
    expected_keys = {'title', 'price', 'rating', 'availability', 
                     'description', 'product_information'}
    assert expected_keys.issubset(data.keys())


def test_get_book_data_title_is_correct():
    """Проверяет корректность значения поля title."""
    data = get_book_data(TEST_BOOK_URL)
    assert data['title'] == 'A Light in the Attic'


def test_scrape_books_returns_non_empty_list():
    """Проверяет, что функция сбора возвращает непустой список книг."""
    books = scrape_books(is_save=False)
    assert isinstance(books, list)
    assert len(books) > 0