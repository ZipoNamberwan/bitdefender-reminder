import os
import json
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from openpyxl import Workbook

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env', override=True)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# ── Step 1: Login via Selenium and capture the first API request ─────────────

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

driver.get("https://bitgravity.bps.go.id/")

username_input = wait.until(EC.presence_of_element_located((
    By.XPATH,
    "/html/body/div[7]/div[2]/span/div/div/div/div[1]/div[1]/span/div/table[1]/tbody/tr/td[2]/input"
)))
username_input.clear()
username_input.send_keys(USERNAME)

password_input = wait.until(EC.presence_of_element_located((
    By.XPATH,
    "/html/body/div[7]/div[2]/span/div/div/div/div[1]/div[1]/span/div/table[2]/tbody/tr/td[2]/input"
)))
password_input.clear()
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)

TARGET_URL = "https://bitgravity.bps.go.id/webservice/EPS/model?"
ROOT_PARENT_NODE_ID = '6756a8de6e95b9d130037894'
ROOT_PARENT_NODE_NAME = '35_Prov. Jawa Timur'

def wait_for_request(drv, url_pattern, timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        for req in drv.requests:
            if url_pattern in req.url and req.response is not None:
                return req
        time.sleep(0.5)
    raise TimeoutError(f"Request to {url_pattern!r} not found within {timeout}s")

captured = wait_for_request(driver, TARGET_URL)

captured_headers = dict(captured.headers)

parsed = urlparse(captured.url)
csrf_token = parse_qs(parsed.query).get('csrfToken', [''])[0]

selenium_cookies = driver.get_cookies()
driver.quit()

# ── Step 2: Build session from captured headers/cookies ──────────────────────

cookies = {c['name']: c['value'] for c in selenium_cookies}

headers = {
    'accept': captured_headers.get('accept', '*/*'),
    'accept-language': captured_headers.get('accept-language', 'en-US,en;q=0.9,id;q=0.8'),
    'content-type': captured_headers.get('content-type', 'application/json'),
    'origin': captured_headers.get('origin', 'https://bitgravity.bps.go.id'),
    'priority': captured_headers.get('priority', 'u=1, i'),
    'referer': captured_headers.get('referer', 'https://bitgravity.bps.go.id/'),
    'sec-ch-ua': captured_headers.get('sec-ch-ua', ''),
    'sec-ch-ua-mobile': captured_headers.get('sec-ch-ua-mobile', '?0'),
    'sec-ch-ua-platform': captured_headers.get('sec-ch-ua-platform', '"Windows"'),
    'sec-fetch-dest': captured_headers.get('sec-fetch-dest', 'empty'),
    'sec-fetch-mode': captured_headers.get('sec-fetch-mode', 'cors'),
    'sec-fetch-site': captured_headers.get('sec-fetch-site', 'same-origin'),
    'user-agent': captured_headers.get('user-agent', ''),
    'x-requested-with': captured_headers.get('x-requested-with', 'XMLHttpRequest'),
}

params = {
    'csrfToken': csrf_token,
}

# ── Step 3: API calls (from get_node.py) ─────────────────────────────────────

def fetch_node_children():
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


def read_records(node_id, parent_node_name, visited_nodes=None, depth=0):
    if visited_nodes is None:
        visited_nodes = set()

    if node_id in visited_nodes:
        return []
    visited_nodes.add(node_id)

    endpoint_rows = []
    page = 1
    limit = 20

    while True:
        # The first call for the root parent node matches the parent curl (page=1).
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
                'page': page,
                'limit': limit,
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
        body = response.json()
        result = body.get('result', {})
        items = result.get('data', [])
        total = result.get('total', len(items))
        total_pages = max(1, (total + limit - 1) // limit)

        print(
            f"DEBUG pagination node={node_id} name={parent_node_name} page={page}/{total_pages} "
            f"items_on_page={len(items)} total={total}"
        )

        # type 262 is endpoint data, type 261 is child node.
        for item in items:
            item_type = item.get('type')

            if item_type == 262:
                endpoint_rows.append(build_export_row(parent_node_name, item))
                continue

            if item_type == 261:
                child_node_id = item.get('_id')
                child_node_name = item.get('name', parent_node_name)
                if child_node_id:
                    if depth == 0:
                        print(
                            f"DEBUG parent-level type=261 found parent={parent_node_name} "
                            f"child_node_id={child_node_id} child_node_name={child_node_name}"
                        )
                    endpoint_rows.extend(
                        read_records(child_node_id, child_node_name, visited_nodes, depth + 1)
                    )

        if page * limit >= total:
            break
        page += 1

    return endpoint_rows


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


def flatten_record(data, parent_key='', output=None):
    if output is None:
        output = {}

    if not isinstance(data, dict):
        return output

    for key, value in data.items():
        flat_key = f'{parent_key}.{key}' if parent_key else key

        if isinstance(value, dict):
            flatten_record(value, flat_key, output)
            continue

        if isinstance(value, list):
            if all(not isinstance(item, (dict, list)) for item in value):
                output[flat_key] = ', '.join(as_text(item) for item in value)
            else:
                output[flat_key] = json.dumps(value, separators=(',', ':'))
            continue

        output[flat_key] = as_text(value)

    return output


def build_export_row(parent_node_name, child_record):
    row = {'parent_node_name': parent_node_name}
    row.update(flatten_record(child_record if isinstance(child_record, dict) else {}))
    return row


def save_to_excel(records, output_path):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Records'

    all_columns = sorted(
        {key for record in records for key in record.keys() if key != 'parent_node_name'}
    )
    export_columns = ['parent_node_name'] + all_columns

    worksheet.append(export_columns)
    for record in records:
        worksheet.append([record.get(header, '') for header in export_columns])
    workbook.save(output_path)


def main():
    all_records = []
    visited_nodes = set()

    print(
        f'DEBUG parent curl start nodeId={ROOT_PARENT_NODE_ID} '
        f'name={ROOT_PARENT_NODE_NAME} page=1'
    )
    all_records.extend(
        read_records(ROOT_PARENT_NODE_ID, ROOT_PARENT_NODE_NAME, visited_nodes, depth=0)
    )

    output_path = Path(__file__).resolve().parent / 'all_read_records.xlsx'
    save_to_excel(all_records, output_path)
    print(f'Saved {len(all_records)} records to: {output_path}')


if __name__ == '__main__':
    main()
