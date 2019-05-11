--
-- AERGO Demo Smart Contract for SqlTestNet
-- by YP (hanlsin@blocko.io)
-- May 9, 2019
--

state.var {
  Version = state.value(),
  UserMap = state.map()
}

function constructor()
  Version:set("0.0.1")

  db.exec([[CREATE TABLE demo_user (
      username      TEXT NOT NULL,
      address       TEXT NOT NULL,
      block_no      INTEGER DEFAULT NULL,
      tx_hash       TEXT NOT NULL,
      metadata      TEXT,
      PRIMARY KEY (address)
    )]])

  db.exec([[CREATE TABLE demo_user_recovery (
      address       TEXT NOT NULL,
      block_no      INTEGER DEFAULT NULL,
      tx_hash       TEXT NOT NULL,
      recovery_key  TEXT,
      PRIMARY KEY (address, tx_hash),
      FOREIGN KEY (address) REFERENCES demo_user (address)
        ON DELETE CASCADE ON UPDATE NO ACTION
    )]])

  db.exec([[CREATE TABLE demo_cert (
      address       TEXT NOT NULL,
      block_no      INTEGER DEFAULT NULL,
      tx_hash       TEXT NOT NULL,
      expire_after  INTEGER DEFAULT 86400,
      PRIMARY KEY (address, tx_hash),
      FOREIGN KEY (address) REFERENCES demo_user (address)
        ON DELETE CASCADE ON UPDATE NO ACTION
    )]])

  db.exec([[CREATE TABLE demo_contract_1on1 (
      contract_id   TEXT NOT NULL,
      iss_addr      TEXT NOT NULL,
      rcv_addr      TEXT NOT NULL,
      block_no      INTEGER DEFAULT NULL,
      contents      TEXT,
      iss_sign      TEXT,
      rcv_sign      TEXT,
      PRIMARY KEY (contract_id),
      FOREIGN KEY (iss_addr) REFERENCES demo_user (address)
        ON DELETE CASCADE ON UPDATE NO ACTION
    )]])
end

function getVersion()
  return Version:get()
end

function addNewUser(username, metadata)
  local address = system.getOrigin()
  local blockNo = system.getBlockheight()
  local txHash = system.getTxhash()

  local userInfo = getUserInfo2(username)
  if userInfo['block_no'] ~= nil then
    contract.event("user", "add", txHash, 400, "username already exists")
    return
  end

  local stmt = db.prepare([[INSERT INTO demo_user
              (username, address, block_no, tx_hash, metadata)
      VALUES  (?, ?, ?, ?, ?)]])
  stmt:exec(username, address, blockNo, txHash, metadata)

  contract.event("user", "add", txHash, 201, {
    username = username,
    address = address,
    block_no = blockNo,
    tx_hash = txHash,
    metadata = json:decode(metadata)
    })
  return
end

function getUserInfo2(username)
  local stmt = db.prepare([[SELECT address, block_no, tx_hash, metadata
    FROM demo_user WHERE username = ?]])
  local rs = stmt:query(username)

  if rs:next() == false then
    return {
      username = username
    }
  end

  local row = { rs:get() }

  return {
    username = username,
    address = row[1],
    block_no = row[2],
    tx_hash = row[3],
    metadata = json:decode(row[4])
  }
end

function getUserInfo(address)
  local stmt = db.prepare([[SELECT username, block_no, tx_hash, metadata
    FROM demo_user WHERE address = ?]])
  local rs = stmt:query(address)

  if rs:next() == false then
    return {
      address = address
    }
  end

  local row = { rs:get() }

  return {
    username = row[1],
    address = address,
    block_no = row[2],
    tx_hash = row[3],
    metadata = json:decode(row[4])
  }
end

function addRecoveryKey(key)
  local address = system.getOrigin()
  local blockNo = system.getBlockheight()
  local txHash = system.getTxhash()

  local stmt = db.prepare([[INSERT INTO demo_user_recovery
              (address, block_no, tx_hash, recovery_key)
      VALUES  (?, ?, ?, ?)]])
  stmt:exec(address, blockNo, txHash, key)
end

function createCert(expireAfter)
  local address = system.getOrigin()
  local blockNo = system.getBlockheight()
  local txHash = system.getTxhash()

  local stmt = db.prepare([[SELECT username FROM demo_user WHERE address = ?]])
  local rs = stmt:query(address)

  if rs:next() == false then
    contract.event("cert", "create", txHash, 404, "signup first")
    return
  end

  local username = rs:get()

  if expireAfter == nil or expireAfter < 0 then
    expireAfter = 86400
  end

  local stmt = db.prepare([[INSERT INTO demo_cert
              (address, block_no, tx_hash, expire_after)
      VALUES  (?, ?, ?, ?)]])
  stmt:exec(address, blockNo, txHash, expireAfter)

  contract.event("cert", "create", txHash, 200, {
    username = username,
    address = address,
    block_no = blockNo,
    tx_hash = txHash,
    expire_after = expireAfter
    })
  return
