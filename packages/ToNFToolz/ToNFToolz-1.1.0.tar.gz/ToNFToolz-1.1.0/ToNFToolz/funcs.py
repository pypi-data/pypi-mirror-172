import json
import time
import base64
import asyncio
from math import ceil
from typing import List

from tonsdk.boc import Cell
from tonsdk.utils import Address, bytes_to_b64str, b64str_to_bytes

from ton import TonlibClient

from .utils import *


async def _get_client(ls: int):
    TonlibClient.enable_unaudited_binaries()
    client = TonlibClient(ls_index=ls)
    await client.init_tonlib()

    return client


def get_client(ls: int = 0) -> TonlibClient:
    client = asyncio.get_event_loop().run_until_complete(_get_client(ls))
    return client


def get_nft_owner(addr: str, client: TonlibClient = None):
    if not client:
        client = get_client(2)
    return asyncio.get_event_loop().run_until_complete(_get_nft_owner(client, addr))


async def _get_nft_owner(client: TonlibClient, addr: str):
    account = await client.find_account(addr)
    x = await account.get_nft_data()
    owner_address = x['owner_address'].to_string()
    sale_data = await get_nft_sale(client, owner_address)
    if sale_data:
        owner_address = sale_data['owner']['address']
    return owner_address


def get_items(client: List[TonlibClient] or TonlibClient, addresses: list, filename_with_nft_metadata=None,
              max_requests: int = 1000):
    items = {}
    if filename_with_nft_metadata and 'json' not in filename_with_nft_metadata:
        raise Exception('Only .json files are expected')
    elif filename_with_nft_metadata:
        with open(filename_with_nft_metadata, 'r') as j:
            items = json.loads(j.read())
    nft_items = []

    if isinstance(client, list):
        pass
    else:
        client = [client]

    d = 0

    for i in range(ceil(len(addresses) / max_requests)):
        tasks = []
        for addr in addresses[i * max_requests:min(len(addresses), max_requests * (i + 1))]:
            tasks.append(get_item(client[d % len(client)], addr, nft_items, items))
            d += 1
        # asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        print('DONE')
    if len(nft_items) < len(addresses):
        raise Exception('SCANNED NOT ALL ITEMS')
    return {"nft_items": nft_items}


async def get_item(client: TonlibClient, addr: str, nft_items: list, items: dict = None):
    account = await client.find_account(addr, preload_state=False)
    x = await account.get_nft_data()
    collection_address = x['collection_address'].to_string()
    owner_address = x['owner_address'].to_string()
    nft_address = Address(addr).to_string(is_user_friendly=False)
    content_url = await get_nft_content_url(client, x['content'], collection_address)

    if items:
        if str(x['index']) in items:
            content = items[str(x['index'])]
        elif nft_address in items:
            content = items[nft_address]
        else:
            content = await get(content_url)
    else:
        content = await get(content_url)

    collection_content = await get_collection_content(client, x['collection_address'].to_string())
    result = {
        'address': nft_address,
        'collection': {
            'address': collection_address,
            'name': collection_content.get('name'),
            'description': collection_content.get('description'),
            'image': collection_content.get('image')
        },
        'collection_address': collection_address,
        'index': x['index'],
        'content_url': content_url,
        'metadata': {
            'attributes': content.get('attributes'),
            'description': content.get('description'),
            'image': content.get('image'),
            'name': content.get('name'),
        },
        'owner': {
            'address': x['owner_address'].to_string()
        }
    }

    sale_data = await get_nft_sale(client, owner_address)

    if sale_data:
        result['sale'] = sale_data

    nft_items.append(result)


def get_collection(client: TonlibClient, addr: str):
    return asyncio.get_event_loop().run_until_complete(_get_collection(client, addr))


async def _get_collection(client: TonlibClient, addr: str):
    account = await client.find_account(addr)
    collection_data = await account.get_collection_data()
    collection_content = await get_collection_content(client, addr)
    result = {
        'address': Address(addr).to_string(is_user_friendly=False),
        'metadata': collection_content,
        'next_item_index': collection_data['next_item_index'],
        'owner': {
            'address': collection_data['owner_address'].to_string()
        }
    }
    return result


