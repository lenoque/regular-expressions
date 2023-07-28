import csv
import re


def format_name(lastname, firstname, surname):
    if len(lastname.split()) == 3:  # ФИО
        lastname, firstname, surname = lastname.split()
    if len(firstname.split()) == 2:  # Ф+ИО
        firstname, surname = firstname.split()
    if len(lastname.split()) == 2:  # ФИ
        lastname, firstname = lastname.split()
    return lastname, firstname, surname


def format_phone_numbers(phone):
    pattern = r"(\+7|8)?\s?\(?(\d{3}?)\)?[-\s]?(\d{3})[-\s]?(\d{2})-?(\d{2})(\s?)\(?([доб.]{4})?\s?(\d{4})?\)?"
    substitution = r"+7(\2)\3-\4-\5\6\7\8"
    return re.sub(pattern, substitution, phone)


if __name__ == "__main__":

    contacts_list = {}
    with open("phonebook_raw.csv", encoding='utf-8') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            lastname, firstname, surname = format_name(row['lastname'], row['firstname'], row['surname'])
            phone = format_phone_numbers(row['phone'])
            if (lastname, firstname, surname) not in contacts_list:
                contacts_list[(lastname, firstname, surname)] = {
                    'lastname': lastname,
                    'firstname': firstname,
                    'surname': surname,
                    'organization': row['organization'],
                    'position': row['position'],
                    'phone': phone,
                    'email': row['email']
                }
            elif phone and not contacts_list[(lastname, firstname, surname)]['phone']:
                contacts_list[(lastname, firstname, surname)]['phone'] = phone

    fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    with open("phonebook.csv", "w", encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts_list.values())
