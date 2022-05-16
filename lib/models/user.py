import discord
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.exc import NoResultFound

from lib.database import Base, db_session


class FailedToCreateUser(Exception):
    def __init__(self, exception):
        print(f">>> {exception}")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    discord_id = Column(Integer, unique=True)
    pickaxe_level = Column(String, default="Wood")

    total = Column(Integer, default=0)

    created_at: datetime = Column(DateTime, default=discord.utils.utcnow())

    def __repr__(self):
        rep = f'User({self.id=}, {self.discord_id=}, {self.total=})'
        return rep

    @classmethod
    async def get_or_create(cls, discord_instance: discord.Member):
        try:
            data = db_session.query(User). \
                filter_by(discord_id=discord_instance.id).one()
        except NoResultFound:
            obj = User()

            obj.discord_id = discord_instance.id

            db_session.add(obj)
            db_session.commit()

            data = db_session.query(User). \
                filter_by(discord_id=discord_instance.id).one()
        except Exception as e:
            raise FailedToCreateUser(e)

        return data
