import json
import logging
import os
import psycopg2
import sys
import datetime
from time import sleep

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(levelname)s (%(asctime)s): %(message)s")

connection = psycopg2.connect(dbname="fooddelivery", user="admin",
                              password="admin", host="localhost", port=5432)

cursor = connection.cursor()


def parse(path_to_file: str):
    with open(f"./orders/{path_to_file}") as file:
        data = json.load(file)
        cursor.execute("INSERT INTO orders (id, datetime, customer_name, city, street, total_price, delivery_instructions)\
            VALUES (%s, %s, %s, %s, %s, %s, %s);", (data["order_id"],
                                                datetime.datetime.strptime((data["date"] + ' ' + data["time"]), 
                                                                               '%d.%m.%Y %H:%M:%S'),
                                                data["customer_name"],
                                                data["customer_address"].split(', ')[0],
                                                    ', '.join(data["customer_address"].split(', ')[1:]),
                                                data["total_price"],
                                                data["delivery_instructions"],))
        for item in data["ordered_items"]:
            cursor.execute("INSERT INTO ordered_items (order_id, item_id, quantity)\
                VALUES (%s, %s, %s);", (data["order_id"], item["item_id"], item["quantity"],))
        connection.commit()

def main():
    if os.listdir('./orders'):
        cursor.execute('SELECT id from orders;')
        last_order_id = cursor.fetchall()
        listdir = [x for x in sorted(os.listdir('./orders'), key=lambda x: int(x.split('_')[1])) 
                   if int(x.split('_')[1]) <= last_order_id[-1][0]]
    else:
        listdir = []
    while True:
        for file in (set(os.listdir(f"./orders/"))-set(listdir)):
            parse(file)
            logging.info(f"parsed file {file}")
        listdir = os.listdir(f"./orders/")
        sleep(5)

if __name__ == "__main__":
    main()