end

function getUserCert(proof, sign, address)
  local proofHash = crypto.sha256(proof)
  if not crypto.ecverify(proofHash, sign, address) then
    return {
      _status_code = 403.2,
      _status_msg = "cannot verify the proof message: " .. proof
    }
  end

  local stmt = db.prepare([[SELECT block_no, tx_hash, expire_after
    FROM demo_cert WHERE address = ? ORDER BY block_no DESC]])
  local rs = stmt:query(address)

  if rs:next() == false then
    return {
      _status_code = 404,
      _status_msg = "cannot find any certificate"
    }
  end

  local row = { rs:get() }

  return {
    address = address,
    block_no = row[1],
    tx_hash = row[2],
    expire_after = row[3]
  }
end

function getUserRecoveryKeys(address)
  local stmt = db.prepare([[SELECT block_no, tx_hash, recovery_key
    FROM demo_user_recovery WHERE address = ? ORDER BY block_no]])
  local rs = stmt:query(address)

  local rows = {}
  while rs:next() do
    local row = { rs:get() }
    table.insert(rows, {
      address = address,
      block_no = row[1],
      tx_hash = row[2],
      recovery_key = row[3]
      })
  end

  return rows
end

function addNew1on1Contract(sign, rcvAddr, contents)
  local address = system.getOrigin()
  local blockNo = system.getBlockheight()
  local contractId = system.getTxhash()

  local contractRaw = "" .. address .. rcvAddr
  if contents ~= nil then
    contractRaw = contractRaw .. contents
  end
  system.print(contractRaw)

  -- verify issuer's signature
  local contractHash = crypto.sha256(contractRaw)
  if not crypto.ecverify(contractHash, sign, address) then
    contract.event("contract", "new", contractId, 400, "wrong issuer's signature")
    return
  end

  local stmt = db.prepare([[INSERT INTO demo_contract_1on1
              (contract_id, iss_addr, rcv_addr, block_no, contents, iss_sign)
      VALUES  (?, ?, ?, ?, ?, ?)]])
  stmt:exec(contractId, address, rcvAddr, blockNo, contents, sign)

  contract.event("contract", "new", contractId, 201, contractRaw)
  return
end

function sign1on1Contract(contractId, sign)
  local address = system.getOrigin()
  local txHash = system.getTxhash()

  local stmt = db.prepare([[SELECT iss_addr, rcv_addr, contents,
          block_no, iss_sign, rcv_sign
    FROM demo_contract_1on1 WHERE contract_id = ?]])
  local rs = stmt:query(contractId)

  if rs:next() == false then
    contract.event("contract", "sign", txHash, 404, "cannot find a contract")
    return
  end

  local row = { rs:get() }
  local rcvAddr = row[2]
  if address ~= rcvAddr then
    contract.event("contract", "sign", txHash, 400, "receiver is different")
    return
  end

  local contractRaw = "" .. row[1] .. rcvAddr .. row[3]
  system.print(contractRaw)

  local issSign = row[5]
  if issSign == 'CANCEL' then
    contract.event("contract", "sign", txHash, 400, "issuer discarded the contract")
    return
  end

  local rcvSign = row[6]
  if rcvSign ~= nil then
    contract.event("contract", "sign", txHash, 400, "receiver already disagreed or signed")
    return
  end

  -- verify issuer's signature
  local contractHash = crypto.sha256(contractRaw)
  system.print(contractHash)
  if not crypto.ecverify(contractHash, sign, address) then
    contract.event("contract", "sign", txHash, 400, "wrong receiver's signature")
    return
  end

  local stmt = db.prepare([[UPDATE demo_contract_1on1 SET rcv_sign = ?
      WHERE contract_id = ?]])
  stmt:exec(sign, contractId)

  contract.event("contract", "sign", txHash, 201, {
    contract_id = contractId,
    issuer = row[1],
    receiver = rcvAddr,
    contents = row[3],
    block_no = row[4],
    issuer_sign = issSign,
    receiver_sign = sign
    })
  return
end

function cancel1on1Contract(contractId)
  local address = system.getOrigin()
  local txHash = system.getTxhash()

  local stmt = db.prepare([[SELECT iss_addr, iss_sign, rcv_sign
    FROM demo_contract_1on1 WHERE contract_id = ?]])
  local rs = stmt:query(contractId)

  if rs:next() == false then
    contract.event("contract", "cancel", txHash, 404, "cannot find a contract")
    return
  end

  local row = { rs:get() }
  local issAddr = row[1]
  if address ~= issAddr then
    contract.event("contract", "cancel", txHash, 400,
      "only issuer can cancel the contract")
    return
  end

  local issSign = row[2]
  if issSign == 'CANCEL' then
    contract.event("contract", "cancel", txHash, 400,
      "issuer already canceled")
    return
  end

  local rcvSign = row[3]
  if rcvSign ~= nil then
    contract.event("contract", "cancel", txHash, 400,
      "receiver already disagreed or signed")
    return
  end

  local stmt = db.prepare([[UPDATE demo_contract_1on1 SET iss_sign = ?
      WHERE contract_id = ?]])
  stmt:exec("CANCEL", contractId)

  contract.event("contract", "cancel", txHash, 201, contract_id)
  return
