import json
import logging
import os
import asyncio
import sys

logging.basicConfig(logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(levelname)s (%(asctime)s): %(message)s"))


def delta(prev_listdir: list):
    return set(os.listdir("orders"))-set(prev_listdir)


async def parse(path: str):
    with open(f"orders/{path}") as file:
        data = json.load(file)
        