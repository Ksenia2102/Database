from db import db_session
from models import User

user = User(name='Oleg', salary=180000, email='oleg@mail.ru')
db_session.add(user)
db_session.commit()