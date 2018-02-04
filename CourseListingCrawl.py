import requests
from collections import defaultdict
from bs4 import BeautifulSoup


def get_converted_table(soup):
    table = soup.find("tbody").find_all("tr")
    return table


def parse_class_name(name):
    name[1] = name[1].lstrip('0')
    parsed_name = ' '.join(name)
    return parsed_name


def get_classes(soup):
    table = get_converted_table(soup)

    classes = {}
    for row in table:
        class_names = row.findAll("td", class_="name")
        instructor_names = row.findAll("td", class_="instruction")
        instructor_dict = defaultdict(list)

        term = ["Fall", "Winter", "Spring"]
        for i, c in enumerate(instructor_names):
            if i == 3:
                break

            quart_instruct = []
            for x in c.findAll("a"):
                quart_instruct.append(x.get_text().strip())
            instructor_dict[term[i]] = quart_instruct

        name = class_names[0].get_text().replace('\n', '').split(' ')
        classes[parse_class_name(name)] = instructor_dict

    return classes


def parse_programs(soup):
    programs = {}
    for option in soup.findAll('select', attrs={'name': 'program'}):
        for program in option.findAll('option'):
            if(program.text not in programs):
                programs[program.text] = program['value']
    return programs


def get_quarter_classes(classes):
    quarter = input("Quarter: ").capitalize()

    for class_name, instructor in classes.items():
        print(class_name, instructor[quarter])


def create_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def get_user_input():
    year = "2017"  # input("Year: ")
    level = "Lower-Division"  # input("Level: ")
    department = "ALL"  # input("Department: ")
    program = input("Program: ").upper()
    return year, level, department, program


def create_classes(params):
    year, level, department, program = params
    program_soup = create_soup("http://www.ics.uci.edu/ugrad/courses/")
    programs = parse_programs(program_soup)

    url = "https://www.ics.uci.edu/ugrad/courses/listing.php?year={}&level={}&department={}&program={}".format(year, level, department, programs[program])
    print(url)
    class_soup = create_soup(url)
    return get_classes(class_soup)


def run(params):
    classes = create_classes(params)
    # get_quarter_classes(classes)
    return classes


if __name__ == '__main__':
    run(get_user_input())

