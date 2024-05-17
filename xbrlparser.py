from ixbrlparse import IXBRL
import json
import requests
import io
import warnings

warnings.filterwarnings("ignore")

def add_spaces_to_camel_case(s):
    return ''.join(' ' + i if i.isupper() else i for i in s).strip()

def fetch_ixbrl(url: str) -> IXBRL:
    headers = {
        'User-Agent': 'Benjamin Cole',
        'From': 'info@benjamincole.com'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        xbrl_object = io.BytesIO(response.content)
        ixbrl = IXBRL(xbrl_object)
        return ixbrl
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the iXBRL document: {str(e)}")
        return None

def extract_data_from_ixbrl(ixbrl_object):
    extracted_data = {}

    for item in ixbrl_object.nonnumeric:
        extracted_data[add_spaces_to_camel_case(item.name)] = item.value

    for item in ixbrl_object.numeric:
        extracted_data[add_spaces_to_camel_case(item.name)] = {
            "value": item.value,
            "unit": item.unit
        }

    extracted_text = json.dumps(extracted_data, indent=4)

    return extracted_text

def write_financial_data(url):
    data_to_write = extract_data_from_ixbrl(fetch_ixbrl(url=url))

    with open('reader.txt', 'w') as file:
        file.write(data_to_write)

# url = "https://www.sec.gov/Archives/edgar/data/320193/000032019321000105/aapl-20210925.htm"
# write_financial_data(url=url)