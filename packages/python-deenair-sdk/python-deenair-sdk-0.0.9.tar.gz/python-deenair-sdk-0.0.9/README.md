# Python DeenAiR-SDK
Base python library to interact with DeenAiR blockchain.



[![License](https://img.shields.io/pypi/l/python-deenair-sdk.svg)](https://badge.fury.io/py/python-deenair-sdk)
[![PyPI version](https://badge.fury.io/py/python-deenair-sdk.svg)](https://badge.fury.io/py/python-deenair-sdk)
[![Python versions](https://img.shields.io/pypi/pyversions/python-deenair-sdk.svg)](https://pypi.python.org/pypi/python-deenair-sdk)
[![Downloads](https://img.shields.io/pypi/dm/python-deenair-sdk.svg)](https://pypi.python.org/pypi/python-deenair-sdk)

## This section will help you to do following features::
- Getting any blockchain info
- Key pair management
- Send transactions, manage your stakes


## Table of contents:
1. [Quick Start](#quick-start)
2. [Methods](#methods)
    - [create_and_send_transaction](#create_and_send_transaction)
    - [get_leader](#get_leader)
    - [get_block](#get_block)
    - [get_node_list](#get_node_list)
    - [get_transaction](#get_transaction)
    - [get_wallet_transactions](#get_wallet_transactions)
    - [get_wallet_state](#get_wallet_state)
    - [get_my_stakes](#get_my_stakes)
    - [generate_keypair](#generate_keypair)
    - [recover_keypair_from_phrase](#recover_keypair_from_phrase)
    - [create_nft](#create_nft)
    - [get_collection](#get_collection)
    - [get_token](#get_token)
    - [burn_nft](#burn_nft)
    - [donate_nft](#donate_nft)
    - [emit_fft](#emit_fft)
    - [transfer_fft](#transfer_fft)
    - [get_fft_list](#get_fft_list)
    - [get_fft_info](#get_fft_info)


## Quick Start

It is easy to install, use and integrate.

1. Install python-deenair-sdk via pip

```pip3 install python-deenair-sdk```

2. Import, declare Client, use methods.

```
from python_deenair_sdk import Client

client = Client("http://mainnet.deenair.org")
my_balance = client.get_wallet_state("FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z")
print(my_balance)
```


## Methods


### create_and_send_transaction

DeenAiR blockchain model is very flexible and allow you to send several messages per transaction. Also, you can pass and sign it with different private keys.
For example, address1 want to send 1.5 DEEN to address2, delegate 1000 DEEN for Node 1, withdraw 2000 DEEN stake from Node 4.

Arguments:
- messages - _list_ contains:
    - message_type _("transfer", "delegate", "withdraw")_
    - payer_secret - _string_ base58 encoded private key
    - receiver_public - _string_ base58 encoded receiver public key
    - amount - _float_ DEEN amount
    - comment - _string_ text comment for message

fee_payer_secret - _string_ base58 encoded private key fee payer

```
data_for_messages = [
    {"message_type": "transfer",
    "payer_secret": "my_private_key",
    "receiver_public": "address2",
    "amount": 1.5,
    "comment": ""},

    {"message_type": "delegate",
    "payer_secret": "my_private_key",
    "receiver_public": "Node 1 address",
    "amount": 1000,
    "comment": ""},

    {"message_type": "withdraw",
    "payer_secret": "my_private_key",
    "receiver_public": "Node 4 address",
    "amount": 2000,
    "comment": ""},
]

transaction_sending_result = client.create_and_send_transaction(data_for_messages, fee_payer_secret="my_other_private_key")
```

### get_leader

This method return current leader. 

```leader = client.get_leader()```

Return:
- nodeid - Node unique identifier which will validate the block 

```
print(leader)
>>> {'id': '8f016b12-2f2d-4b41-aa06-a2868192204f',
 'jsonrpc': '2.0',
 'result': {'nodeid': '8b7PH1SwGXPpNJz5Md7zrLwDNyu9qMM7TYTvY7jRtRaG'},
 'status': 'ok'}
```

### get_block

Return block info. Pass "latest" for latest block info, or string contain block index for certain block. "12" for example. 

Arguments:
    - block _string_ - pass block index or "latest"
```block = client.get_block("latest")```

Return:
- "blk" - block number
- "blkid" - block hash
- "trxs" - transactions list
- "validator" - node validated this block


```
print(block)

>>> {'id': 'c4360936-3320-490e-afc0-8f850c5e143b',
 'jsonrpc': '2.0',
 'result': {'blk': '12',
            'blkid': 'CUgGe4RMdRfvGah9yNEoaUv6DsBnpBLgQip9RaTmi7YD',
            'trxs': [{'status': 'approved',
                      'trxid': '4Kwwjiqf7S9QapRm3V6ibnNwgG8x2skKFyi9uCsTZ79a',
                      'type': 'system',
                      'votes': [{'author': 'HW7d1jxu3emHanUwYSKoCS7A5zQ3XDN966MBAfW1VLib',
                                 'block': '13',
                                 'round': '1',
                                 'sign': 'gmKYGBMTYb7bLMdgEnoGUPDKzQ5RXhPMQnQ2wyY4uTRabf7tpG6JdXZFjvgyETYre3P2Z9JiTdZuLc18DsZXuQS',
                                 'vote': '2CieeTFDM9NxYbQMqxMhuGT2dhpdWbXBBzdhrCf47vA6'},
                                {'author': 'H5KAwn1A2MtYxCeEHsL3y8qadCWbnZ5MvjZWoukHJwp4',
                                 'block': '13',
                                 'round': '1',
                                 'sign': '4NqHz47ENNXUwonFkBEqxAQmApzny6weR7j5K6pQwAkvdPGudRP1ziP46p9yykvKJvCGfvLMpbSYEbhW4dpM3CYA',
                                 'vote': '8b7PH1SwGXPpNJz5Md7zrLwDNyu9qMM7TYTvY7jRtRaG'},
                                {'author': 'GPQXtBJs7W7sCmciWfJyrvHPGuYkNT9rqV6VrQs2DeLY',
                                 'block': '13',
                                 'round': '1',
                                 'sign': '2ezhyFBnphL97irUtMUFYgJuURoFgxqF1FQZT8JzaS1TUpqPPqxAKhrQns896vL133o1uWA9H6mWsRQkhtaJ57cq',
                                 'vote': 'D72hBA6kJdK5H5kEUMvCCJgHDu8CrdEtYzxNYz1RdeHd'},
                                {'author': 'FQ7UGXXCtCrKH4WhYkUb3iNWQNs1mKYGYfMUrzYncvFA',
                                 'block': '13',
                                 'round': '1',
                                 'sign': '5nvmUcxek7a8ydYg4EAJUC2FgFg4W1br5GadihfbQfSZjF9GmGucF8kNcdqWmRCAXxSQDiNR6dRd2UVwUm7bkQHD',
                                 'vote': '8b7PH1SwGXPpNJz5Md7zrLwDNyu9qMM7TYTvY7jRtRaG'},
                                {'author': 'EUjRzCXg8sUZhiajPhPuYw8z72zTPzRzHFjMt4XXtY2K',
                                 'block': '13',
                                 'round': '1',
                                 'sign': '3L2KVunzqHvG4rJnALmSK53dbWRnoHHvGWCi7AewkgGUnee8pG56RZf1JYR2sXB5HHKnoCRz8rmffrEYP6DAU2du',
                                 'vote': 'H5KAwn1A2MtYxCeEHsL3y8qadCWbnZ5MvjZWoukHJwp4'},
                                {'author': 'DCQP4AjFydfScw662awTXBg4hd5YkvqjhZotfe6o14bj',
                                 'block': '13',
                                 'round': '1',
                                 'sign': '4iwoR5RoEBxYkdHbjYpNZwgKfjZ94C59WgorZQqMxeyj7xx96AfA7PJe3umFSFPJVip4kEBgYZxPzua2p2gmyTK',
                                 'vote': 'D72hBA6kJdK5H5kEUMvCCJgHDu8CrdEtYzxNYz1RdeHd'},
                                {'author': 'D72hBA6kJdK5H5kEUMvCCJgHDu8CrdEtYzxNYz1RdeHd',
                                 'block': '13',
                                 'round': '1',
                                 'sign': '5Vgb8rszJt447xr9kTjC993GEjG31C34uih7swPhTkDZz1EYQ8RdfrZyLM5jD2zRLQknQNpQ5Ets1ceXzoHWg1Pc',
                                 'vote': 'H5KAwn1A2MtYxCeEHsL3y8qadCWbnZ5MvjZWoukHJwp4'},
                                {'author': '8b7PH1SwGXPpNJz5Md7zrLwDNyu9qMM7TYTvY7jRtRaG',
                                 'block': '13',
                                 'round': '1',
                                 'sign': '2yYKF9RABB6Ari15xVqeb19K3b9hprWwjXfnpDaPrWCKwjYgBUs5P1pa4Ey8bm3E9Zg4ApgtH12EAfZ3nGkoWBPY',
                                 'vote': 'FQ7UGXXCtCrKH4WhYkUb3iNWQNs1mKYGYfMUrzYncvFA'},
                                {'author': '2CieeTFDM9NxYbQMqxMhuGT2dhpdWbXBBzdhrCf47vA6',
                                 'block': '13',
                                 'round': '1',
                                 'sign': 'tifawJEMM95KaK9ZYCH36La1jdaWJ6hHRL2xMKZm9rMArtzWfmqBuNWHr3ye9UxKysr9zfgBDhi1EP79PRuferF',
                                 'vote': 'H5KAwn1A2MtYxCeEHsL3y8qadCWbnZ5MvjZWoukHJwp4'}]},
                     {'msgs': [{'comment': '',
                                'payer': 'FFvTLRy16bjefbgBPA9ZyYLwjiovkz77L7w27aneFnEQ',
                                'receiver': 'FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z',
                                'sign': '3fR5V3w8xuk8Ss3vuhvJ7YtCASzytBoTyF6Gt9rqH4pPak7UGLLBLCm1x7d9eGPHqe4i5qAPN39bciQVFWxvdJAJ',
                                'sum': '10000000',
                                'time': '1662457806000',
                                'type': 'transfer'},
                               {'comment': '',
                                'payer': 'FFvTLRy16bjefbgBPA9ZyYLwjiovkz77L7w27aneFnEQ',
                                'receiver': 'deenAiRoven55555555555555555555555555555555',
                                'sign': '39gLM2jwNtJU8dWia86ZBpcMs8LSPXiCS1YagJziNynJGpBvx5EF4EQnKaFWRXFWtG6jbfiQnDRUjvNpK8eErB2D',
                                'sum': '12270',
                                'time': '1662457806000',
                                'type': 'fee'}],
                      'status': 'approved',
                      'trxid': '5wdcefni8KffbhzSAoD56NzSPxE1F8r2f9WTgeBB26dS',
                      'type': 'remittance'},
                     {'msgs': [{'comment': 'system reward',
                                'payer': 'deenAiRissuer777777777777777777777777777777',
                                'receiver': 'FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z',
                                'sign': 'x1jHT4YybqPHeFmGZBuAw5vGoEhovNPA7vUq4LsFAAdReS9u1gQBovdfYwLds2Jm5pqHmrYaQxNNQyPCKkQKNuh',
                                'sum': '31802440',
                                'time': '1662457808465',
                                'type': 'emission'},
                               {'comment': 'node reward',
                                'payer': 'deenAiRissuer777777777777777777777777777777',
                                'receiver': 'FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z',
                                'sign': '5kq3tkRaDPLWcZxS3uqpLMSkSpZJokPWBcem31ttyBX82mPkvyLGkxs5VgPp4CmDxYtuhuQLrrCYfhLrz6co1yov',
                                'sum': '31802440',
                                'time': '1662457808465',
                                'type': 'emission'},
                               {'comment': 'reward for block 12',
                                'payer': 'deenAiRissuer777777777777777777777777777777',
                                'receiver': 'DkYVUPNbjcpdYe2mh8G7QfejZrP6W9wKjHaUA4rnhYHJ',
                                'sign': '5xUs1Jn1aRCyDvhZkXpqrePn2cUtfegYQRiLsRRJdcrozjkAPJiVRkPu7oGfVbgtA255NLi1Riz5as8894DUoeMm',
                                'sum': '95407390',
                                'time': '1662457808465',
                                'type': 'emission'}],
                      'status': 'approved',
                      'trxid': 'HFsmQune59PB98MS1BbCVLZiHsNvBVUjrHfVJ24615sj',
                      'type': 'remittance'}],
            'validator': 'EUjRzCXg8sUZhiajPhPuYw8z72zTPzRzHFjMt4XXtY2K'},
 'status': 'ok'}
```

### get_node_list

Return full known nodes list.

```nodes_list = client.get_node_list()```

Return:
- comment - Node description string
- ip address - Node ip address
- ip port - Node port
- nodeid - Node unique identifier which will validate the block 
- public - Node DeenAiR address
- stake - Total Solidius (1 DEEN = 10 000 000 Solidius) staked by this Node
- storage - Block keeps (will be deprecated soon)

```
print(nodes_list)

>>> {'id': '7acdde04-9484-408c-b989-9b5b64a48ba0',
 'jsonrpc': '2.0',
 'result': [{'comment': 'Node 1',
             'ip address': '91.92.144.211',
             'ip port': '333',
             'nodeid': 'GPQXtBJs7W7sCmciWfJyrvHPGuYkNT9rqV6VrQs2DeLY',
             'public': 'HW9SMTAjQ1JN1JuTwd2QmhFK8Er1svsMD65aFR7kfZXM',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node 2',
             'ip address': '147.124.216.116',
             'ip port': '333',
             'nodeid': 'H5KAwn1A2MtYxCeEHsL3y8qadCWbnZ5MvjZWoukHJwp4',
             'public': '7bQUofUVSJbFmyyGvtTGhuHGKseF9kPkv4RWjCXrcBFs',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node 3',
             'ip address': '185.230.245.83',
             'ip port': '333',
             'nodeid': '2CieeTFDM9NxYbQMqxMhuGT2dhpdWbXBBzdhrCf47vA6',
             'public': '2oT6CHZZBMHPZy9Z2B9on2NKLfP2P7PVg6jjCMcbVMTZ',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node 4',
             'ip address': '31.222.238.225',
             'ip port': '333',
             'nodeid': 'D72hBA6kJdK5H5kEUMvCCJgHDu8CrdEtYzxNYz1RdeHd',
             'public': 'Cmmdicq1bEUE6wQNX9G5xTqiuvpBytHV2oQ95Jwjf3Pv',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node 5',
             'ip address': '45.136.5.73',
             'ip port': '333',
             'nodeid': 'DCQP4AjFydfScw662awTXBg4hd5YkvqjhZotfe6o14bj',
             'public': '2CQfQmV42k7KLQHN8Dze6PHSuqrq4JEnzmgu8d3U3PsL',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node 6',
             'ip address': '213.202.241.242',
             'ip port': '333',
             'nodeid': 'FQ7UGXXCtCrKH4WhYkUb3iNWQNs1mKYGYfMUrzYncvFA',
             'public': '6FQMU9ms7LznQWAJtuqmu1Lq3qtzPPcw5gMULBiJRkZt',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node 7',
             'ip address': '103.236.108.79',
             'ip port': '333',
             'nodeid': 'EUjRzCXg8sUZhiajPhPuYw8z72zTPzRzHFjMt4XXtY2K',
             'public': '6NYffPMSuUeoJRHv9U3tiGzK1sJRHALKLMvLqqobgbQ1',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node 8',
             'ip address': '194.34.132.37',
             'ip port': '333',
             'nodeid': 'HW7d1jxu3emHanUwYSKoCS7A5zQ3XDN966MBAfW1VLib',
             'public': '8BNUCcpj5GMrBHS7HTAwBDEjK4hQg1h1TxoCW4fHS9Pj',
             'stake': '10000000000000',
             'storage': '0-1'},
            {'comment': 'Node ZERO',
             'ip address': '213.33.215.250',
             'ip port': '333',
             'nodeid': '8b7PH1SwGXPpNJz5Md7zrLwDNyu9qMM7TYTvY7jRtRaG',
             'public': 'BxcQzsfG7xuvLwpTr5SkMZ91JMfCXMQJYmL564XgR69y',
             'stake': '27182810000000',
             'storage': '0-1'}],
 'status': 'ok'}
```

### get_transaction

Get transaction info by transaction ID.

Arguments:
    - wallet _string_ - base58 encoded public key (DeenAiR address)

```trx_info = client.get_transaction("HFsmQune59PB98MS1BbCVLZiHsNvBVUjrHfVJ24615sj")```

Return:

- msgs - Messages list
- status ("approved", "rejected", "pending") - transaction status
- trxid - transaction hash
- type ("remittance" for DeenAiR sending, "system" for voting) - transaction type

Each message contain following information:
- type ("emission", "transfer", "fee", "delegate", "withdraw") - message type. 
- time - transaction sending unix timestamp since epoch (ms)
- sum - Solidius amount (1 DEEN = 10 000 000 Solidius)
- sign - Binary message ECDSA sign
- receiver - Base58 encoded receiver DeenAiR address
- payer - Base58 encoded sender DeenAiR address


```
print(trx_info)

>>> {'id': '8b0b1d15-d3f3-4ceb-8308-6aab0e10c4ec',
 'jsonrpc': '2.0',
 'result': {'msgs': [{'comment': 'system reward',
                      'payer': 'deenAiRissuer777777777777777777777777777777',
                      'receiver': 'FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z',
                      'sign': 'x1jHT4YybqPHeFmGZBuAw5vGoEhovNPA7vUq4LsFAAdReS9u1gQBovdfYwLds2Jm5pqHmrYaQxNNQyPCKkQKNuh',
                      'sum': '31802440',
                      'time': '1662457808465',
                      'type': 'emission'},
                     {'comment': 'node reward',
                      'payer': 'deenAiRissuer777777777777777777777777777777',
                      'receiver': 'FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z',
                      'sign': '5kq3tkRaDPLWcZxS3uqpLMSkSpZJokPWBcem31ttyBX82mPkvyLGkxs5VgPp4CmDxYtuhuQLrrCYfhLrz6co1yov',
                      'sum': '31802440',
                      'time': '1662457808465',
                      'type': 'emission'},
                     {'comment': 'reward for block 12',
                      'payer': 'deenAiRissuer777777777777777777777777777777',
                      'receiver': 'DkYVUPNbjcpdYe2mh8G7QfejZrP6W9wKjHaUA4rnhYHJ',
                      'sign': '5xUs1Jn1aRCyDvhZkXpqrePn2cUtfegYQRiLsRRJdcrozjkAPJiVRkPu7oGfVbgtA255NLi1Riz5as8894DUoeMm',
                      'sum': '95407390',
                      'time': '1662457808465',
                      'type': 'emission'}],
            'status': 'approved',
            'trxid': 'HFsmQune59PB98MS1BbCVLZiHsNvBVUjrHfVJ24615sj',
            'type': 'remittance'},
 'status': 'ok'}
```

### get_wallet_transactions

Return all transaction list received or sent by specified wallet.

Arguments:
    - wallet _string_ - base58 encoded public key (DeenAiR address)

```trx_list = client.get_wallet_transactions("13Apa2YGPfBu3SpRNN54JKbjrfPa3GorQR6J6dfrXZWC")```

Return:
`[trx1, trx2..., trxn]` - transactions list. Transaction and message [specification here](#get_transaction).

```
print(trx_list)

>>> {'id': 'a495d521-ac7a-4016-845c-ce251858b557',
 'jsonrpc': '2.0',
 'result': [{'msgs': [{'comment': '',
                       'payer': 'FFvTLRy16bjefbgBPA9ZyYLwjiovkz77L7w27aneFnEQ',
                       'receiver': '13Apa2YGPfBu3SpRNN54JKbjrfPa3GorQR6J6dfrXZWC',
                       'sign': '4dQobMR2ZBxKJZe4ACt4zmQmyUbYj1WqzpP3mKD58soTwCVwSCZsjyFxCES6PDzjPCf6NiJnF6KnBFYrRXiAXW84',
                       'sum': '100000000000000',
                       'time': '1661973067000',
                       'type': 'transfer'},
                      {'comment': '',
                       'payer': 'FFvTLRy16bjefbgBPA9ZyYLwjiovkz77L7w27aneFnEQ',
                       'receiver': 'deenAiRoven55555555555555555555555555555555',
                       'sign': '5oxErGF3wy8EGqcxM49TCdsXVVt7Em34PTXxFdXzXr4rp9gv9CH9yU8QPH5YPJCTmTWG1K7AtPWQzpdxoXGCTW6r',
                       'sum': '12270',
                       'time': '1661973067000',
                       'type': 'fee'}],
             'status': 'approved',
             'trxid': 'Dwvu33FLYJpnWhomQz7g2ZRxh98NXxLvxqGAV3MD1T5K',
             'type': 'remittance'}],
 'status': 'ok'}
```


### get_wallet_state

Return DeenAiR address current balance, last transaction ID. 

Arguments:
    - wallet _string_ - base58 encoded public key (DeenAiR address)
```wallet_state = client.get_wallet_state("FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z")```

Return:
- balance. Current Solidius amount.  (1 DEEN = 10 000 000 Solidius)
- last trx. Last approved transaction ID
- wallet - specified DeenAiR address
```
print(wallet_state)

>>> {'id': '87198eee-ad19-4ac8-92f1-81bb3919d0bb',
 'jsonrpc': '2.0',
 'result': {'balance': '2718282435234240',
            'last trx': 'HWcMvCi83gBEhdTfsS2UWotjVWhnq33vtWW8xzR4GPLD',
            'wallet': 'FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z'},
 'status': 'ok'}
```


### get_my_stakes

Return withdrawable stake amount and total amount staked by specified DeenAiR address.
You can withdraw your stake after 14 days. 

Arguments:
    - wallet _string_ - base58 encoded public key (DeenAiR address)

```my_stakes = client.get_my_stakes("FaN54gXbj6mhDob8CXwHLLuGwgBGiiswdaMt6d1UmS3z")```

Return:
- stake - total Solidius staked by this address
- withdrawable - total Solidius staked by this address able to withdraw

```
print(my_stakes)

>>> {'id': '87198eee-ad19-4ac8-92f1-81bb3919d0bb',
 'jsonrpc': '2.0',
 'result': {
    "stake":10000000,
    "withdrawable":0
},
 'status': 'ok'}
```


### generate_keypair

Generate seed, public key, private key.

Arguments:
- wallet_id _int, default = 3._ DeenAiR default derivation path  "m/44'/3566'/1'/0'/3'", but you can customize it with wallet_id argument. For example, if you pass _4_ - your derivation path becomes "m/44'/3566'/1'/0'/4'".
- strength - _int_, default 128._ It means your seed length will be equals 12 words. If you pass 256 - it will be 24 words.

```keypair = client.generate_keypair()```

Return dict contain following pairs:

- "seed" - your mnemonic seed. For keypair recovery. 
- "wallet_id" - wallet derivation path purpose. 
- "priv_key" - base58 encoded private key
- "publ_key" - base58 encoded public key (DeenAiR address)


### recover_keypair_from_phrase

Recover your private and public keys with your seed and derivation path

Arguments:
- phrase - _list_ Your seed phrase. ["abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon"]
- wallet_id - _int default=3._  Your address derivation path. 

Return dict contain following pairs:

- "wallet_id" - wallet derivation path purpose. 
- "priv_key" - base58 encoded private key
- "publ_key" - base58 encoded public key (DeenAiR address)


### create_nft

Create your NFT.

Arguments:
- metadata - _dict_ Your NFT Metadata  
- minter_pub - _string_ base58 encoded public key (DeenAiR address). This address will become an NFT owner.
- fee_payer_secret - _string_ base58 encoded private key fee payer
- collection_secret - _string_ base58 encoded collection private key


```
nft_meta = {
   "location": "https://path/to/your/mediafile",
   "trait_1": "trait_1_value",
   "trait_2": "trait_2_value",
   "trait_3": "trait_3_value",
   "royalty": {
      "SOMEONE_ADDRESS":"10"
   }
}
create_nft_result = client.create_nft(nft_meta,
                     collection_secret="NFT_COLLECTION_SECRET",
                     minter_pub="OWNER_ADDRESS",
                     fee_payer_secret="FEE_PAYER_SECRET"
                     )
```


### get_collection

Returns all token IDs of specified collection.

Arguments:
- collection_id _string_ Collection id.

```
collection = client.get_collection("GnBgxYeVwFSqPgn2SgGUK5hUPKTdbycU7n7E3xdSTbmu")

>>> {'jsonrpc': '2.0', 'status': 'ok', 'id': '3b12b8ad-2e3f-4ca6-b42d-7bab25a23e8e', 'result': ['AnVZpQb9SfAEYyL3FQA2Pj9Uv4KhY4Xz7jP719E2zVs']}
```


### get_token

Returns all token data.

Arguments:
- token_id _string_ Token id.

```
collection = client.get_token("AnVZpQb9SfAEYyL3FQA2Pj9Uv4KhY4Xz7jP719E2zVs")

>>> {'id': 'a1be3137-5b75-4911-a1c4-7476a234e4d6',
 'jsonrpc': '2.0',
 'result': {'coll': 'GnBgxYeVwFSqPgn2SgGUK5hUPKTdbycU7n7E3xdSTbmu',
            'last trx': '3ys5BPHdxnXwq83yzzHNCeokBFXsV8p3vjGmWTqLQEcM',
            'metadata': '{"location":"https://path/to/your/mediafile","trait_1":"trait_1_value","trait_2":"trait_2_value","trait_3":"trait_3_value","royalty":{"6w3yfx5ww6hG6KAU5uvGCo7JVK6ZbcFCyMV6pk78WkFX":"10"}}',
            'owner': '6TycKpDvqYszBxa5z2ce6wk17PiCFUhCtkw8J6uPNeef',
            'token': 'AnVZpQb9SfAEYyL3FQA2Pj9Uv4KhY4Xz7jP719E2zVs'},
 'status': 'ok'}
```

### burn_nft

Permamently delete your token.

Arguments: 

- token_id _string_ Token ID
- owner_private_key _string_ Owner's base58 encoded private key
- fee_payer_secret - _string_ base58 encoded private key fee payer

```
client.burn_nft("AnVZpQb9SfAEYyL3FQA2Pj9Uv4KhY4Xz7jP719E2zVs",
                        owner_private_key="owner_private_key",
                        fee_payer_secret="fee_payer_secret")
```


### donate_nft

Transfer of token ownership to another address.

Arguments: 

- token_id _string_ Token ID
- owner_private_key _string_ Owner's base58 encoded private key
- receiver _string_ New owner base58 encoded private key
- fee_payer_secret - _string_ base58 encoded private key fee payer

```
client.donate_nft("AnVZpQb9SfAEYyL3FQA2Pj9Uv4KhY4Xz7jP719E2zVs",
                        owner_private_key="owner_private_key",
                        receiver="new_owner_address",
                        fee_payer_secret="fee_payer_private_key")
```


### emit_fft

Create your own side-coin.

Arguments:

- amount _int_ - token amount to mint
- fft_public - _str_ token id
- owner_private - _str_ token creator base58 DeenAiR address
- emit_wallet - _str_ base58 DeenAiR address which receive minted tokens
- fee_payer_secret - _string_ base58 encoded private key fee payer
- token_name - _string_ Token name


```
 emit = client.emit_fft(amount=100000,
                    fft_public="TOKEN_PUBLIC_KEY,
                    owner_private="MINTER_PRIVATE_KEY",
                    emit_wallet="RECEIVER_ADDRESS",
                    fee_payer_secret="FEE_PAYER_PRIVATE_KEY",
                    token_name="USDT")
```


### transfer_fft

Transfer sidecoins.

Arguments:

- fft_public - _str_ token id
- sender_private_key - _str_ sender's private key
- receiver - _str_ base58 DeenAiR address which receive tokens 
- amount _int_ - token amount to mint
- fee_payer_secret - _string_ base58 encoded private key fee payer


```
cl.transfer_fft(fft_public=public_fft,
                sender_private_key="SENDER_PRIVATE_KEY,
                receiver="RECEIVER_ADDRESS",
                amount=1,
                fee_payer_secret="FEE_PAYER_PRIVATE_KEY")
```


### get_fft_info

Returns all data about sidecoin.

```
print(client.get_fft_info("CyR9v5yPQZjatM1uky9tSb5uqozvyfw5QkJLNqA9cZAi"))

>>> {'id': '71d6bec5-77dd-4007-93df-3b9aefad2b2f',
 'jsonrpc': '2.0',
 'result': {'name': 'USDT',
            'owner': '6w3yfx5ww6hG6KAU5uvGCo7JVK6ZbcFCyMV6pk78WkFX',
            'token': 'CyR9v5yPQZjatM1uky9tSb5uqozvyfw5QkJLNqA9cZAi'},
 'status': 'ok'}
```


### get_fft_list

Returns all FFT.

```
print(client.get_fft_list())

>>> {'id': 'cb78b237-15fa-44f4-8fb3-5f7d9d99baf7',
 'jsonrpc': '2.0',
 'result': ['CyR9v5yPQZjatM1uky9tSb5uqozvyfw5QkJLNqA9cZAi'],
 'status': 'ok'}
```