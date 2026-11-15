import requests
import time
from bs4 import BeautifulSoup


def get_book_data(book_url: str) -> dict:
    """
    Собирает информацию об одной книге со страницы каталога books.toscrape.com.
    """
    response = requests.get(book_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else None

    price_tag = soup.find('p', class_='price_color')
    price = price_tag.get_text(strip=True) if price_tag else None

    rating_tag = soup.find('p', class_='star-rating')
    rating = None
    if rating_tag:
        for cls in rating_tag.get('class', []):
            if cls != 'star-rating':
                rating = cls
                break

    availability_tag = soup.find('p', class_='instock availability')
    availability = availability_tag.get_text(strip=True) if availability_tag else None

    desc_header = soup.find('div', id='product_description')
    description = None
    if desc_header:
        desc_p = desc_header.find_next_sibling('p')
        if desc_p:
            description = desc_p.get_text(strip=True)

    product_info = {}
    table = soup.find('table', class_='table-striped')
    if table:
        for row in table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')
            if th and td:
                product_info[th.get_text(strip=True)] = td.get_text(strip=True)

    return {
        'title': title,
        'price': price,
        'rating': rating,
        'availability': availability,
        'description': description,
        'product_information': product_info
    }


def scrape_books(is_save: bool = False) -> list:
    """
    Обходит все страницы каталога books.toscrape.com и собирает данные о книгах.
    """
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    all_books = []
    page = 1

    while True:
        url = base_url.format(page)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        book_links = soup.select('article.product_pod h3 a')

        if not book_links:
            break

        for link in book_links:
            relative_url = link['href']
            book_url = f'http://books.toscrape.com/catalogue/{relative_url}'
            try:
                book_data = get_book_data(book_url)
                all_books.append(book_data)
            except Exception:
                pass

        page += 1
        time.sleep(0.3)

    if is_save:
        with open('books_data.txt', 'w', encoding='utf-8') as f:
            for book in all_books:
                f.write(str(book) + '\n')

    return all_books