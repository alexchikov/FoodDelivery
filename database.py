from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base
import config

Base = declarative_base()

class Items(Base):
    __tablename__ = 'items'
    
    id = Column('id', 
                Integer, 
                primary_key=True,
                nullable=False,
                autoincrement=True,
                unique=True)
    
    name = Column('name',
                  String(80),
                  nullable=False)
    
    price = Column('price',
                   Integer,
                   nullable=False)
    
class Orders(Base):
    
    __tablename__ = 'orders'
    
    id = Column('id', 
                Integer, 
                primary_key=True,
                nullable=False,
                autoincrement=True,
                unique=True)
    
    datetime = Column('datetime', 
                      DateTime, 
                      nullable=False)
    
    customer_name = Column('customer_name',
                           String(120),
                           nullable=False)
    
    city = Column('city', String(80))
    street = Column('street', String(80))
    
    ordered_items = ...
    
    total_price = Column('total_price',
                         Integer,
                         nullable=False)
    
    delivery_instructions = Column('delivery_instructions',
                                   String(200))
    
    
engine = create_engine(f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
Base.metadata.create_all(engine)