end

function disagree1on1Contract(contractId)
  local address = system.getOrigin()
  local txHash = system.getTxhash()

  local stmt = db.prepare([[SELECT rcv_addr, iss_sign, rcv_sign
    FROM demo_contract_1on1 WHERE contract_id = ?]])
  local rs = stmt:query(contractId)

  if rs:next() == false then
    contract.event("contract", "disagree", txHash, 404,
      "cannot find a contract")
    return
  end

  local row = { rs:get() }
  local rcvAddr = row[1]
  if address ~= rcvAddr then
    contract.event("contract", "disagree", txHash, 400,
      "only receiver can disagree the contract")
    return
  end

  local issSign = row[2]
  if issSign == 'CANCEL' then
    contract.event("contract", "disagree", txHash, 400,
      "issuer already canceled")
    return
  end

  local rcvSign = row[3]
  if rcvSign ~= nil then
    contract.event("contract", "disagree", txHash, 400,
      "receiver already disagreed or signed")
    return
  end

  local stmt = db.prepare([[UPDATE demo_contract_1on1 SET rcv_sign = ?
      WHERE contract_id = ?]])
  stmt:exec("DISAGREE", contractId)

  contract.event("contract", "disagree", txHash, 201, contract_id)
  return
end

function get1on1Contract(contractId)
  local stmt = db.prepare([[SELECT iss_addr, rcv_addr, contents, block_no,
          iss_sign, rcv_sign
    FROM demo_contract_1on1 WHERE contract_id = ?]])
  local rs = stmt:query(contractId)

  if rs:next() == false then
    return {
      contract_id = contractId
    }
  end

  local row = { rs:get() }
  return {
    contract_id = contractId,
    issuer = row[1],
    receiver = row[2],
    contents = row[3],
    block_no = row[4],
    issuer_sign = row[5],
    receiver_sign = row[6]
  }
end

function getAll1on1Contract()
  local stmt = db.prepare([[SELECT iss_addr, rcv_addr, contents, block_no,
          iss_sign, rcv_sign, contract_id
    FROM demo_contract_1on1 ORDER BY block_no DESC]])
  local rs = stmt:query()

  local rows = {}
  while rs:next() do
    local row = { rs:get() }
    system.print(row)
    table.insert(rows, {
      issuer = row[1],
      receiver = row[2],
      contents = row[3],
      block_no = row[4],
      issuer_sign = row[5],
      receiver_sign = row[6],
      contract_id = row[7]
      })
  end

  return rows
end

function getAllIssued1on1Contract(issAddr)
  local stmt = db.prepare([[SELECT iss_addr, rcv_addr, contents, block_no,
          iss_sign, rcv_sign, contract_id
    FROM demo_contract_1on1 WHERE iss_addr = ? ORDER BY block_no DESC]])
  local rs = stmt:query(issAddr)

  local rows = {}
  while rs:next() do
    local row = { rs:get() }
    table.insert(rows, {
      issuer = row[1],
      receiver = row[2],
      contents = row[3],
      block_no = row[4],
      issuer_sign = row[5],
      receiver_sign = row[6],
      contract_id = row[7]
      })
  end

  return rows
end

function getAllReceived1on1Contract(rcvAddr)
  local stmt = db.prepare([[SELECT iss_addr, rcv_addr, contents, block_no,
          iss_sign, rcv_sign, contract_id
    FROM demo_contract_1on1 WHERE rcv_addr = ? ORDER BY block_no DESC]])
  local rs = stmt:query(rcvAddr)

  local rows = {}
  while rs:next() do
    local row = { rs:get() }
    table.insert(rows, {
      issuer = row[1],
      receiver = row[2],
      contents = row[3],
      block_no = row[4],
      issuer_sign = row[5],
      receiver_sign = row[6],
      contract_id = row[7]
      })
  end

  return rows
end

abi.register(addNewUser, addRecoveryKey, createCert, addNew1on1Contract,
  sign1on1Contract, cancel1on1Contract, disagree1on1Contract)
abi.register_view(getVersion, getUserInfo2, getUserInfo, getUserCert,
  getUserRecoveryKeys, get1on1Contract,
  getAll1on1Contract, getAllIssued1on1Contract, getAllReceived1on1Contract)
