import csv
from datetime import datetime
from sqlalchemy.ext import SQLAlchemyError

from db import db_session
from models import Company, Employee, Payment, Project, ProjectEmployee


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['project_name',  'company_id', 'employee_id', 'date_start', 'date_end']
        reader = csv.DictReader(f, fields, delimiter=';')
        for row_num, row in enumerate(reader, start=1):
            try:
                process_row(row)
            except (TypeError, ValueError) as e:
                print_error(row_num, 'Неправильный формат данных: {}', e)
            except SQLAlchemyError as e:
                print_error(row_num, 'Нарушена целостность данных: {}', e)

def print_error(row_num, error_text, exception):
    print(f"Ошибка на строке {row_num}")
    print(error_text.format(exception))
    print('-' * 80)


def prepare_data(row):
    row['company_id'] = int(row['company_id'])
    row['employee_id'] = int(row['employee_id'])
    row['date_start'] = datetime.strptime(row['date_start'], '%Y-%m-%d')
    row['date_end'] = datetime.strptime(row['date_end'], '%Y-%m-%d')
    return row


def process_row(row):
    row = prepare_data(row)
    project = get_or_create_project(row['project_name'], row['company_id'])
    save_project_employee(project, row)


def get_or_create_project(name, company_id):
    project = Project.query.filter(
        Project.name == name, Project.company_id == company_id
    ).first()
    if not project:
        project = Project(name=name, company_id=company_id)
        db_session.add(project)
        try:
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise 
    return project


def save_project_employee(row, project):
    project_employee = ProjectEmployee(
        employee_id=row['employee_id'],
        project_id=project.id,
        date_start=row['date_start'],
        date_end=row['date_end'],
    )
    db_session.add(project_employee)
    try:
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        raise 


def save_companies(data):
    processed = []
    unique_companies = []
    for row in data:
        if row['company'] not in processed:
            company = {
                'name': row['company'],
                'city': row['city'],
                'address': row['address'],
                'phone': row['phone_company']
            }
            unique_companies.append(company)
            processed.append(company['name'])
    db_session.bulk_insert_mappings(Company, unique_companies, return_defaults=True)
    db_session.commit()
    return unique_companies



def get_company_by_id(companies, company_name):
    for company in companies:
        if company['name'] == company_name:
            return company['id']


def save_employees(data, companies):
    processed = []
    unique_emploeeys = []
    for row in data:
        if row['phone_person'] not in processed:
            employee = {
                'name': row['name'],
                'job': row['job'],
                'email': row['email'],
                'phone': row['phone_person'],
                'date_of_birth': row['date_of_birth'],
                'company_id': get_company_by_id(companies, row['company'])
            }
            unique_emploeeys.append(employee)
            processed.append(employee['phone'])
    db_session.bulk_insert_mappings(Employee, unique_emploeeys, return_defaults=True)
    db_session.commit()
    return unique_emploeeys


def get_employee_by_id(employees, phone):
    for employee in employees:
        if employee['phone'] == phone:
            return employee['id']


def save_payments(data, employees):
    payments = []
    for row in data:
        payment = {
            'payment_date': row['payment_date'],
            'ammount': row['ammount'],
            'employee_id': get_employee_by_id(employees, row['phone_person'])
        }
        payments.append(payment)
    db_session.bulk_insert_mappings(Payment, payments)
    db_session.commit()


if __name__ == '__main__':
    # all_data = read_csv('salary.csv')
    # companies = save_companies(all_data)
    # employees = save_employees(all_data, companies)
    # save_payments(all_data, employees)
    read_csv()
    