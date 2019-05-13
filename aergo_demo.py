# -*- coding: utf-8 -*-

import sys
import time
import json
import toml
import aergo.herapy as herapy
import string
import random
import traceback

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

AERGO_WAITING_TIME = 3
AERGO_CONF = {}
AERGO_CONN_DICT = {}
AERGO_IS_DEBUG = False

SC_MAINNET_VERSION = "0.0.1"
SC_MAINNET_PAYLOAD = "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"
SC_MAINNET_ADDRESS = "AmgSN4dWHuADYmo67dj7CUPoAiAyFYZ91nE3673DfSHGiuTzTXge"

DEBUG_SC_SQLTESTNET_ENDPOINT = "localhost:7845"
SC_SQLTESTNET_ENDPOINT = "sqltestnet-api.aergo.io:7845"
#SC_SQLTESTNET_ENDPOINT = "sql1.aergo.io:7845"
#SC_SQLTESTNET_ENDPOINT = "sql2.aergo.io:7845"
#SC_SQLTESTNET_ENDPOINT = "sql3.aergo.io:7845"
SC_SQLTESTNET_VERSION = "0.0.1"
SC_SQLTESTNET_PAYLOAD = "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"
SC_SQLTESTNET_ADDRESS = "AmgRM3DdnK2gu1kPS3QGnpkcn1wdpm5SqdauXjJmBYfByjxN9chd"


def conn_mainnet():
    aergo_mainnet = herapy.Aergo()
    if AERGO_IS_DEBUG:
        aergo_mainnet.connect("localhost:7845")
    else:
        # SqlTestNet
        #aergo_mainnet.connect("sql1.aergo.io:7845")
        #aergo_mainnet.connect("sql2.aergo.io:7845")
        #aergo_mainnet.connect("sql3.aergo.io:7845")
        # TestNet
        #aergo_mainnet.connect("testnet-api.aergo.io:7845")
        #aergo_mainnet.connect("testnet-node1.aergo.io:7845")
        #aergo_mainnet.connect("testnet-node2.aergo.io:7845")
        #aergo_mainnet.connect("13.209.189.119:7845")
        # MainNet
        aergo_mainnet.connect("mainnet-api.aergo.io:7845")
        #aergo_mainnet.connect("mainnet-node1.aergo.io:7845")
        #aergo_mainnet.connect("mainnet-node2.aergo.io:7845")
        #aergo_mainnet.connect("mainnet-node3.aergo.io:7845")

    # init account for MainNet
    try:
        aergo_mainnet.import_account(exported_data=AERGO_CONF['mainnet']['exported_key'],
                                     password=AERGO_CONF['mainnet']['password'])
        aergo_mainnet.get_account()
        print("---------------------------")
        print("MainNet Account Address: {}".format(str(aergo_mainnet.account.address)))
        print("---------------------------")
    except Exception as e:
        traceback.print_exc()
        raise e

    return aergo_mainnet


def cached_conn(addr):
    print("cached_conn")
    try:
        aergo = AERGO_CONN_DICT[addr]
    except:
        return None

    retry_conn = 1
    is_fail_conn = True
    while retry_conn > 0:
        try:
            aergo.get_account()
            is_fail_conn = False
            break
        except:
            retry_conn -= 1

    if is_fail_conn:
        raise RuntimeError("cannot connect to SQL TestNet")

    return aergo


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
    print(str(tx.tx_hash))

    # check TX
    result = aergo.get_tx_result(tx.tx_hash)
    if result.status != herapy.TxResultStatus.SUCCESS:
        err_print(result)
        raise RuntimeError("[{0}]:{1}: {2}".format(result.contract_address, result.status, result.detail))
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
    try:
        metadata_str = json.dumps(metadata)
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "addNewUser",
                     args=[username, metadata_str])
        s_tx_hash = str(tx.tx_hash)
    except Exception as e:
        traceback.print_exc()
        raise e

    # store recovery key
    if recovery_key is not None:
        try:
            enc_key = aergo.export_account(password=recovery_key)
            call_sc(aergo, SC_SQLTESTNET_ADDRESS, "addRecoveryKey", [enc_key])
        except Exception as e:
            traceback.print_exc()
            raise e

    # add new user in MainNet
    try:
        aergo_mainnet = conn_mainnet()
        tx = call_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "addNewUser",
                     args=[address, s_tx_hash])
        m_tx_hash = str(tx.tx_hash)
    except Exception as e:
        traceback.print_exc()
        raise e

    aergo.disconnect()
    enc_key = aergo.export_account(password=password)

    return {
        "address": address,
        "encrypted_key": enc_key,
        "s_tx_hash": s_tx_hash,
        "m_tx_hash": m_tx_hash,
    }


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
    aergo_mainnet = conn_mainnet()
    result = query_sc(aergo_mainnet, SC_MAINNET_ADDRESS,
                      "getUserInfo", [address])
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
        traceback.print_exc()
        raise e

    if cert is None:
        raise RuntimeError("fail to create new certificate")

    # store new cert hash in MainNet
    try:
        cert_hash = get_hash(json.dumps(cert), no_rand=True)
        aergo_mainnet = conn_mainnet()
        call_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "registerNewCertHash",
                args=[address, str(tx.tx_hash), cert_hash])
    except Exception as e:
        traceback.print_exc()
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
        traceback.print_exc()
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
                status = 'REFUSED'
            elif rcv_sign is not None:
                # receiver agreed and signed the contract
                status = 'SIGNED'
            else:
                # user waiting receiver's reaction
                status = 'ISSUED'
    elif address == rcv_addr:
        if 'DISAGREE' == rcv_sign:
            # user disagreed the contract
            status = 'DISAGREED'
        else:
            if 'CANCEL' == iss_sign:
                # issuer canceled the contract
                status = 'DISCARDED'
            elif rcv_sign is not None:
                # user signed the contract
                status = 'AGREED'
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
        traceback.print_exc()
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
        traceback.print_exc()
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
        traceback.print_exc()
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
        traceback.print_exc()
        raise e

    if status_code != 201:
        raise RuntimeError(err_msg)
    else:
        contract = err_msg

    # store final contract in MainNet
    try:
        contract_hash = get_hash(json.dumps(contract), no_rand=True)
        aergo_mainnet = conn_mainnet()
        call_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "register1on1Contract",
                args=[iss_addr, rcv_addr,
                      contract_id, encode_b58(contract_hash)])
    except Exception as e:
        traceback.print_exc()
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
    if aergo is None:
        raise ValueError("need AERGO account first")

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

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = cached_conn(user_address)
        check_user_cert(aergo)
        user = get_user_info2(aergo, username)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to get the user info: {}".format(e)
        })


