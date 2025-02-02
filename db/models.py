from datetime import datetime

from sqlalchemy import Column, Integer, String,ForeignKey,Table,DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, Session,relationship
from sqlalchemy.sql.functions import current_timestamp

from db.config import engine

from sqlalchemy import create_engine
engine=engine
engine=create_engine(engine)
engine.connect()

class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()+'s'
class HomeBase(Base):
    __abstract__=True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
favorite_table=Table(
    'favorites',
    Base.metadata,
    Column('user_id',Integer,ForeignKey('users.id')),
    Column('movie_id',Integer,ForeignKey('movies.id'))
)

class User(HomeBase):
    first_name:Mapped[str]=mapped_column(nullable=True)
    user_name:Mapped[str]=mapped_column(nullable=True,default="None")
    user_id:Mapped[str]=mapped_column(String,nullable=True,unique=True)
    is_follow:Mapped[str]=mapped_column(String,nullable=True,default="false")
    favorite_movies:Mapped[list['Movie']]=relationship(secondary=favorite_table,back_populates='favorite_users')
    is_blockes:Mapped[str]=mapped_column(String,nullable=True,default="false")
    created_at:Mapped[datetime]=mapped_column(DateTime,default=current_timestamp)
    is_admin:Mapped[str]=mapped_column(String,nullable=True,default="false")


class Movie(HomeBase):
    film:Mapped[str]=mapped_column(String,unique=True)
    film_code:Mapped[int]=mapped_column(Integer,autoincrement=True)
    title:Mapped[str]=mapped_column(nullable=True)
    description:Mapped[str]=mapped_column(nullable=True)
    genre:Mapped[str]=mapped_column(nullable=True)
    year:Mapped[str]=mapped_column(nullable=True)
    language:Mapped[str]=mapped_column(nullable=True)
    country:Mapped[str]=mapped_column(nullable=True)
    age_border:Mapped[str]=mapped_column(nullable=True)
    favorite_users:Mapped[list['User']]=relationship(secondary=favorite_table,back_populates='favorite_movies')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    thumbnail:Mapped[str]=mapped_column(nullable=True)
    visit_count:Mapped[int]=mapped_column(Integer,nullable=True)
    added_by:Mapped[str]=mapped_column(nullable=True)

class Review(HomeBase):
    user_id:Mapped[str]=mapped_column(nullable=True)
    review:Mapped[str]=mapped_column(nullable=True)



Base.metadata.create_all(engine)
engine.dispose()
session = Session(engine)

class Models:
    User=User
    Movie=Movie
    Review=Review


