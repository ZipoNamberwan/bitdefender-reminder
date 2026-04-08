import time
from pathlib import Path

import requests
from openpyxl import Workbook

cookies = {
    '_ga_FMZTHHQN2K': 'GS2.1.s1764908778$o3$g0$t1764908782$j56$l0$h0',
    'cf_clearance': 'ILIb.hwLx7TgP.MQEOXP6fQzF8htjOYDEepc8DfhdjM-1767452092-1.2.1.1-xdpO0rYhGTGl9._2rGilRZB6eXKf5XERqTujrzfICeMvGVSDYGKR5QDOcmQkavvqWcKOLK3.Icu6QftTQt.KdgQtSrvPqjss.qobiGmREl9VoMD6AEmHk5Fc89XvFO73DnWTjYmAOooXISZLDuphU2e.10MAn1sQxJbji_h5k152ZdLg5aOaIrfIxS3sqBJWnrNyLadfFWIMOaSk80fgHbtTrNlW94QhY39bUcS3U9c',
    '_ga_XXTTVXWHDB': 'GS2.3.s1767452094$o6$g0$t1767452105$j49$l0$h0',
    '_ga': 'GA1.1.1843701966.1750653428',
    '_ga_XKFNKKMMCW': 'GS2.1.s1771152511$o2$g0$t1771152511$j60$l0$h0',
    'lang': 'en_US',
    'deviceId': '86df1f2b4603f021b23975bb0b6af183e199b7024722f512042d60b47482368b',
    'lastUnifiedUsedService': '3',
    'lastUsedService': '1',
    'TS012a1668': '0167a1c86188685fde91ecefa08e9edb0a0c8dde3ad00365782a8d3cc62a27b0e157a122eae6053b15614cee0c434cb8583e4a40a6',
    'PHPSESSID': 'r0c52jpb75dq0iejgom7qkk894',
    'TS0151fc2b': '0167a1c861309e83670f1584d2a5f6bb582965fdbfe5ec6b749cc672962551b95c0f4fa9c14ba895b44a45b604f7de0927a0075a44',
    'sveView': '%7B%7D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://bitgravity.bps.go.id',
    'priority': 'u=1, i',
    'referer': 'https://bitgravity.bps.go.id/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_ga_FMZTHHQN2K=GS2.1.s1764908778$o3$g0$t1764908782$j56$l0$h0; cf_clearance=ILIb.hwLx7TgP.MQEOXP6fQzF8htjOYDEepc8DfhdjM-1767452092-1.2.1.1-xdpO0rYhGTGl9._2rGilRZB6eXKf5XERqTujrzfICeMvGVSDYGKR5QDOcmQkavvqWcKOLK3.Icu6QftTQt.KdgQtSrvPqjss.qobiGmREl9VoMD6AEmHk5Fc89XvFO73DnWTjYmAOooXISZLDuphU2e.10MAn1sQxJbji_h5k152ZdLg5aOaIrfIxS3sqBJWnrNyLadfFWIMOaSk80fgHbtTrNlW94QhY39bUcS3U9c; _ga_XXTTVXWHDB=GS2.3.s1767452094$o6$g0$t1767452105$j49$l0$h0; _ga=GA1.1.1843701966.1750653428; _ga_XKFNKKMMCW=GS2.1.s1771152511$o2$g0$t1771152511$j60$l0$h0; lang=en_US; deviceId=86df1f2b4603f021b23975bb0b6af183e199b7024722f512042d60b47482368b; lastUnifiedUsedService=3; lastUsedService=1; TS012a1668=0167a1c86188685fde91ecefa08e9edb0a0c8dde3ad00365782a8d3cc62a27b0e157a122eae6053b15614cee0c434cb8583e4a40a6; PHPSESSID=r0c52jpb75dq0iejgom7qkk894; TS0151fc2b=0167a1c861309e83670f1584d2a5f6bb582965fdbfe5ec6b749cc672962551b95c0f4fa9c14ba895b44a45b604f7de0927a0075a44; sveView=%7B%7D',
}

params = {
    'csrfToken': '526c788d785a9c6544c0f6eae942addbd357a924',
}

json_data = {
    'action': 'ProtectedEntitiesEPS',
    'method': 'getNodeChildren',
    'data': {
        'viewType': 7,
        'node': '6756a8de6e95b9d130037894',
    },
    'type': 'rpc',
    'tid': 42,
}


