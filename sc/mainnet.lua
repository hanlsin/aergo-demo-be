--
-- AERGO Demo Smart Contract for MainNet
-- by YP (hanlsin@blocko.io)
-- May 9, 2019
--

state.var {
  Version = state.value(),
  UserMap = state.map()
}

function constructor()
  Version:set("0.0.1")
end

function getVersion()
  return Version:get()
end

function addNewUser(addr, initTx)
  UserMap[addr] = {
    sqlTestChain = {
      addr = addr,
      initTx = initTx,
    },
    blockNo = system.getBlockheight(),
    txHash = system.getTxhash(),
    certHashList = {},
    issuedContract = {},
    receivedContract = {}
  }
end

function getUserInfo(addr)
  return UserMap[addr]
end

function registerNewCertHash(addr, certId, certHash)
  local userInfo = UserMap[addr]
  table.insert(userInfo["certHashList"], {
    certId = certId,
    certHash = certHash,
    blockNo = system.getBlockheight(),
    txHash = system.getTxhash()
  })
  UserMap[addr] = userInfo
end

function register1on1Contract(issAddr, rcvAddr, contractId, contractHash)
  local issuer = UserMap[issAddr]
  issuer["issuedContract"][contractId] = {
    receiver = rcvAddr,
    contractId = contractId,
    contractHash = contractHash,
    blockNo = system.getBlockheight(),
    txHash = system.getTxhash()
  }
  UserMap[issAddr] = issuer

  local receiver = UserMap[rcvAddr]
  receiver["receivedContract"][contractId] = {
    issuer = issAddr,
    contractId = contractId,
    contractHash = contractHash,
    blockNo = system.getBlockheight(),
    txHash = system.getTxhash()
  }
  UserMap[rcvAddr] = receiver
end

abi.register(addNewUser, registerNewCertHash, register1on1Contract)
abi.register_view(getVersion, getUserInfo)
