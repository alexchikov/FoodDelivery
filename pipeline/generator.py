import os
import random
import logging
import sys
import samples
import json
from time import sleep
from datetime import datetime

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(levelname)s (%(asctime)s): %(message)s")


def generate_items(number: int, items: list) -> dict:
    order_items, summa = list(), int()
    for item in range(number):
        while True:
            id = random.randint(1, 20)
            for item in order_items:
                if id == int(item["item_id"]):
                    id = None
            if id is not None:
                break
        quantity = random.randint(1, 10)
        order_items.append({"item_id": items[id-1]["item_id"],
                            "quantity": quantity
                            })
        summa += round(items[id-1]["price"]*quantity, 2)
    return (order_items, summa)


def generate_order(current_id: id) -> dict:
    customer_gender = random.choice(["male", "female"])
    customer_name = random.choice(samples.name_samples[customer_gender])
    customer_surname = random.choice(samples.surname_samples[customer_gender]) if not None else ""

    customer_address = random.choice(samples.addresses)
    customer_address = f'{customer_address["city"]}, {customer_address["street"]}, {customer_address["house"]}'

    with open(f"./items.json") as file:
        customer_items = generate_items(random.randint(1, 10), json.load(file))
    return {"order_id": current_id,
            "date": datetime.now().strftime("%d.%m.%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "customer_name": f"{customer_name} {customer_surname}",
            "customer_address": customer_address,
            "ordered_items": customer_items[0],
            "total_price": customer_items[1],
            "delivery_instructions": "Please ring doorbell when delivering."
            }


if __name__ == "__main__":
    if os.listdir('./orders'):
        id = int(sorted(os.listdir("./orders"), key=lambda x: int(x.split('_')[1]))[-1].split('_')[1])
    else:
        id = 0
    while True:
        id += 1
        order = generate_order(id)
        logging.info(f"Successfully generated order {id}")
        with open(f"./orders/order_{id}_{datetime.now().strftime('%d-%m_%H:%M')}.json", "w") as file:
            json.dump(order, file, indent=4,
                      ensure_ascii=False, separators=[",", ":"])
        sleep(random.randint(5, 60))
