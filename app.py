#!/usr/local/bin/python
#
# -*- Coding: UTF-8 -*-
#coding: utf-8
# Autor: Iaslan Nascimento
# Inicio: 23/03/2020
# Fim:
# Objetivo: Código base para a API de OCR
# API Flak, leitura de imagem web , envio da mensagem para armazenamento, Envio para processar


from flask import Flask, request, Response, jsonify, make_response
#import json
#import matplotlib.pyplot as plt
from cv2 import cv2
import pytesseract
import numpy as np
import io
import time
import pytz
import base64
import os
from datetime import datetime, timezone
from PIL import Image
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
print(os.getcwd())
#from comparaResultado import comparaResultados
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
#REPOSITORY = '/home/imd.joao/evidencias/'
#RUNNING = {}

# API FLASK
@app.route('/')
def hello():
    return '<h1>API de OCR</h1>'

# função para pegar a imagem web
@app.route('/classify', methods=['POST'])
def init_importer():
    # lendo o json
    json_file = request.get_json()
    idXMLUFED = json_file["idArquivo"]
    bs64 = json_file["base64"]
    #bs64 = bs64.split(',')[1]

    # carregando a imagem
    im_data = base64.b64decode(bs64)
    image = Image.open(io.BytesIO(im_data))  # PIL
    im2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    #plt.imshow(im2)
    #plt.show()

    try:

        # ajuste de tamanho
        im5 = cv2.resize(im2, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

        # blur
        im6 = cv2.medianBlur(im5, 3)

        result = pytesseract.image_to_string(im6)
        #print(result)

        return jsonify(
            {
                "idArquivo": idXMLUFED,
                "tipo": "ocr-api",
                "dataProcessamento": datetime.now(pytz.utc).isoformat(),
                "propriedades": {
                    "texto" : result
                },
                "resultados": []
            }
        )

    except Exception as err:
        print(err)
        return "Error"


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('./Certificates/cert.pem', './Certificates/key.pem'))
