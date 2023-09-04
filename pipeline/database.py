from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, SmallInteger, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import config
import psycopg2
import json

Base = declarative_base()


class Items(Base):
    __tablename__ = 'items'

    id = Column('id',
                Integer,
                primary_key=True,
                nullable=False,
                autoincrement=False,
                unique=True)

    name = Column('name',
                  String(80),
                  nullable=False)

    price = Column('price',
                   Float,
                   nullable=False)


class Orders(Base):
    __tablename__ = 'orders'

    id = Column('id',
                Integer,
                primary_key=True,
                nullable=False,
                autoincrement=False,
                unique=True)

    datetime = Column('datetime',
                      DateTime,
                      nullable=False)

    customer_name = Column('customer_name',
                           String(120),
                           nullable=False)

    city = Column('city', String(80))
    street = Column('street', String(80))

    total_price = Column('total_price',
                         Integer,
                         nullable=False)

    delivery_instructions = Column('delivery_instructions',
                                   String(200))


class Ordered_items(Base):
    __tablename__ = 'ordered_items'

    id = Column('id',
                Integer,
                primary_key=True,
                nullable=False,
                autoincrement=True,
                unique=True)

    order_id = Column('order_id', ForeignKey('orders.id'))
    item_id = Column('item_id', ForeignKey('items.id'))
    quantity = Column('quantity', SmallInteger)
    items = relationship("Items")
    orders = relationship("Orders")


engine = create_engine(
    f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
Base.metadata.create_all(engine)

connection = psycopg2.connect(dbname="fooddelivery", user="admin",
                              password="admin", host="localhost", port=5432)

cursor = connection.cursor()

with open("../items.json") as file:
    data = json.load(file)

for item in data:
    cursor.execute(f"INSERT INTO items (id, name, price) VALUES (%s,%s,%s);", (int(
        item["item_id"]), f'{item["item_name"]}', item["price"]))
    connection.commit()
cursor.close()
connection.close()
