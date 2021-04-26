import time

from db import db_session
from models import Company, Employee, Project


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


def company_projects_employees(company_name):
    query = Project.query.join(Project.company, Project.employees).filter(Company.name == company_name)

    for project in query:
        print('-' * 20)
        print(project.name)
        for employee in project.employees:
            print(f"{employee.employee.name} {(employee.date_end - employee.date_start).days} день")


if __name__ == '__main__':
    company_projects_employees('РусГидро')