def fetch_node_children():
    response = requests.post(
        'https://bitgravity.bps.go.id/webservice/EPS/model',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get('result', {}).get('data', [])


def read_records(node_id):
    payload = {
        'action': 'ProtectedEntitiesEPS',
        'method': 'readRecords',
        'data': {
            'nodeId': node_id,
            'viewType': 7,
            'additionalFilters': {
                'policyTemplate': '',
                'depth': 2,
                'tagType': 1,
                'tagAttribute': '',
                'tagValue': '',
            },
            'page': 1,
            'limit': 20,
            'sort': 'name',
            'dir': 'ASC',
        },
        'type': 'rpc',
        'tid': 50,
    }

    response = requests.post(
        'https://bitgravity.bps.go.id/webservice/EPS/model',
        params=params,
        cookies=cookies,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


EXPORT_COLUMNS = [
    'parent_node_name',
    'specifics.dnsHostName',
    'specifics.fqdn',
    'specifics.ip',
    'specifics.endpointUsers.userNames',
    'specifics.endpointUsers.lastUpdate',
    'specifics.label',
    'specifics.gzTags',
]


def as_text(value):
    if value is None:
        return ''
    if isinstance(value, list):
        return ', '.join(str(item) for item in value)
    return str(value)


def extract_endpoint_users_fields(endpoint_users):
    if isinstance(endpoint_users, dict):
        return (
            as_text(endpoint_users.get('userNames', '')),
            as_text(endpoint_users.get('lastUpdate', '')),
        )

    if isinstance(endpoint_users, list):
        user_names = []
        last_updates = []
        for user in endpoint_users:
            if not isinstance(user, dict):
                continue
            if user.get('userNames') not in (None, ''):
                user_names.append(as_text(user.get('userNames')))
            if user.get('lastUpdate') not in (None, ''):
                last_updates.append(as_text(user.get('lastUpdate')))

        return (' | '.join(user_names), ' | '.join(last_updates))

    return ('', '')


def extract_gztag_names(gztags):
    if not isinstance(gztags, list):
        return ''

    names = [tag.get('name') for tag in gztags if isinstance(tag, dict) and tag.get('name')]
    return ', '.join(names)


def build_export_row(parent_node_name, child_record):
    specifics = child_record.get('specifics', {}) if isinstance(child_record, dict) else {}
    endpoint_users = specifics.get('endpointUsers', '') if isinstance(specifics, dict) else ''
    endpoint_user_names, endpoint_last_update = extract_endpoint_users_fields(endpoint_users)

    return {
        'parent_node_name': parent_node_name,
        'specifics.dnsHostName': as_text(specifics.get('dnsHostName', '')),
        'specifics.fqdn': as_text(specifics.get('fqdn', '')),
        'specifics.ip': as_text(specifics.get('ip', '')),
        'specifics.endpointUsers.userNames': endpoint_user_names,
        'specifics.endpointUsers.lastUpdate': endpoint_last_update,
        'specifics.label': as_text(specifics.get('label', '')),
        'specifics.gzTags': extract_gztag_names(specifics.get('gzTags', [])),
    }


def save_to_excel(records, output_path):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Records'

    worksheet.append(EXPORT_COLUMNS)
    for record in records:
        worksheet.append([record.get(header, '') for header in EXPORT_COLUMNS])

    workbook.save(output_path)


def main():
    nodes = fetch_node_children()
    all_records = []

    for index, node in enumerate(nodes, start=1):
        node_id = node.get('_id')
        node_name = node.get('name', '')
        if not node_id:
            print(f'Skipping item #{index}: missing _id')
            continue

        print(f'[{index}/{len(nodes)}] nodeId={node_id} name={node_name}')
        result = read_records(node_id)
        child_records = result.get('result', {}).get('data', [])

        for child_record in child_records:
            all_records.append(build_export_row(node_name, child_record))

        if index < len(nodes):
            time.sleep(2)

    output_path = Path(__file__).resolve().parent / 'all_read_records.xlsx'
    save_to_excel(all_records, output_path)
    print(f'Saved {len(all_records)} records to: {output_path}')


if __name__ == '__main__':
    main()

