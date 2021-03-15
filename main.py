import csv


def get_department_name(dep_line: str) -> str:
    """Get department name from the line"""
    department = dep_line.split(' –> ')
    return department[1]


def new_dep_info(dep_line: list, dep_name: str) -> list:
    """Creates list of new department name, workers count, min payment, max payment"""
    return [dep_name, 1, str(dep_line[4])[:-2], str(dep_line[4])[:-2], str(dep_line[4])[:-2], 0]


def dep_appender(all_dep: list, dep_line: list, dep_name: str) -> list:
    """Adds department that was not mentioned before"""
    new_dep = new_dep_info(dep_line, dep_name)
    all_dep.append(new_dep)
    return all_dep


def dep_aggregator(all_dep: list, dep_line: list, place: int) -> list:
    """Aggregates info about one department"""
    all_dep[place][1] += 1
    payment_value = int(dep_line[:-2])
    payment_sum = int(all_dep[place][4])
    all_dep[place][4] = str(payment_sum + payment_value)
    min_payment_value = int(all_dep[place][2])
    max_payment_value = int(all_dep[place][3])
    if min_payment_value > payment_value:
        all_dep[place][2] = payment_value
    if max_payment_value < payment_value:
        all_dep[place][3] = payment_value
    return all_dep


def agr_department(all_dep: list, dep_line: list) -> list:
    """Aggregates information from all info list into department info"""
    dep_name = get_department_name(dep_line[2])
    place = -1
    for i in all_dep:
        place += 1
        if dep_name in i:
            all_dep = dep_aggregator(all_dep, dep_line[4], place)
            return all_dep
    all_dep = dep_appender(all_dep, dep_line, dep_name)
    return all_dep


def create_summary_report(reader):
    """Create summary report"""
    rep_agr = list()
    for row in reader:
        line = str(row)
        line2 = list(line.split(';'))
        all_dep = agr_department(rep_agr, line2)
    for i in all_dep:
        i[5] = int(str(i[4]))/int(str(i[1]))
    return all_dep


def show_all_departments(all_dep: list):
    """Print all department names"""
    for i in all_dep:
        print(i[0])


def write_report_to_csv(all_dep: list):
    """Writes report to csv"""
    with open('agr_report.csv', 'w', newline='') as file:
        write = csv.writer(file)
        write.writerows(all_dep)


def print_report(all_dep: list):
    for i in all_dep:
        print('Department:', i[0], ';Workers count:', i[1], ';Min payment:', i[2],
              '; Max payment:', i[3], ';Middle payment:', i[5])


if __name__ == '__main__':
    print('Введите имя файла или не вводите, если назвали report.csv')
    file_name = input("Enter filename : ") or "report.csv"
    with open(file_name, encoding='UTF-8-sig') as f:
        reader = csv.reader(f)
        print('Падажжи я работаю...')
        summary_report = create_summary_report(reader)
    print('1 - вывести отделы 2 - вывести отчет 3 - выгрузить отчет в csv')
    a_dict = {'1': show_all_departments, '2': print_report, '3': write_report_to_csv}
    option = ''
    while option not in a_dict:
        option = input()
    a_dict[option](summary_report)
    print('ALL DONE')