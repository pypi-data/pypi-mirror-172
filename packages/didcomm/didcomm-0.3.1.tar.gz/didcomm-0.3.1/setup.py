# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['didcomm',
 'didcomm.common',
 'didcomm.core',
 'didcomm.core.keys',
 'didcomm.did_doc',
 'didcomm.protocols',
 'didcomm.protocols.routing',
 'didcomm.secrets']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=1.1.0,<2.0.0',
 'attrs>=21.2,<22.0',
 'base58>=2.1,<3.0',
 'packaging>=21.0,<22.0',
 'pycryptodomex>=3.10,<4.0',
 'varint>=1.0.2,<1.1.0']

setup_kwargs = {
    'name': 'didcomm',
    'version': '0.3.1',
    'description': 'Basic DIDComm v2 support in python',
    'long_description': '# DIDComm Python\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Unit Tests](https://github.com/sicpa-dlab/didcomm-python/workflows/verify/badge.svg)](https://github.com/sicpa-dlab/didcomm-python/actions/workflows/verify.yml)\n[![Python Package](https://img.shields.io/pypi/v/didcomm)](https://pypi.org/project/didcomm/)\n\nBasic [DIDComm v2](https://identity.foundation/didcomm-messaging/spec) support in Python.\n\n## Installation\n```\npip install didcomm\n```\n\n## DIDComm + peerdid Demo\nSee https://github.com/sicpa-dlab/didcomm-demo.\n\n## Assumptions and Limitations\n- Python >= 3.7.\n- In order to use the library, `SecretsResolver` and `DIDResolver` interfaces must be implemented on the application level. \n  Implementation of that interfaces is out of DIDComm library scope.  \n  - Verification materials are expected in JWK, Base58 and Multibase (internally Base58 only) formats.\n    - In Base58 and Multibase formats, keys using only X25519 and Ed25519 curves are supported.\n    - For private keys in Base58 and Multibase formats, the verification material value contains both private and public parts (concatenated bytes).\n    - In Multibase format, bytes of the verification material value is prefixed with the corresponding Multicodec code.\n  - Key IDs (kids) used in `SecretsResolver` must match the corresponding key IDs from DID Doc verification methods.\n  - Key IDs (kids) in DID Doc verification methods and secrets must be a full [DID Fragment](https://www.w3.org/TR/did-core/#fragment), that is `did#key-id`.\n  - Verification methods referencing another DID Document are not supported (see [Referring to Verification Methods](https://www.w3.org/TR/did-core/#referring-to-verification-methods)).\n- The following curves and algorithms are supported:\n  - Encryption:\n     - Curves: X25519, P-384, P-256, P-521\n     - Content encryption algorithms: \n       - XC20P (to be used with ECDH-ES only, default for anoncrypt),\n       - A256GCM (to be used with ECDH-ES only),\n       - A256CBC-HS512 (default for authcrypt)\n     - Key wrapping algorithms: ECDH-ES+A256KW, ECDH-1PU+A256KW\n  - Signing:\n    - Curves: Ed25519, Secp256k1, P-256\n    - Algorithms: EdDSA (with crv=Ed25519), ES256, ES256K\n- Forward protocol is implemented and used by default.\n- DID rotation (`fromPrior` field) is supported.\n- DIDComm has been implemented under the following [Assumptions](https://hackmd.io/i3gLqgHQR2ihVFV5euyhqg)   \n\n\n## Examples\n\nSee [demo scripts](tests/demo) for details.\n\nA general usage of the API is the following:\n- Sender Side:\n  - Build a `Message` (plaintext, payload).\n  - Convert a message to a DIDComm Message for further transporting by calling one of the following:\n     - `pack_encrypted` to build an Encrypted DIDComm message\n     - `pack_signed` to build a Signed DIDComm message\n     - `pack_plaintext` to build a Plaintext DIDComm message\n- Receiver side:\n  - Call `unpack` on receiver side that will decrypt the message, verify signature if needed\n  and return a `Message` for further processing on the application level.\n\n### 1. Build an Encrypted DIDComm message for the given recipient\n\nThis is the most common DIDComm message to be used in most of the applications.\n\nA DIDComm encrypted message is an encrypted JWM (JSON Web Messages) that \n- hides its content from all but authorized recipients\n- (optionally) discloses and proves the sender to only those recipients\n- provides message integrity guarantees\n\nIt is important in privacy-preserving routing. It is what normally moves over network transports in DIDComm\napplications, and is the safest format for storing DIDComm data at rest.\n\nSee `pack_encrypted` documentation for more details.\n\n**Authentication encryption** example (most common case):\n\n```\n# ALICE\nmessage = Message(body={"aaa": 1, "bbb": 2},\n                  id="1234567890", type="my-protocol/1.0",\n                  frm=ALICE_DID, to=[BOB_DID])\npack_result = await pack_encrypted(message=message, frm=ALICE_DID, to=BOB_DID)\npacked_msg = pack_result.packed_msg\nprint(f"Sending ${packed_msg} to ${pack_result.service_metadata.service_endpoint}")\n\n# BOB\nunpack_result = await unpack(packed_msg)\nprint(f"Got ${unpack_result.message} message")\n```\n\n**Anonymous encryption** example:\n\n```\nmessage = Message(body={"aaa": 1, "bbb": 2},\n                  id="1234567890", type="my-protocol/1.0",\n                  frm=ALICE_DID, to=[BOB_DID])\npack_result = await pack_encrypted(message=message, to=BOB_DID)\n```\n\n**Encryption with non-repudiation** example:\n\n```\nmessage = Message(body={"aaa": 1, "bbb": 2},\n                  id="1234567890", type="my-protocol/1.0",\n                  frm=ALICE_DID, to=[BOB_DID])\npack_result = await pack_encrypted(message=message, frm=ALICE_DID, to=BOB_DID, sign_frm=ALICE_DID)\n```\n\n### 2. Build an unencrypted but Signed DIDComm message\n\nSigned messages are only necessary when\n- the origin of plaintext must be provable to third parties\n- or the sender can’t be proven to the recipient by authenticated encryption because the recipient is not known in advance (e.g., in a\nbroadcast scenario).\n \nAdding a signature when one is not needed can degrade rather than enhance security because it\nrelinquishes the sender’s ability to speak off the record.\n\nSee `pack_signed` documentation for more details.\n\n```\n# ALICE\nmessage = Message(body={"aaa": 1, "bbb": 2},\n                  id="1234567890", type="my-protocol/1.0",\n                  frm=ALICE_DID, to=[BOB_DID])\npacked_msg = await pack_signed(message=message, sign_frm=ALICE_DID)\npacked_msg = pack_result.packed_msg\nprint(f"Publishing ${packed_msg}")\n\n# BOB\nunpack_result = await unpack(packed_msg)\nprint(f"Got ${unpack_result.message} message signed as ${unpack_result.metadata.signed_message}")\n```\n\n### 3. Build a Plaintext DIDComm message\n\nA DIDComm message in its plaintext form that \n- is not packaged into any protective envelope\n- lacks confidentiality and integrity guarantees\n- repudiable\n\nThey are therefore not normally transported across security boundaries. \n\n```\n# ALICE\nmessage = Message(body={"aaa": 1, "bbb": 2},\n                  id="1234567890", type="my-protocol/1.0",\n                  frm=ALICE_DID, to=[BOB_DID])\npacked_msg = await pack_plaintext(message)\nprint(f"Publishing ${packed_msg}")\n\n# BOB\nunpack_result = await unpack(packed_msg)\nprint(f"Got ${unpack_result.plaintext} message")\n```\n\n## Contribution\nPRs are welcome!\n\nThe following CI checks are run against every PR:\n- all tests must pass\n- [flake8](https://github.com/PyCQA/flake8) checks must pass\n- code must be formatted by [Black](https://github.com/psf/black)',
    'author': 'SICPA',
    'author_email': 'DLCHOpenSourceContrib@sicpa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sicpa-dlab/didcomm-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
