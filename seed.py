from models import User
from app import aoo

db.create_all()
User.query.delete()

