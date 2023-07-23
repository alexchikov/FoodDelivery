import random
import logging
import sys
import samples
import json

logging.basicConfig(logging.INFO, stream=sys.stdout)

def generate_items(number: int, items: list) -> dict:
    order_items, summa = list(), int()
    for item in range(number):
        id = random.randint(1,20)
        quantity = random.randint(1,10)
        order_items.append({"item_id": items[id]["item_id"],
                            "item_name": items[id]["item_name"],
                            "quantity": quantity
                            })
        summa += items[id]["price"]*quantity
    return (order_items, summa)
        
def generate_order(current_id: id) -> dict:
    customer_gender = random.choice(["male", "female"])
    customer_name = random.choice(samples.name_samples[customer_gender])+" "+\
        random.choice(samples.surname_samples[customer_gender])
    
    customer_address = " ".join([val for val in random.choice(samples.addresses).values()])
    with open("items.json") as file:
        customer_items = generate_items(random.randint(1,10), json.load(file))
    return {
    "order_id": current_id,
    "customer_name": customer_name,
    "customer_address": customer_address,
    "order_items": customer_items[0],
    "total_price": customer_items[1],
    "delivery_instructions": "Please ring doorbell when delivering."
}
    