@app.route('/accproof', methods=['POST'])
def account_proof():
    print("call account_proof")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = cached_conn(user_address)
        check_user_cert(aergo)
        result = get_user_fingerprint(user_address)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to get the user info: {}".format(e)
        })


@app.route('/profile/<address>', methods=['POST'])
def profile(address):
    print("call profile")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = cached_conn(user_address)
        check_user_cert(aergo)
        user = get_user_info(aergo, address)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to get the user info: {}".format(e)
        })


@app.route('/login', methods=['POST'])
def login():
    print("call login")

    try:
        payload = request.data
        payload = json.loads(payload)
        enc_key = payload['enc_key']
        password = payload['password']

        aergo = herapy.Aergo()
        aergo.import_account(exported_data=enc_key,
                             password=password,
                             skip_state=True)
        address = str(aergo.account.address)

        cert = None
        cached_aergo = cached_conn(address)
        if cached_aergo:
            try:
                aergo = cached_aergo
                cert = check_user_cert(aergo)
            except:
                print("yes account, no cert")
                pass
        else:
            aergo.connect(SC_SQLTESTNET_ENDPOINT)
            aergo.get_account()
            AERGO_CONN_DICT[address] = aergo

        if cert is None:
            # check user available
            user = get_user_info(aergo, address)
            if 'block_no' not in user:
                raise RuntimeError('user does not exists')

            cert = create_cert(aergo)

        return jsonify(cert)
    except Exception as e:
        traceback.print_exc()
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

        result = add_new_user(username, password, metadata={
            'username': username,
            'email': user_email,
        }, recovery_key=image_data_hash)

        # TODO register new user in AERGO sidechain to avoid GDPR

        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
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
        aergo = cached_conn(user_address)
        check_user_cert(aergo)

        if contract_type == "1on1":
            # contractor
            rcv_addr = payload['receiver']
            contents = payload['contents']
            result = issue_1on1_contract(aergo, rcv_addr, contents)
            return jsonify(result)
        else:
            raise RuntimeError("not supported contract type: {}".format(contract_type))
    except Exception as e:
        traceback.print_exc()
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
        aergo = cached_conn(user_address)
        check_user_cert(aergo)

        contract = get_1on1_contract(aergo, contract_id)
        return jsonify(contract)
    except Exception as e:
        traceback.print_exc()
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
        aergo = cached_conn(user_address)
        check_user_cert(aergo)

        contracts = get_all_1on1_contract(aergo, address)
        return jsonify(contracts)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to get contract list: {}".format(e)
        })


@app.route('/cancel/<contract_id>', methods=['POST'])
def cancel_contract(contract_id):
    print("call cancel_contract")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = cached_conn(user_address)
        check_user_cert(aergo)

        result = cancel_1on1_contract(aergo, contract_id)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to cancel the contract: {}".format(e)
        })


@app.route('/agree/<contract_id>', methods=['POST'])
def agree_contract(contract_id):
    print("call agree_contract")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = cached_conn(user_address)
        check_user_cert(aergo)

        result = sign_1on1_contract(aergo, contract_id)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to agree the contract: {}".format(e)
        })


@app.route('/disagree/<contract_id>', methods=['POST'])
def disagree_contract(contract_id):
    print("call disagree_contract")

    payload = request.data
    payload = json.loads(payload)
    user_address = payload['address']

    try:
        aergo = cached_conn(user_address)
        check_user_cert(aergo)

        result = disagree_1on1_contract(aergo, contract_id)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to disagree the contract: {}".format(e)
        })


if __name__ == '__main__':
    try:
        conf_file = sys.argv[1]
        with open(conf_file, 'r') as f:
            conf = toml.load(f)

        print(json.dumps(conf, indent=2))
        AERGO_CONF = conf
    except Exception as e:
        traceback.print_exc()
        raise e

    try:
        if sys.argv[2] == "debug":
            SC_SQLTESTNET_ENDPOINT = DEBUG_SC_SQLTESTNET_ENDPOINT
            AERGO_IS_DEBUG = True
    except:
        AERGO_IS_DEBUG = False
        pass

    aergo_mainnet = conn_mainnet()

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
        traceback.print_exc()
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
