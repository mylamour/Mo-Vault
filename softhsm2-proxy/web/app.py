import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, send_file, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename
from waitress import serve
from src import HSM, Svault, int_to_bytes, hex_to_bytes
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.exceptions import PinIncorrect, NoSuchKey, NoSuchToken, MultipleObjectsReturned

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_KEY_TYPS= ["rsa", "aes"]
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf','word','ppt','txt'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
    - key_type
    - secret_path
    - secret_version
    - payload
    - iv
"""

SLOT = os.environ.get("TOKENLABEL")
PIN = os.environ.get("PINSECRET")

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

hsm = HSM(slot=SLOT, pin=PIN) # it should be managed as session

_VERSION = 0.1

@app.route("/")
def hello():
    return "Weclome!"
    # routes = []
    # for route in app.url_map.iter_rules():
    #     routes.append('%s' % route)
    # all_indexs = "\n".join(sorted(routes))

    # return all_indexs

@app.route("/gen/key/<key_type>", methods=['GET', 'POST'])
def genkey(key_type):
    """
        curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"random_test/zhao", "secret_version":"1"}' http://127.0.0.1:8080/gen/key/aes
    """
    if key_type in ALLOWED_KEY_TYPS:
        if request.method == 'GET':
            return jsonify({"Info":"we only support rsa & aes, please use post method"})

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
def encryptit(key_type):
    if key_type in ALLOWED_KEY_TYPS:
        if request.method == 'GET':
            return jsonify({"Info":"we only support rsa & aes, please use post method"})

        if request.method == 'POST':
            secret_path = request.json['secret_path']
            secret_version = int(request.json['secret_version'])
            plaintext = request.json['plaintext']
        
            if key_type == "rsa":
                pub, _ = hsm.get_rsa(secret_path,secret_version)
                pubV = Svault(pub)
                _, ciphertext = pubV.encrypt(plaintext)
                if pub:
                    return jsonify({"ciphertext" : "{}".format(ciphertext)})
                else:
                    return jsonify({"Info": "Key was not exsits"})

            if key_type == "aes":
                aes = hsm.get_aes(secret_path, secret_version)
                aesV = Svault(aes)
                if aes:
                    iv, ciphertext = aesV.encrypt(plaintext)
                    return jsonify({"iv": iv, "ciphertext": "{}".format(ciphertext)})
                else:
                    return jsonify({"Info": "Key not was exsits"})

    return jsonify({"Error":"key type was not supported \n"})


@app.route("/key/decrypt/<key_type>",methods=['GET', 'POST'])
def decryptit(key_type):
    if key_type in ALLOWED_KEY_TYPS:
        if request.method == 'GET':
            return jsonify({"Info":"we only support rsa & aes, please use post method"})

        if request.method == 'POST':
            secret_path = request.json['secret_path']
            secret_version = int(request.json['secret_version'])
            ciphertext = request.json['ciphertext']
        
            if key_type == "rsa":
                priv = hsm.get_rsa(secret_path,secret_version,keypairs="private")
                privV = Svault(priv)

                if priv:
                    plaintext = privV.decrypt(ciphertext)
                    return jsonify({"plaintext" : "{}".format(plaintext)})
                else:
                    return jsonify({"Info": "Key was not exsits"})

            if key_type == "aes":
                oiv = request.json['iv']
                aes = hsm.get_aes(secret_path, secret_version)
                if aes:
                    plaintext = Svault(aes).decrypt(ciphertext,iv=oiv)
                    return jsonify({"plaintext" : "{}".format(plaintext)})
                else:
                    return jsonify({"Info": "Key not was exsits"})
    return jsonify({"Error":"key type was not supported \n"})


@app.route("/key/sign/<payload_type>",methods=['GET', 'POST'])
def signit(payload_type):
    if request.method == 'GET':
        return jsonify({"Info":"Sign only support rsa , please use post method"})

    if request.method == 'POST':

        if payload_type == "message":
            secret_path = request.json['secret_path']
            secret_version = int(request.json['secret_version'])
            payload = request.json['data']

        if payload_type == "file":
            secret_path = request.form['secret_path']
            secret_version = int(request.form['secret_version'])
            ufile = request.files['data']

            if ufile and allowed_file(ufile.filename):
                payload = ufile.read()

        priv = hsm.get_rsa(secret_path,secret_version,keypairs="private")
        signature = Svault(priv).sign(payload)

        return jsonify({"signature" : signature })
    
    return jsonify({"Error":"I don't know what happended now\n"})

@app.route("/key/verify/<payload_type>",methods=['GET', 'POST'])
def verifyit(payload_type):
    if request.method == 'GET':
        return jsonify({"Info":"Sign only support rsa , please use post method"})

    if request.method == 'POST':

        if payload_type == "message":
            secret_path = request.json['secret_path']
            secret_version = int(request.json['secret_version'])
            signature = request.json['signature']

            payload = request.json['data']

        if payload_type == "file":
            secret_path = request.form['secret_path']
            secret_version = int(request.form['secret_version'])
            signature = request.form['signature']

            ufile = request.files['data']

            if ufile and allowed_file(ufile.filename):
                payload = ufile.read()


        pub = hsm.get_rsa(secret_path,secret_version,keypairs="public")

        result = Svault(pub).verify(payload,signature)
        
        return jsonify({"Verify Result" : result })

    return jsonify({"Error":"I don't know what happended now\n"})

@app.route("/download")

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
    # app.debug = True
    # app.run(host="0.0.0.0",port = int(8080))
    serve(app, host="0.0.0.0", port=8443)