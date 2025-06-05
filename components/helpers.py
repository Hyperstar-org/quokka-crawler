import json
from typing import Optional

import httpx
import logging

import requests
from lxml.html import fromstring

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('apify_client')


async def get_request_data_async(url, **kwargs):
    headers = kwargs.get('headers', {})
    params = kwargs.get('params', {})
    cookies = kwargs.get('cookies', {})

    async with httpx.AsyncClient(headers=headers, cookies=cookies) as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                logger.info(f"Returning data for url: {url}")
                return response.text
            else:
                logger.info(f"Unable to get data for url. Status {response.status_code}")
                return None
        except httpx.HTTPError as e:
            logger.info(f"Unable to get data for url. Error {e}")
            return None

def get_request_data_sync(url, **kwargs):
    headers = kwargs.get('headers', {})
    params = kwargs.get('params', {})
    cookies = kwargs.get('cookies', {})

    try:
        response = requests.get(url, headers=headers, params=params, cookies=cookies)
        if response.status_code == 200:
            data = response.text
            logger.info(f"Returning data for url: {url}")
            return data
        else:
            logger.info(f"Unable to get data for url. Status {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.info(f"Unable to get data for url. Error {e}")
        return None

def input_data_to_api(url, **kwargs):
    headers = kwargs.get('headers', {})
    params = kwargs.get('params', {})
    cookies = kwargs.get('cookies', {})
    json_data = kwargs.get('json', {})

    try:
        response = requests.post(url, headers=headers, params=params, cookies=cookies,
                                json=json_data)
        if response.status_code == 200:
            data = response.text
            logger.info(f"Returning data for url: {url}")
            return data
        elif response.status_code == 422:
            i = 0
        else:
            logger.info(f"Unable to get data for url. Status {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.info(f"Unable to get data for url. Error {e}")
        return None

def extract_xpath_data(response_text:str, xpath, _list=False):
    tree = fromstring(response_text)
    try:
        if _list:
            return list(set(tree.xpath(xpath)))
        return tree.xpath(xpath)[0]
    except Exception as e:
        logger.error(f"Failed to extract xpath. Error {e}")

def extract_json_data(response_text: str, sub: str) -> Optional[dict]:
    try:
        text = response_text.replace(sub, "").strip()
        data = json.loads(text)
    except:
        logger.error("Unable to extract website of the club.")
        return None
    return data

