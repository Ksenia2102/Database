from sqlalchemy import Column, Integer, String, Date
from db import Base, engine

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     name = Column(String())
#     salary = Column(Integer())
#     email = Column(String(120), unique=True)

#     def __repr__(self):
#         return f'User {self.id}, {self.name}'

class Salary(Base):
    __tablename__ = 'salaries'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    address = Column(String)
    company = Column(String)
    job = Column(String)
    phone_number = Column(String)
    email = Column(String)
    date_of_birth = Column(Date)
    salary = Column(Integer)

    def __repr__(self):
        return f'Salary {self.id}, {self.name}, {self.company}'

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)