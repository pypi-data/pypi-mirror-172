'''parser module'''
import json
import re
import logging
from itertools import cycle
from core.logging_utils import LoggingUtils
LOGGR=None

if LOGGR is None:
    LOGGR = LoggingUtils.get_logger()

def set_defaults(args):
    '''set defaults if not detected in incoming json'''
    if 'url' not in args.keys():
        args.update({'url':''})
    if 'verbosity' not in args.keys():
        args.update({'verbosity':'false'})


def url_validation(url):
    '''validate url patterns'''
    # pylint: disable=anomalous-backslash-in-string
    if '/?o=' in url:
        # if the workspace_id exists, lets remove it from the URL
        url = re.sub("\/\?o=.*", '', url)
    elif 'net/' == url[-4:]:
        url = url[:-1]
    elif 'com/' == url[-4:]:
        url = url[:-1]
    return url.rstrip("/")
    # pylint: enable=anomalous-backslash-in-string



#DEBUG < INFO < WARNING < ERROR < CRITICAL
# pylint: disable=multiple-statements
def get_log_level(vloglevel):
    '''get log level that is set'''
    vloglevel=vloglevel.upper()
    if vloglevel == "DEBUG": return logging.DEBUG
    elif vloglevel == "INFO": return logging.INFO
    elif vloglevel == "WARNING": return logging.WARNING
    elif vloglevel == "ERROR": return logging.ERROR
    elif vloglevel == "CRITICAL": return logging.CRITICAL
# pylint: enable=multiple-statements


def str2bool(vinput):
    '''convert string to bool'''
    return vinput.lower() in ("yes", "true", "t", "1")

# Dummy values for account_id and clusterid
# {"account_id":"0123456-e659-4e8c-b108-126b3ac3d0ab", "export_db": "logs", "verify_ssl": "False", "verbosity":"info",
#   "clusterid":"01234-120418-34fw1eab","master_name_scope":"swat_masterscp",
#   "master_name_key":"user", "master_pwd_scope":"swat_masterscp", "master_pwd_key":"pass",
#       "workspace_pat_scope":"swat_masterscp",  "workspace_pat_token":"sat_token" }
def parse_input_jsonargs(jsonargs, workspace_id):
    '''parse and validate incoming json string and return json'''
    inp_configs = simple_sat_fn(jsonargs, workspace_id)
    inp_configs =json.loads(inp_configs)
    set_defaults(inp_configs)
    url = url_validation(inp_configs['url'])
    inp_configs.update({'url':url})
    inp_configs.update({'verbosity':get_log_level(inp_configs['verbosity'])})
    LoggingUtils.loglevel=inp_configs['verbosity'] #update class variable
    ## validate values are present
    if inp_configs['account_id'] == '':
        raise ValueError('Account ID cannot be empty')
    if inp_configs['clusterid'] == '':
        raise ValueError('Cluster ID cannot be empty')
    if inp_configs['mastername'] == '':
        raise ValueError('Master name cannot be empty')
    if inp_configs['masterpwd'] == '':
        raise ValueError('Master pwd cannot be empty')
    if inp_configs['token'] == '':
        raise ValueError('Pass valid Token')
    return inp_configs


def simple_sat_fn(message:str, key:str) -> str:
    """
    Encrypt
    :param message:
        plaintext or cipher text.
    :param cipher_key:
        key chosen by create_key function.
    :return:
        return a string either cipher text or plain text.
    """
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(message, cycle(key)))


def get_decrypted_json_key(obscured: str, key:str, workspace_id:str) -> str:
    '''get decrypted json'''
    inp_configs = simple_sat_fn(obscured, workspace_id)
    jsonobj = json.loads(inp_configs)
    return jsonobj[key]
