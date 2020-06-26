import base64
from dotenv import load_dotenv
import hmac
import hashlib
import os
from os.path import join, dirname
import requests
import time
from urllib import parse
import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_version = '2015-01'
sas_name = 'RootManageSharedAccessKey'
sas_value = os.getenv("SAS_VALUE")
nh_hostname = os.getenv("NH_HOSTNAME")
nh_name = os.getenv("NH_NAME")
outdir = os.getenv("OUT_DIR", "out")


def generate_sas_token(uri, sas_name, sas_value):
    target_uri = parse.quote_plus(uri)
    sas = sas_value.encode('utf-8')
    expiry = str(int(time.time() + 10000))
    string_to_sign = (target_uri + '\n' + expiry).encode('utf-8')
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature = parse.quote(base64.b64encode(signed_hmac_sha256.digest()))
    return 'SharedAccessSignature sr={}&sig={}&se={}&skn={}' \
                     .format(target_uri, signature, expiry, sas_name)

def get_uri(next_token=None):
    if next_token:
        return 'https://{0}/{1}/registrations/?continuationToken={2}&api-version={3}'.format(
            nh_hostname,
            nh_name,
            token,
            api_version,
        )
    return 'https://{0}/{1}/registrations/?api-version={2}'.format(
        nh_hostname,
        nh_name,
        api_version
    )

def save_registrations(uri, continuationToken=None):
    """
    Get the 100 regisration chunk and save it to the file system.
    uri: url to call and get the registrations
    continuationToken: token to add in query and get values.
    retunt: the next token to use for the next call.
    """

    x = datetime.datetime.now()
    file_name = os.path.join(outdir, "devices_{0}.xml".format(x.strftime("%Y-%m-%d-%H%M%S")))
    r = requests.get(uri, headers=headers)

    with open(file_name, 'w') as file:
        file.write(r.text)

    return r.headers.get('x-ms-continuationtoken')



if __name__ == "__main__":

    uri = get_uri()
    sas_token = generate_sas_token(uri, sas_name, sas_value)

    headers = {
        'Authorization':sas_token,
        'x-ms-version':api_version
    }

    print("Start")
    token = next_token = None

    next_token = save_registrations(uri, token)

    while next_token != token:
        time.sleep(2)
        token = next_token
        uri = get_uri(token)

        next_token = save_registrations(uri, token)

    print("End")
