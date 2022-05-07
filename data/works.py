import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Work(SqlAlchemyBase):
    __tablename__ = 'works'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photos = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.TEXT)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.chat_id"))
    result = sqlalchemy.Column(sqlalchemy.FLOAT)
    user = orm.relation('User')
