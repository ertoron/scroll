import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import questionary
from loguru import logger
from questionary import Choice

from config import ACCOUNTS, PROXIES
from settings import (
    RANDOM_WALLET,
    SLEEP_TO,
    SLEEP_FROM,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO, REMOVE_WALLET
)
from modules_settings import *
from utils.helpers import remove_wallet
from utils.sleeping import sleep


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Deposit to Scroll", deposit_scroll),
            Choice("2) Withdraw from Scroll", withdraw_scroll),
            Choice("3) Bridge Orbiter", bridge_orbiter),
            Choice("4) Bridge Layerswap", bridge_layerswap),
            Choice("5) Wrap ETH", wrap_eth),
            Choice("6) Unwrap ETH", unwrap_eth),
            Choice("7) Swap on Skydrome", swap_skydrome),
            Choice("8) Swap on Zebra", swap_zebra),
            Choice("9) Swap on SyncSwap", swap_syncswap),
            Choice("10) Swap on Space.fi", swap_spacefi),
            Choice("11) Deposit LayerBank", deposit_layerbank),
            Choice("12) Withdraw LayerBank", withdraw_layerbank),
            Choice("13) Deposit RocketSam", deposit_rocketsam),
            Choice("14) Withdraw RocketSam", withdraw_rocketsam),
            Choice("15) Mint and Bridge Zerius NFT", mint_zerius),
            Choice("16) Mint ZkStars NFT", mint_zkstars),
            Choice("17) Create NFT collection on Omnisea", create_omnisea),
            Choice("18) Mint NFT on NFTS2ME", mint_nft),
            Choice("19) Mint Scroll Origins NFT", nft_origins),
            Choice("20) Dmail send email", send_mail),
            Choice("21) Create gnosis safe", create_safe),
            Choice("22) Deploy contract", deploy_contract),
            Choice("23) Swap tokens to ETH", swap_tokens),
            Choice("24) Use Multiswap", swap_multiswap),
            Choice("25) Use custom routes", custom_routes),
            Choice("26) Check transaction count", "tx_checker"),
            Choice("27) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
        print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
        sys.exit()
    return result


def get_wallets():
    account_with_proxy = dict(zip(ACCOUNTS, PROXIES))
    wallets = [
        {
            "id": _id,
            "key": key,
            "proxy": account_with_proxy[key]
        } for _id, key in enumerate(account_with_proxy, start=1)
    ]

    return wallets


async def run_module(module, account_id, key, proxy):
    try:
        await module(account_id, key, proxy)
    except Exception as e:
        logger.error(e)

    if REMOVE_WALLET:
        remove_wallet(key)

    await sleep(SLEEP_FROM, SLEEP_TO)


def _async_run_module(module, account_id, key, proxy):
    asyncio.run(run_module(module, account_id, key, proxy))


def main(module):
    wallets = get_wallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                _async_run_module,
                module,
                account.get("id"),
                account.get("key"),
                account.get("proxy")
            )
            time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))


if __name__ == '__main__':
    print("❤️ Subscribe to me – https://t.me/sybilwave\n")

    logger.add("logging.log")

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        main(module)

    print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
    print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
