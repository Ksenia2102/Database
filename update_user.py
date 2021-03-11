from db import db_session
from models import User

user = User.query.first()

user.salary = 150000
db_session.commit()