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
aergo_mainnet.connect("testnet-api.aergo.io:7845")
#aergo_mainnet.connect("mainnet-api.aergo.io:7845")
SC_MAINNET_VERSION = "0.0.1"
SC_MAINNET_PAYLOAD = "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"
SC_MAINNET_ADDRESS = "Amhnt25NtHeV6pwhZ9gh6b4QQmkqKegXAJV6Q4vaxyZBVtwgfsJE"

#SC_SQLTESTNET_ENDPOINT = "sqltestnet-api.aergo.io:7845"
SC_SQLTESTNET_ENDPOINT = "localhost:7845"
SC_SQLTESTNET_VERSION = "0.0.1"
SC_SQLTESTNET_PAYLOAD = "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"
SC_SQLTESTNET_ADDRESS = "Amhnt25NtHeV6pwhZ9gh6b4QQmkqKegXAJV6Q4vaxyZBVtwgfsJE"


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

    iss_addr = contract['issuer']
    rcv_addr = contract['receiver']
    contents = contract['contents']

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
    except:
        err_print("cannot run without conf file")

    # init account for MainNet
    try:
        aergo_mainnet.import_account(exported_data=conf['mainnet']['exported_key'],
                                     password=conf['mainnet']['password'])
        aergo_mainnet.get_account()
        print("MainNet Demo Address: {}".format(str(aergo_mainnet.account.address)))
    except:
        err_print("cannot run without MainNet account")

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
    except:
        err_print("cannot run without SqlTestNet account")

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