def get_all_wallet_transactions_raw(addr: str, client: TonlibClient = None):
    """
    highly recommend to use with client which ls index = 2, for e.g. client = get_client(ls=2)
    """
    if not client:
        client = get_client(2)
    return asyncio.get_event_loop().run_until_complete(_get_all_wallet_transactions_raw(client, addr))


def get_all_wallet_transactions(addr: str, client: TonlibClient = None):
    """
    highly recommend to use with client which ls index = 2, for e.g. client = get_client(ls=2)
    """
    if not client:
        client = get_client(2)
    return asyncio.get_event_loop().run_until_complete(_get_all_wallet_transactions(client, addr))


async def _get_all_wallet_transactions(client: TonlibClient, addr: str):
    all_transactions = await _get_all_wallet_transactions_raw(client, addr)
    result = []
    for tr in all_transactions:
        tr_result = {
            'type': '',  # in or out
            'from': '',  # address in raw format
            'to': '',  # address in raw format
            'value': '',  # value in nanoTon, divide by 10**9 to get Ton
            'message': '',  # comment
            'fee': tr['fee'],
            # 'status': '',  # OK or ERROR TODO
            'timestamp': tr['utime'],  # unix timestamp of transaction
        }
        if len(tr['out_msgs']):
            tr_result['type'] = 'out'
            tr_result['from'] = Address(addr).to_string(is_user_friendly=True)
            tr_result['to'] = Address(tr['out_msgs'][0]['destination']['account_address']).to_string(is_user_friendly=True)
            tr_result['value'] = int(tr['out_msgs'][0]['value'])
            tr_result['message'] = base64.b64decode(tr['out_msgs'][0]['msg_data']['text']).decode('utf-8') if tr['out_msgs'][0]['msg_data']['@type'] == 'msg.dataText' else ''
        else:
            tr_result['type'] = 'in'
            tr_result['from'] = Address(tr['in_msg']['source']['account_address']).to_string(is_user_friendly=True)
            tr_result['to'] = Address(addr).to_string(is_user_friendly=True)
            tr_result['value'] = int(tr['in_msg']['value'])
            tr_result['message'] = base64.b64decode(tr['in_msg']['msg_data']['text']).decode('utf-8') if tr['in_msg']['msg_data']['@type'] == 'msg.dataText' else ''
        result.append(tr_result)
    return result


async def _get_all_wallet_transactions_raw(client: TonlibClient, addr: str):
    account = await client.find_account(addr)
    all_transactions = []
    limit = 30  # must be more than 1
    trs = await account.get_transactions(limit=limit)
    for tr in trs:
        all_transactions.append(tr.to_json())
    while len(trs) == limit:
        trs = await account.get_transactions(from_transaction_lt=trs[-1].to_json()['transaction_id']['lt'],
                                             from_transaction_hash=trs[-1].to_json()['transaction_id']['hash'],
                                             limit=limit)
        for tr in trs[1:]:
            all_transactions.append(tr.to_json())
    return all_transactions


def get_nft_items_by_owner_address(addr: str, client: TonlibClient = None):
    """
    highly recommend to use with client which ls index = 2, for e.g. client = get_client(ls=2)
    """
    if not client:
        client = get_client(2)
    return asyncio.get_event_loop().run_until_complete(_get_nft_items_by_owner_address(client, addr))


async def _get_nft_items_by_owner_address(client: TonlibClient, addr: str):
    result = set()
    all_transactions = await _get_all_wallet_transactions(client, addr)
    for tr in all_transactions:
        print(tr['type'])
        if tr['type'] == 'in':
            account = await client.find_account(tr['from'])
            try:
                nft_data = await account.get_nft_data()
                owner = nft_data['owner_address'].to_string()
                sale = await get_nft_sale(client, addr)
                if sale:
                    owner = sale['owner']['address']
                if owner == Address(addr).to_string(is_user_friendly=False):
                    result.add(tr['from'])
            except:
                continue
    return list(result)
