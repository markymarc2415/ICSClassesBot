import RMPCrawl
import CourseListingCrawl
from collections import defaultdict


def get_user_input():
    year = "2017"  # input("Year: ")
    level = "Lower-Division"  # input("Level: ")
    department = "ALL"  # input("Department: ")
    program = input("Program: ")
    return year, level, department, program


def create_ratings_database(classes):
    database = dict()
    all_quarters = ["Fall", "Winter", "Spring"]

    for class_name, instructor in classes.items():
        for quarter in all_quarters:
            for prof in instructor[quarter]:
                if prof not in database and prof not in ("TBD", ""):
                    prof_ratings = RMPCrawl.run(prof)
                    if prof_ratings not in(None, dict()):
                        database[prof] = prof_ratings

    return database


def prof_quarter(classes, ratings_database, quarter):
    best_combination = defaultdict(list)

    for class_name, instructor in classes.items():
        for prof in instructor[quarter]:
            if prof in ratings_database and prof not in ("TBD", ""):
                best_combination[class_name].append((ratings_database[prof]['quality'], prof))

        best_combination[class_name].sort(reverse=True)

    return best_combination


def prof_quarters(classes, class_name, prof_name):
    result = []
    for quarter in ("Fall", "Winter", "Spring"):
        if prof_name in classes[class_name][quarter]:
            result.append(quarter)
    return result


def best_class(classes, ratings_database):

    all_quarters = ["Fall", "Winter", "Spring"]
    database = dict()

    for quarter in all_quarters:
        best_profs = prof_quarter(classes, ratings_database, quarter)
        for class_name,prof in best_profs.items():
            if len(prof) != 0:
                if class_name not in database:
                    database[class_name] = (prof[0][0], prof[0][1], prof_quarters(classes, class_name, prof[0][1]))
                else:
                    if prof[0][0] > database[class_name][0]:
                        database[class_name] = (prof[0][0], prof[0][1], prof_quarters(classes, class_name, prof[0][1]))

    return database


def run(year="2017", level="Lower-Division", department="ALL", program="ALL"):
    classes = CourseListingCrawl.run((year, level, department, program))
    database = create_ratings_database(classes)
    return best_class(classes, database)


if __name__ == '__main__':
    # classes = CourseListingCrawl.run(get_user_input())
    classes = CourseListingCrawl.run(("2017", "Upper-Division", "ALL", "ALL"))
    print(classes)
    database = create_ratings_database(classes)
    y = best_class(classes, database)
    
    for x in y:
        print(x, y[x])