from loguru import logger
from settings import RETRY_COUNT
from utils.sleeping import sleep


def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries <= RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                await sleep(10, 20)
                retries += 1

    return wrapper


def remove_wallet(private_key: str):
    with open("accounts.txt", "r") as file:
        lines = file.readlines()

    line_index = 0
    for line in lines:
        if private_key in line:
            break
        else: 
            line_index += 1

    with open("accounts.txt", "w") as file:
        for line in lines:
            if private_key not in line:
                file.write(line)

    with open("proxy.txt", "r") as file:
        lines = file.readlines()

    index = 0
    with open("proxy.txt", "w") as file:
        for line in lines:
            if index != line_index:
                file.write(line)
            index += 1

