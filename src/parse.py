import json
import logging
import os
import psycopg2
import sys
import datetime
from time import sleep
from paths import PATH

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(levelname)s (%(asctime)s): %(message)s")

connection = psycopg2.connect(dbname="fooddelivery", user="admin",
                              password="admin", host="localhost", port=5432)

cursor = connection.cursor()


def parse(path_to_file: str):
    with open(f"{PATH}orders/{path_to_file}") as file:
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
    listdir = list()
    while True:
        for file in (set(os.listdir(f"{PATH}orders/"))-set(listdir)):
            parse(file)
            logging.info(f"parsed file {file}")
        listdir = os.listdir(f"{PATH}orders/")
        sleep(5)

if __name__ == "__main__":
    main()