import os
from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import pprint
import json

idInstance=7103846733
apiTokenInstance = "d9bd0740cec34b92bec7f06d2b4e0182bef74eb6af5e4f969a"
message = f'I use Green-API to send this message to you!'
phoneNumber = 77058217951
phoneNumber2 = 79642920400

urlFile = "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187.jpg"
urlFile = "https://media.tenor.com/e1foxy6gXgsAAAAC/kazakhstan-nyan-cat.gif"

app = Flask(__name__)
app.secret_key = '83576937509357'


@app.route('/')
def index():
    return render_template('index.html', idInstance=idInstance, apiTokenInstance=apiTokenInstance, phoneNumber=phoneNumber, phoneNumber2=phoneNumber2, message=message,urlFile=urlFile)


@app.route('/handle_action', methods=['POST'])
def handle_action():
    global idInstance, apiTokenInstance, phoneNumber, phoneNumber2, message, urlFile

    instance_id = request.form.get('idInstance', default=idInstance)
    token = request.form.get('apiTokenInstance', default=apiTokenInstance)
    phoneNumber = request.form.get('phoneNumber', default = phoneNumber)
    phoneNumber2 = request.form.get('phoneNumber2', default = phoneNumber2)

    message = request.form.get('message', default = message)
    urlFile = request.form.get('urlFile', default = urlFile)
    action = request.form['action']



    if action == "GetSettings":
        instance_id = request.form.get('idInstance', default=idInstance)
        token = request.form.get('apiTokenInstance', default=apiTokenInstance)
        url = fr"https://api.green-api.com/waInstance{instance_id}/getSettings/{token}"
        payload = {}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=payload)
        return render_template('index.html', result=pprint.pformat (response.text), idInstance=instance_id, apiTokenInstance=token,message=message,phoneNumber=phoneNumber,urlFile=urlFile)


    elif action == "GetStateInstance":
        instance_id = request.form.get('idInstance', default=idInstance)
        token = request.form.get('apiTokenInstance', default=apiTokenInstance)
        url = fr"https://api.green-api.com/waInstance{instance_id}/getStateInstance/{token}"
        payload = {}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=payload)
        return render_template('index.html', result=response.text, idInstance=instance_id, apiTokenInstance=token,message=message,phoneNumber=phoneNumber,urlFile=urlFile)

    elif action == "SendMessage":
        instance_id = request.form.get('idInstance', default=idInstance)
        token = request.form.get('apiTokenInstance', default=apiTokenInstance)
        phoneNumber = request.form.get('phoneNumber', default=phoneNumber)
        phoneNumber2 = str(request.form.get('phoneNumber2', default=phoneNumber))
        message = request.form.get('message', default=message)
        url = fr"https://api.green-api.com/waInstance{instance_id}/sendMessage/{token}"
        payload = f'{{\r\n\t\"chatId\": \"{phoneNumber}@c.us\",\r\n\t\"message\": \"{message}"\r\n}}'
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return render_template('index.html', result=response.text, idInstance=instance_id, apiTokenInstance=token,message=message,phoneNumber=phoneNumber,phoneNumber2=phoneNumber2,urlFile=urlFile)

    elif action == "SendFileByUrl":
        instance_id = request.form.get('idInstance', default=idInstance)
        token = request.form.get('apiTokenInstance', default=apiTokenInstance)
        phoneNumber = request.form.get('phoneNumber', default=phoneNumber)
        phoneNumber2 = str(request.form.get('phoneNumber2', default=phoneNumber))
        # message = request.form.get('message', default=message)
        urlFile = request.form.get('urlFile', default=urlFile)
        url = fr"https://api.green-api.com/waInstance{instance_id}/sendFileByUrl/{token}"
        fileName = urlFile.split("/")[-1:][0]
        caption = fileName.split(".")[:1][0]
        chatId = str(phoneNumber2) + '@c.us'
        payload = {"chatId": f"{chatId}",
                   "urlFile": f"{urlFile}",
                   "fileName": f"{fileName}",
                   "caption": f"{caption}"
                   }
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        return render_template('index.html', result=response.text, idInstance=instance_id, apiTokenInstance=token,message=message,phoneNumber=phoneNumber,phoneNumber2=phoneNumber2,urlFile=urlFile)


    return "Unknown action"





if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
