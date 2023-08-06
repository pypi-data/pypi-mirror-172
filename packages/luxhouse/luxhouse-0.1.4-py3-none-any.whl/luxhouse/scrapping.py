import requests
from bs4 import BeautifulSoup
from luxhouse.database import SQLite

from luxhouse.model import House, Location


def load_page(url: str) -> BeautifulSoup:
    print('loading: ' + url)
    r = requests.get(url)
    print(r.status_code)
    return BeautifulSoup(r.content, 'html5lib')


def get_next_page(page: BeautifulSoup) -> BeautifulSoup:
    next = page.find_all('a', attrs={'class', 'in-pagination__item'})
    for candidate in next:
        label = candidate.find('span', attrs={'class', 'in-pagination__controlText'})
        if label and label.getText() == 'Suivant':
            return load_page(candidate['href'])
    
    return None


def to_int(text:str)-> int:
    return int(''.join([i for i in text if i.isdecimal()]))


def extract_locality(title: str) -> tuple[str,str]:
    elements = title.split(',')
    return elements[-2].strip(), elements[-1].strip()


def process_house(result: BeautifulSoup) -> House:
    header = result.find('a', attrs={'class': 'in-card__title'})
    city, province = extract_locality(header['title'])

    location = Location(city, province)
    reference = header['href']
    title = header['title']
    current_price = to_int(result.find('li', attrs={'class':'in-realEstateListCard__features--main'}).getText())
    rooms = to_int(result.find('li', attrs={'aria-label': 'chambres/pièces'}).getText())
    size = to_int(result.find('li', attrs={'aria-label': 'superficie'}).getText())
    description = result.find('p', attrs={'class': 'in-realEstateListCard__description'}).getText()

    return House(reference, title, current_price, rooms, size, location, description)

def result_reader(url: str):
    page = load_page(url)

    while page:
        results = page.find('ul', attrs={'data-cy': 'result-list'})
        for result in results.find_all('div', attrs={'class': 'in-realEstateListCard__content'}):
            yield result
        page = get_next_page(page)


def immotop(database_path:str):
    URL = "https://www.immotop.lu/vente-maisons/luxembourg-pays/?criterio=dataModifica&ordine=desc&noAste=1"

    database = SQLite(database_path)

    for result in result_reader(URL):
        try:
            house = process_house(result)
            database.add_house(house)
        except:
            print('Invalid Format')
