import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    chat_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    ident = sqlalchemy.Column(sqlalchemy.String)
    jobs = orm.relation("Work", back_populates='user')
