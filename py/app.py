import logging
from logging import Formatter, FileHandler

from flask import Flask, request, jsonify
from waitress import serve

from src import HSM, Svault, int_to_bytes, hex_to_bytes
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.exceptions import PinIncorrect, NoSuchKey, NoSuchToken, MultipleObjectsReturned

ALLOWED_KEY_TYPS= ["rsa", "aes"]

"""
    - key_type
    - secret_path
    - secret_version
    - payload
    - iv
"""

app = Flask(__name__)
hsm = HSM(slot="OpenDNSSEC", pin="1234") # it should be managed as session

@app.route("/")
def hello():
    return "Weclome!"
    # routes = []
    # for route in app.url_map.iter_rules():
    #     routes.append('%s' % route)
    # all_indexs = "\n".join(sorted(routes))

    # return all_indexs

@app.route("/gen/key/<key_type>", methods=['GET', 'POST'])
def genkey(key_type,secret_path,secret_version):
    if key_type in ALLOWED_KEY_TYPS:
        if request.method == 'GET':
            return jsonify({"Error":"we only support rsa & aes"})

        if request.method == 'POST':
            secret_path = request.json['secret_path']
            secret_version = int(request.json['secret_version'])
        
            if key_type == "rsa":
                if hsm.gen_rsa(secret_path,secret_version):
                    return jsonify({"Info" : "RSA Key with {} Generated".format(secret_path)})
                else:
                    return jsonify({"Info": "Key was exsits"})

            if key_type == "aes":
                if hsm.gen_aes(secret_path,secret_version):
                    return jsonify({"Info" : "AES Key with {} Generated".format(secret_path)})
                else:
                    return jsonify({"Info": "Key was exsits"})

    return jsonify({"Error":"key type was not supported \n"})


@app.route("/key/encrypt/<key_type>",methods=['GET', 'POST'])
def encryptit():
    pass

@app.route("/key/decrypt/<key_type>",methods=['GET', 'POST'])
def decryptit():
    pass

@app.route("/key/sign")
def signit():
    pass

@app.route("/key/verify")
def verifyit():
    pass

@app.errorhandler(500)
def internal_error(error):
    print(str(error))

@app.errorhandler(404)
def not_found_error(error):
    print(str(error))

@app.errorhandler(405)
def not_allowed_error(error):
    print(str(error))

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port = int(8080))

    # serve(app, host="0.0.0.0", port=8080)