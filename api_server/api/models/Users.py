from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, Text, Table, Boolean

class Users:
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String)
    password = Column('password', String)
    status = Column('status', Boolean, default=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password