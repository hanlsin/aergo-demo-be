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
SC_MAINNET_ADDRESS = "AmgmyriYhaFzzeYerxhxUzhFc5PypKrt5c848cRb947RFwcnmGr6"

DEBUG_SC_SQLTESTNET_ENDPOINT = "localhost:7845"
SC_SQLTESTNET_ENDPOINT = "sqltestnet-api.aergo.io:7845"
#SC_SQLTESTNET_ENDPOINT = "sql1.aergo.io:7845"
#SC_SQLTESTNET_ENDPOINT = "sql2.aergo.io:7845"
#SC_SQLTESTNET_ENDPOINT = "sql3.aergo.io:7845"
SC_SQLTESTNET_VERSION = "0.0.1"
SC_SQLTESTNET_PAYLOAD = "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"
SC_SQLTESTNET_ADDRESS = "AmhghEmLFq8kd7m3ttUppe1pYmaN45VVF3BbbJRxJD48efbm4JvP"


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
    tx_hash = None
    try:
        metadata_str = json.dumps(metadata)
        tx = call_sc(aergo, SC_SQLTESTNET_ADDRESS, "addNewUser",
                     args=[username, metadata_str])
        tx_hash = str(tx.tx_hash)
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
        call_sc(aergo_mainnet, SC_MAINNET_ADDRESS, "addNewUser",
                args=[address, tx_hash])
    except Exception as e:
        traceback.print_exc()
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
        traceback.print_exc()
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
        traceback.print_exc()
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

        enc_key = add_new_user(username, password, metadata={
            'username': username,
            'email': user_email,
        }, recovery_key=image_data_hash)

        # TODO register new user in AERGO sidechain to avoid GDPR

        return jsonify({
            "encrypted_key": enc_key
        })
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
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
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
        aergo = AERGO_CONN_DICT[user_address]
    except:
        raise RuntimeError("cannot find the user certificate")

    check_user_cert(aergo)

    try:
        contracts = get_all_1on1_contract(aergo, address)
        return jsonify(contracts)
    except Exception as e:
        traceback.print_exc()
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
        traceback.print_exc()
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
        traceback.print_exc()
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
        traceback.print_exc()
        return jsonify({
            "error_msg": "fail to disagree contracts: {}".format(e)
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
