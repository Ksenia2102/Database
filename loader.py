import csv
import time 

from db import db_session
from models import Salary

# def read_csv2(filename):
#     with open(filename, 'r', encoding='utf-8') as f:
#         fields = ['name', 'city_name', 'street_address',
#     'large_company', 'job', 'phone_number',
#     'free_email', 'date_of_birth', 'salary']
#         reader = csv.DictReader(f, fields, delimiter=';')
#         for row in reader:
#             save_salary_data(row)
    
def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['name', 'city', 'address',
    'company', 'job', 'phone_number',
    'email', 'date_of_birth', 'salary']
        reader = csv.DictReader(f, fields, delimiter=';')
        salary_data = []
        for row in reader:
            salary_data.append(row)
        save_salary_data(salary_data)

# def save_salary_data2(row):
#     salary = Salary(name=row['name'], city=row['city_name'], address=row['street_address'], 
#                     company=row['large_company'], job=row['job'], phone_number=row['phone_number'],
#                     email=row['free_email'], date_of_birth=row['date_of_birth'], salary=row['salary'])
#     db_session.add(salary)
#     db_session.commit()

def save_salary_data(data):
    db_session.bulk_insert_mappings(Salary, data)
    db_session.commit()

if __name__ == '__main__':
    start = time.time()
    read_csv('salary.csv')
    print(time.time() - start)