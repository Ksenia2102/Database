import time

from db import db_session
from models import Company, Employee

def employees_by_company(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    employee_list = []
    if company:
        for employee in Employee.query.filter(Employee.company_id == company.id):
            employee_list.append(f'{company.name} - {employee.name}')
        return employee_list

def employees_by_company_joined(company_name):
    query = db_session.query(Employee, Company).join(
        Company, Employee.company_id == Company.id
    ).filter(Company.name == company_name)
    employee_list =[]
    for employee, company in query:
            employee_list.append(f'{company.name} - {employee.name}')
    return employee_list

def employees_by_company_relation(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    employee_list = []
    if company:
        for employee in company.employees:
            employee_list.append(f'{company.name} - {employee.name}')
        return employee_list

if __name__ == '__main__':
    start = time.perf_counter()
    # for _ in range(100):
    #     employees_by_company('Мосметрострой')
    # print(time.perf_counter() - start)

    # for _ in range(100):
    #     employees_by_company_joined('Мосметрострой')
    # print(time.perf_counter() - start)

    for _ in range(100):
        employees_by_company_relation('Мосметрострой')
    print(time.perf_counter() - start)