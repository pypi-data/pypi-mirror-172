import requests
from bs4 import BeautifulSoup, PageElement
from luxhouse.database import SQLite

from luxhouse.model import House, Location


def load_page(url: str) -> BeautifulSoup:
    print('loading: ' + url)
    r = requests.get(url)
    print(r.status_code)
    return BeautifulSoup(r.content, 'html5lib')


def get_next_page(page: BeautifulSoup) -> PageElement:
    next = page.find_all('a', attrs={'class', 'in-pagination__item'})
    for candidate in next:
        label = candidate.find('span', attrs={'class', 'in-pagination__controlText'})
        if label and label.getText() == 'Suivant':
            return load_page(candidate['href'])
    
    return None


def to_int(page_element:PageElement)-> int:
    text = to_text(page_element)

    if text is None:
        return None

    elements = text.split('-')
    
    if len(elements) == 2:
        text = elements[0]

    digits = [i for i in text if i.isdecimal()]

    if len(digits) == 0:
        return None

    return int(''.join(digits))

def to_text(page_element: PageElement) -> str:
    if page_element is None:
        return None

    return page_element.get_text()

def extract_locality(title: str) -> tuple[str,str]:
    elements = title.split(',')

    if len(elements) >= 3:
        return elements[-2].strip(), elements[-1].strip()

    if len(elements) == 2:
        return elements[-1].strip(), elements[-1].strip()

    elements = title.split('à')
    
    if len(elements) == 2:
        return elements[-1].strip(), elements[-1].strip()

    raise TypeError('Failed to parse title ' + title)


def process_house(result: PageElement) -> House:
    header = result.find('a', attrs={'class': 'in-card__title'})
    reference = header['href']

    locality, commune = extract_locality(header['title'])
    location = Location(locality, commune, 'Luxembourg')
    title = header['title']
    current_price = to_int(result.find('li', attrs={'class':'in-realEstateListCard__features--main'}))
    rooms = to_int(result.find('li', attrs={'aria-label': 'chambres/pièces'}))
    bathrooms = to_int(result.find('li', attrs={'aria-label': 'salles de bain'}))
    size = to_int(result.find('li', attrs={'aria-label': 'superficie'}))
    description = to_text(result.find('p', attrs={'class': 'in-realEstateListCard__description'}))
    return House(reference, title, current_price, rooms, bathrooms, size, location, description)
        
def result_reader(url: str):
    page = load_page(url)

    while page:
        results = page.find('ul', attrs={'data-cy': 'result-list'})
        for result in results.find_all('div', attrs={'class': 'in-realEstateListCard__content'}):
            yield result
        page = get_next_page(page)


def immotop(database_path:str) -> None:
    URL = "https://www.immotop.lu/vente-maisons/luxembourg-pays/?criterio=dataModifica&ordine=desc&noAste=1"

    database = SQLite(database_path)

    for result in result_reader(URL):
        house = process_house(result)
        database.add_house(house)

if __name__ == '__main__':
    immotop('results.sqlite3')