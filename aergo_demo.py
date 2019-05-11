# -*- coding: utf-8 -*-

import sys
import time
import json
import toml
import aergo.herapy as herapy
import string
import random

from aergo.herapy.utils import get_hash, encode_b58

from flask import Flask, jsonify, request
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)

# enable CORS
CORS(app)

"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
"""

AERGO_ENDPOINT = "localhost:7845"
DEMO_SC_ADDRESS = ""
AERGO_WAITING_TIME = 3

aergo_mainnet = herapy.Aergo()
#aergo_mainnet.connect("localhost:7845")
#aergo_mainnet.connect("testnet-api.aergo.io:7845")
aergo_mainnet.connect("mainnet-api.aergo.io:7845")
SC_MAINNET_VERSION = "0.0.1"
SC_MAINNET_PAYLOAD = "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"
SC_MAINNET_ADDRESS = "AmgLrBJVojSWmjgqbFE97T3dApzC1THUQzbgZMLXExJwsobvLETi"

#SC_SQLTESTNET_ENDPOINT = "localhost:7845"
SC_SQLTESTNET_ENDPOINT = "sqltestnet-api.aergo.io:7845"
SC_SQLTESTNET_VERSION = "0.0.1"
SC_SQLTESTNET_PAYLOAD = "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"
SC_SQLTESTNET_ADDRESS = "AmhVt9arVQTfjARs5MN8ASMt3r5K14WV7ii1PPooBtFy5GvEHsbt"


AERGO_CONN_DICT = {}


def get_dict_value(d, k):
    if d is None:
        return None
    if k is None:
        return None
    if k not in d:
        return None
    else:
        return d[k]


def get_random_string(length=20, with_number=True, with_punctuation=False):
    letters = string.ascii_letters
    if with_number:
        letters += string.digits
    if with_punctuation:
        letters += string.punctuation

    return ''.join(random.choice(letters) for i in range(length))


def err_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def deploy_sc(aergo, payload, args=None):
    # send TX
    tx, result = aergo.deploy_sc(payload=payload, args=args)
    if result.status != herapy.CommitStatus.TX_OK:
        raise RuntimeError("[{0}]: {1}".format(result.status, result.detail))

    time.sleep(int(AERGO_WAITING_TIME))

    # check TX
    result = aergo.get_tx_result(tx.tx_hash)
    if result.status != herapy.TxResultStatus.CREATED:
        raise RuntimeError("[{0}]:{1}: {2}".format(result.contract_address, result.status, result.detail))

    return result.contract_address


def call_sc(aergo, hsc_address, func_name, args=None):
    # send TX
    tx, result = aergo.call_sc(hsc_address, func_name, args=args)
    if result.status != herapy.CommitStatus.TX_OK:
        raise RuntimeError("[{0}]: {1}".format(result.status, result.detail))

    """
    time.sleep(int(AERGO_WAITING_TIME))

    # check TX
    result = aergo.get_tx_result(tx.tx_hash)
    if result.status != herapy.TxResultStatus.SUCCESS:
        err_print(result)
        raise RuntimeError("[{0}]:{1}: {2}".format(result.contract_address, result.status, result.detail))

    return result
    """
    return tx


def query_sc(aergo, hsc_address, func_name, args=None):
    # send TX
    result = aergo.query_sc(hsc_address, func_name, args=args)
    return result


def add_new_user(username, password, metadata, recovery_key):
    print("add_new_user")

    aergo = herapy.Aergo()

    aergo.connect(SC_SQLTESTNET_ENDPOINT)
    aergo.new_account()
    address = str(aergo.account.address)
    print(address)

    # check username exists
    user_info = get_user_info2(aergo, username)
    if "address" in user_info:
        if user_info["address"] == address:
            raise RuntimeError("user already exists")
        else:
            raise RuntimeError("username already exists")

    # check address exists
    if "tx_hash" in get_user_info(aergo, address):
        raise ValueError("user already exists")

    # store user info into SqlTestNet
    tx_hash = None
    try:
        metadata_str = json.dumps(metadata)
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "addNewUser",
                     args=[username, metadata_str])
        tx_hash = str(tx.tx_hash)
    except Exception as e:
        err_print(e)
        raise e

    # store recovery key
    if recovery_key is not None:
        try:
            enc_key = aergo.export_account(password=recovery_key)
            call_sc(aergo, SC_SQLTESTNET_ADDRESS, "addRecoveryKey", [enc_key])
        except Exception as e:
            err_print(e)
            raise e

    # add new user in MainNet
    try:
        call_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "addNewUser",
                args=[address, tx_hash])
    except Exception as e:
        err_print(e)
        raise e

    aergo.disconnect()
    return aergo.export_account(password=password)


def get_user_info(aergo, address):
    print("get_user_info")
    result = query_sc(aergo, SC_SQLTESTNET_ADDRESS, "getUserInfo", [address])
    return json.loads(result)


def get_user_info2(aergo, username):
    print("get_user_info2")
    result = query_sc(aergo, SC_SQLTESTNET_ADDRESS, "getUserInfo2", [username])
    return json.loads(result)


def get_user_fingerprint(address):
    print("get_user_fingerprint")
    result = query_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "getUserInfo", [address])
    return json.loads(result)


def create_cert(aergo):
    print("create_cert")

    address = str(aergo.account.address)
    print(address)

    # request to create new cert to SqlTestNet
    try:
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "createCert")

        cert = None
        for _ in range(20):
            # try max 10 seconds
            time.sleep(0.5)

            events = aergo.get_events(SC_SQLTESTNET_ADDRESS, "cert",
                                      with_desc=True,
                                      arg_filter={0 : 'create',
                                                  1 : str(tx.tx_hash)})
            for i, e in enumerate(events):
                cert = e.arguments[3]
                break

            if cert is not None:
                break
    except Exception as e:
        err_print(e)
        raise e

    if cert is None:
        raise RuntimeError("fail to create new certificate")

    # store new cert hash in MainNet
    try:
        cert_hash = get_hash(json.dumps(cert), no_rand=True)
        call_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "registerNewCertHash",
                args=[address, str(tx.tx_hash), cert_hash])
    except Exception as e:
        err_print(e)
        raise e

    return cert


def get_user_cert(aergo):
    print("get_user_cert")

    try:
        proof = get_random_string()
        proof_hash = get_hash(proof, no_rand=True, no_encode=True)
        sign = aergo.account.private_key.sign_msg(proof_hash)
        sign = '0x' + sign.hex()

        result = query_sc(aergo, SC_SQLTESTNET_ADDRESS, "getUserCert",
                          args=[proof, sign, str(aergo.account.address)])
    except Exception as e:
        err_print(e)
        raise e

    return json.loads(result)


def judge_1on1_contract_status(address, contract):
    iss_addr = get_dict_value(contract, 'issuer')
    rcv_addr = get_dict_value(contract, 'receiver')

    iss_sign = get_dict_value(contract, 'issuer_sign')
    rcv_sign = get_dict_value(contract, 'receiver_sign')

    if address == iss_addr:
        if 'CANCEL' == iss_sign:
            # user canceled the contract
            status = 'CANCELED'
        else:
            if 'DISAGREE' == rcv_sign:
                # receiver disagree the contract
                status = 'DISAGREED'
            elif rcv_sign is not None:
                # receiver agreed and signed the contract
                status = 'AGREED'
            else:
                # user waiting receiver's reaction
                status = 'ISSUED'
    elif address == rcv_addr:
        if 'DISAGREE' == rcv_sign:
            # user disagreed the contract
            status = 'REFUSED'
        else:
            if 'CANCEL' == iss_sign:
                # issuer canceled the contract
                status = 'DISCARDED'
            elif rcv_sign is not None:
                # user signed the contract
                status = 'SIGNED'
            else:
                # issuer waiting user's reaction
                status = 'OPENED'
    else:
        raise RuntimeError("not allowed to see the contract")

    return status


def get_1on1_contract(aergo, contract_id):
    print("get_1on1_contract")
    contract = query_sc(aergo, SC_SQLTESTNET_ADDRESS,
                        "get1on1Contract", args=[contract_id])
    contract = json.loads(contract)

    address = str(aergo.account.address)
    print(address)

    contract['status'] = judge_1on1_contract_status(address, contract)

    return contract


def disagree_1on1_contract(aergo, contract_id):
    print("disagree_1on1_contract")

    address = str(aergo.account.address)
    print(address)

    # set disagree to the contract in SqlTestNet
    try:
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "disagree1on1Contract",
                     args=[contract_id])
        contract_id = str(tx.tx_hash)
        status_code = 0
        err_msg = ""
        for _ in range(20):
            # try max 10 seconds
            time.sleep(0.5)

            events = aergo.get_events(SC_SQLTESTNET_ADDRESS, "contract",
                                      with_desc=True,
                                      arg_filter={0 : 'disagree',
                                                  1 : contract_id})
            for i, e in enumerate(events):
                status_code = e.arguments[2]
                err_msg = e.arguments[3]
                break

            if status_code is not 0:
                break
    except Exception as e:
        err_print(e)
        raise e

    if status_code != 201:
        raise RuntimeError(err_msg)

    return {
        "contract_id": contract_id,
    }


def cancel_1on1_contract(aergo, contract_id):
    print("cancel_1on1_contract")

    address = str(aergo.account.address)
    print(address)

    # set cancel to the contract in SqlTestNet
    try:
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "cancel1on1Contract",
                     args=[contract_id])
        contract_id = str(tx.tx_hash)
        status_code = 0
        err_msg = ""
        for _ in range(20):
            # try max 10 seconds
            time.sleep(0.5)

            events = aergo.get_events(SC_SQLTESTNET_ADDRESS, "contract",
                                      with_desc=True,
                                      arg_filter={0 : 'cancel',
                                                  1 : contract_id})
            for i, e in enumerate(events):
                status_code = e.arguments[2]
                err_msg = e.arguments[3]
                break

            if status_code is not 0:
                break
    except Exception as e:
        err_print(e)
        raise e

    if status_code != 201:
        raise RuntimeError(err_msg)

    return {
        "contract_id": contract_id,
    }


def issue_1on1_contract(aergo, rcv_addr, contents):
    print("issue_1on1_contract")

    address = str(aergo.account.address)
    print(address)

    if contents is not None:
        contract_raw = "{}{}{}".format(address, rcv_addr, contents)
    else:
        contract_raw = "{}{}".format(address, rcv_addr)

    contract_hash = get_hash(contract_raw, no_rand=True, no_encode=True)
    sign = aergo.account.private_key.sign_msg(contract_hash)
    sign = '0x' + sign.hex()

    # store new contract to SqlTestNet
    try:
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "addNew1on1Contract",
                     args=[sign, rcv_addr, contents])
        contract_id = str(tx.tx_hash)
        status_code = 0
        err_msg = ""
        for _ in range(20):
            # try max 10 seconds
            time.sleep(0.5)

            events = aergo.get_events(SC_SQLTESTNET_ADDRESS, "contract",
                                      with_desc=True,
                                      arg_filter={0 : 'new',
                                                  1 : contract_id})
            for i, e in enumerate(events):
                status_code = e.arguments[2]
                err_msg = e.arguments[3]
                break

            if status_code is not 0:
                break
    except Exception as e:
        err_print(e)
        raise e

    if status_code != 201:
        raise RuntimeError(err_msg)

    return {
        "contract_id": contract_id,
        "issuer_sign": sign,
    }


def sign_1on1_contract(aergo, contract_id):
    print("sign_1on1_contract")

    address = str(aergo.account.address)
    print(address)

    contract = get_1on1_contract(aergo, contract_id)

    if 'issuer' not in contract:
        raise RuntimeError("cannot find the contract")

    iss_addr = get_dict_value(contract, 'issuer')
    rcv_addr = get_dict_value(contract, 'receiver')
    contents = get_dict_value(contract, 'contents')

    if rcv_addr != address:
        raise RuntimeError("only receiver can agree the contract")

    if contents is not None:
        contract_raw = "{}{}{}".format(iss_addr, rcv_addr, contents)
    else:
        contract_raw = "{}{}".format(iss_addr, rcv_addr)

    contract_hash = get_hash(contract_raw, no_rand=True, no_encode=True)
    sign = aergo.account.private_key.sign_msg(contract_hash)
    sign = '0x' + sign.hex()

    # store new contract to SqlTestNet
    try:
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "sign1on1Contract",
                     args=[contract_id, sign])

        status_code = 0
        err_msg = None
        for _ in range(20):
            # try max 10 seconds
            time.sleep(0.5)

            events = aergo.get_events(SC_SQLTESTNET_ADDRESS, "contract",
                                      with_desc=True,
                                      arg_filter={0 : 'sign',
                                                  1 : str(tx.tx_hash)})
            for i, e in enumerate(events):
                status_code = e.arguments[2]
                err_msg = e.arguments[3]
                break

            if status_code is not 0:
                break
    except Exception as e:
        err_print(e)
        raise e

    if status_code != 201:
        raise RuntimeError(err_msg)
    else:
        contract = err_msg

    # store final contract in MainNet
    try:
        contract_hash = get_hash(json.dumps(contract), no_rand=True)
        call_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "register1on1Contract",
                args=[iss_addr, rcv_addr,
                      contract_id, encode_b58(contract_hash)])
    except Exception as e:
        err_print(e)
        raise e

    return contract


def get_all_1on1_contract(aergo, address):
    print("get_all_1on1_contract")

    contracts = {}

    # all issued contracts
    issued_contracts = query_sc(aergo, SC_SQLTESTNET_ADDRESS,
                                "getAllIssued1on1Contract", args=[address])
    issued_contracts = json.loads(issued_contracts)
    print(json.dumps(issued_contracts, indent=2))

    if len(issued_contracts) > 0:
        for c in issued_contracts:
            c['status'] = judge_1on1_contract_status(address, c)
            contracts[c['contract_id']] = c

    # all received contracts
    received_contracts = query_sc(aergo, SC_SQLTESTNET_ADDRESS,
                                  "getAllReceived1on1Contract", args=[address])
    received_contracts = json.loads(received_contracts)
    print(json.dumps(received_contracts, indent=2))

    if len(received_contracts) > 0:
        for c in received_contracts:
            c['status'] = judge_1on1_contract_status(address, c)
            contracts[c['contract_id']] = c

    contracts = sorted(contracts.values(), key=lambda item: item['block_no'],
                       reverse=True)

    return contracts


def check_user_cert(aergo):
    cert = get_user_cert(aergo)

    _, block_no = aergo.get_blockchain_status()

    # check expire
    if cert['expire_after'] < (block_no - cert['block_no']):
        aergo.disconnect()
        AERGO_CONN_DICT.pop(str(aergo.account.address))
        raise RuntimeError("the user certificate is expired")

    return cert


@app.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    """
    root path
    """
    print("index")
    return jsonify('Hello AERGO World!')


@app.route('/profile2/<username>', methods=['POST'])
def profile2(username):
    print("call profile2")

    # TODO create certificate using AERGO mainnet

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        user = get_user_info2(aergo, username)
        return jsonify(user)
    except Exception as e:
        err_print(e)
        raise RuntimeError("fail to get the user info: {}".format(e))


@app.route('/profile/<address>', methods=['POST'])
def profile(address):
    print("call profile")

    # TODO create certificate using AERGO mainnet

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        user = get_user_info(aergo, address)
        return jsonify(user)
    except Exception as e:
        err_print(e)
        raise RuntimeError("fail to get the user info: {}".format(e))


@app.route('/login', methods=['POST'])
def login():
    print("call login")

    try:
        payload = request.data
        payload = json.loads(payload)
        enc_key = payload['enc_key']
        password = payload['password']

        # TODO create certificate using AERGO mainnet
        aergo = herapy.Aergo()
        aergo.connect(SC_SQLTESTNET_ENDPOINT)
        aergo.import_account(exported_data=enc_key,
                             password=password)
        address = str(aergo.account.address)

        cert = None
        if address in AERGO_CONN_DICT:
            aergo.disconnect()
            aergo = AERGO_CONN_DICT[address]

            # check certificate and re-issue
            try:
                cert = check_user_cert(aergo)
            except:
                pass
        else:
            AERGO_CONN_DICT[address] = aergo

        if cert is None:
            # check user available
            user = get_user_info(aergo, address)
            if 'block_no' not in user:
                raise RuntimeError('user does not exists')

            cert = create_cert(aergo)

        return jsonify(cert)
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to login: {}".format(e)
        })


@app.route('/signup', methods=['POST'])
def signup():
    print("call signup")

    try:
        payload = request.data
        payload = json.loads(payload)
        username = payload['username']
        user_email = payload['userEmail']
        password = payload['password']
        image_data_hash = payload['imageDataHash']

        enc_key = add_new_user(username, password, metadata={
            'username': username,
            'email': user_email,
        }, recovery_key=image_data_hash)

        # TODO register new user in AERGO sidechain to avoid GDPR

        return jsonify({
            "encrypted_key": enc_key
        })
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to signup: {}".format(e)
        })


@app.route('/newcontract/<contract_type>', methods=['POST'])
def issue_contract(contract_type):
    print("call issue_contracts")

    payload = request.data
    payload = json.loads(payload)
    # issuer
    user_address = payload['issuer']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        if contract_type == "1on1":
            # contractor
            rcv_addr = payload['receiver']
            contents = payload['contents']
            result = issue_1on1_contract(aergo, rcv_addr, contents)
            return jsonify(result)
        else:
            raise RuntimeError("not supported contract type: {}".format(contract_type))
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to issue new contract: {}".format(e)
        })


@app.route('/contract/<contract_id>', methods=['POST'])
def get_contract(contract_id):
    print("call get_contract")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        contract = get_1on1_contract(aergo, contract_id)
        return jsonify(contract)
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to get contracts: {}".format(e)
        })


@app.route('/contracts/<address>', methods=['POST'])
def get_contracts(address):
    print("call get_contracts")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        contracts = get_all_1on1_contract(aergo, address)
        return jsonify(contracts)
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to get contracts: {}".format(e)
        })


@app.route('/cancel/<contract_id>', methods=['POST'])
def cancel_contract(contract_id):
    print("call cancel_contract")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        result = cancel_1on1_contract(aergo, contract_id)
        return jsonify(result)
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to cancel contracts: {}".format(e)
        })


@app.route('/agree/<contract_id>', methods=['POST'])
def agree_contract(contract_id):
    print("call agree_contract")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        result = sign_1on1_contract(aergo, contract_id)
        return jsonify(result)
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to disagree contracts: {}".format(e)
        })


@app.route('/disagree/<contract_id>', methods=['POST'])
def disagree_contract(contract_id):
    print("call disagree_contract")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        result = disagree_1on1_contract(aergo, contract_id)
        return jsonify(result)
    except Exception as e:
        err_print(e)
        return jsonify({
            "error_msg": "fail to disagree contracts: {}".format(e)
        })


if __name__ == '__main__':
    try:
        conf_file = sys.argv[1]
        with open(conf_file, 'r') as f:
            conf = toml.load(f)

        print(json.dumps(conf, indent=2))
    except Exception as e:
        err_print("cannot run without conf file")
        raise e

    # init account for MainNet
    try:
        aergo_mainnet.import_account(exported_data=conf['mainnet']['exported_key'],
                                     password=conf['mainnet']['password'])
        aergo_mainnet.get_account()
        print("MainNet Demo Address: {}".format(str(aergo_mainnet.account.address)))
    except Exception as e:
        err_print("cannot run without MainNet account")
        raise e

    # check MainNet SC
    try:
        # check a version of the deployed SC
        version = query_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "getVersion")
        version = json.loads(version)
        print("MainNet SC Version: {}".format(version))

        if version != SC_MAINNET_VERSION:
            print("Version is different. Redeploy SC.")
            SC_MAINNET_ADDRESS = deploy_sc(aergo_mainnet, SC_MAINNET_PAYLOAD)
            aergo_mainnet.account.nonce += 1
        else:
            pass
    except:
        # not exists, deploy
        print("Cannot find MainNet SC. Deploy SC.")
        SC_MAINNET_ADDRESS = deploy_sc(aergo_mainnet, SC_MAINNET_PAYLOAD)
        aergo_mainnet.account.nonce += 1

    print("MainNet SC Address: {}".format(SC_MAINNET_ADDRESS))

    aergo = herapy.Aergo()

    # init account for SqlTestNet
    try:
        aergo.connect(SC_SQLTESTNET_ENDPOINT)
        aergo.import_account(exported_data=conf['sqltestnet']['exported_key'],
                             password=conf['sqltestnet']['password'])
        aergo.get_account()
        print("SqlTestNet Demo Address: {}".format(str(aergo.account.address)))
    except Exception as e:
        err_print("cannot run without SqlTestNet account")
        raise e

    # check SqlTestNet SC
    try:
        # check a version of the deployed SC
        version = query_sc(aergo, SC_SQLTESTNET_ADDRESS, "getVersion")
        version = json.loads(version)
        print("SqlTestNet SC Version: {}".format(version))

        if version != SC_SQLTESTNET_VERSION:
            print("Version is different. Redeploy SC.")
            SC_SQLTESTNET_ADDRESS = deploy_sc(aergo, SC_SQLTESTNET_PAYLOAD)
        else:
            pass
    except:
        # not exists, deploy
        print("Cannot find SqlTestNet SC. Deploy SC.")
        SC_SQLTESTNET_ADDRESS = deploy_sc(aergo, SC_SQLTESTNET_PAYLOAD)

    print("SqlTestNet SC Address: {}".format(SC_SQLTESTNET_ADDRESS))
    aergo.disconnect()

    """
    # TODO remove test below
    enc_key = add_new_user("1234", {"email": "test@blocko.io", "name": "yp", "is_test": True}, "recovery_key")

    time.sleep(3)

    aergo.connect(SC_SQLTESTNET_ENDPOINT)
    aergo.import_account(enc_key, "1234")

    fingerprint = get_user_fingerprint(str(aergo.account.address))
    print("fingerprint = {}".format(json.dumps(fingerprint, indent=2)))

    # login
    cert = create_cert(aergo)
    print(json.dumps(cert, indent=2))
    user = get_user_info(aergo, str(aergo.account.address))
    print(json.dumps(user, indent=2))

    time.sleep(3)

    fingerprint = get_user_fingerprint(str(aergo.account.address))
    print("fingerprint = {}".format(json.dumps(fingerprint, indent=2)))

    contract_id = issue_1on1_contract(aergo, str(aergo.account.address), "contract123")

    time.sleep(3)

    # get all contracts
    get_all_1on1_contract(aergo)

    # sign the received contract
    sign_1on1_contract(aergo, contract_id)

    time.sleep(3)

    # get all contracts
    get_all_1on1_contract(aergo)

    fingerprint = get_user_fingerprint(str(aergo.account.address))
    print("fingerprint = {}".format(json.dumps(fingerprint, indent=2)))

    sys.exit(0)
    """

    app.run(host="0.0.0.0", port=5000)
