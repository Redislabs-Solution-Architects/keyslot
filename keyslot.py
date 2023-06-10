'''
@Maker Joey Whelan
'''
import crcmod
from argparse import ArgumentParser
import requests
import re2

SHARD_EP = '/v1/shards/stats'

crc16 = crcmod.predefined.mkCrcFun('xmodem')
requests.urllib3.disable_warnings()

def find_slot(args) -> dict:
    key = args.key
    m = re2.match(".*\\{(?P<tag>.*)\\}.*", key)
    if m:
        key = m.group('tag')

    slot = crc16(bytes(key.encode())) % 16384
    node = 1
    for shard in fetch_shards(args):
        if slot >= shard['begin'] and slot <= shard['end']:
            node = shard['node']
            break
    return { 'key': key, 'slot': slot, 'node': node }

def fetch_shards(args):
    headers = {'Accept': 'application/json'}
    params = {'parent_uid': args.dbid}
    shards = []
    try:
        r = requests.get(args.url + SHARD_EP, auth=(args.user, args.password),  headers=headers, params=params, verify=False)
        r.raise_for_status()
        arr = r.json()
        for item in arr:
            if item['role'] == 'master':
                node = int(item['node_uid'])
                slots = item['assigned_slots'].split('-')
                begin = int(slots[0])
                end = int(slots[1])
                shards.append({'node': node, 'begin': begin, 'end': end})
        return shards
    except Exception as err:
        raise SystemExit(err)

if __name__ == '__main__':
    parser = ArgumentParser(description='Redis Key Slot Finder')
    parser.add_argument('key', type=str, help='a key for slot look up')
    parser.add_argument('--url', required=True, type=str, help='Redis REST API URL')
    parser.add_argument('--user', required=True, type=str, help='Redis REST API user name')
    parser.add_argument('--password', required=True, type=str, help='Redis REST API user name')
    parser.add_argument('--dbid', required=True, type=int, help='Redis Database ID')
    args = parser.parse_args()
    print(find_slot(args))