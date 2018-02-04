
import requests
from bs4 import BeautifulSoup


def create_soup(url):
    # print(url)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def find_prof(soup, prof: list) -> str:
    all_lines = soup.find_all("a", href=True)
    for line in all_lines:
        if (line['href'].startswith('/ShowRatings.jsp?tid=')):
            possible_prof = set(line.find('span', {'class': 'main'}).text.strip().split(', '))
            if set(prof) <= possible_prof:
                return 'http://www.ratemyprofessors.com' + line['href']
            elif prof[-1] in possible_prof:
                return 'http://www.ratemyprofessors.com' + line['href']


def get_ratings(soup):
    result = dict()
    for x in ("quality", "difficulty", "takeAgain"):
        line = soup.find('div', {"class": x})
        temp = line.find(class_="grade")
        if temp is not None:
            result[x] = (temp.text.strip())
    return result


def run(prof: str):
    prof = prof.split()
    url = 'http://www.ratemyprofessors.com/search.jsp?query='
    url += 'UCI+' + prof[-1]

    soup = create_soup(url)
    prof_page = find_prof(soup, prof)

    if(prof_page != None):
        prof_soup = create_soup(prof_page)
        return get_ratings(prof_soup)


if __name__ == '__main__':
    url = 'http://www.ratemyprofessors.com/search.jsp?query='

    url += 'UCI+Pattis'

    soup = create_soup(url)
    prof_page = find_prof(soup, {'Pattis'})
    prof_soup = create_soup(prof_page)
    ratings = get_ratings(prof_soup)