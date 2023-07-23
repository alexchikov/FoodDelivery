import random
import typing

def generate_items(number: int) -> typing.Generator:
    for item in range(number):
        yield {"item_id":random.randint()}