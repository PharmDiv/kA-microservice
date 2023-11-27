import requests
import re
import json
from flask import Flask, request, jsonify
from Subscriptions.subscription import create_subscription
from Subscriptions.Process_subscriptions.process import extract_reference_values
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


#GET/POST plan Definition
@app.route('/PlanDefinition', methods=['GET', 'POST'])
def route_plandefinition():
    base_url = os.getenv("data_source")
    headers = {"Content-Type": "application/json"}
    if request.method == 'GET':
        #Get PlanDefinition from lafia fhirserver
        response = requests.get(url = f"{base_url}/PlanDefinition", headers=headers)
        return (response.json())  
    if request.method == 'POST':
        #Validate if this is a knowedge artifact plandefinition before sending to fhir server
        #If valid POST
        trigger = request.json["action"][0]["trigger"][0]['extension'][0]['valueCodeableConcept']['coding'][0]['code']
        pd_id = request.json['id']
        pd_status = request.json['status']
        apisix_gateway = os.getenv("apisix_gateway")
        requests.post(url=f"{base_url}/Subscription", headers=headers, data=create_subscription(pd_status, trigger, apisix_gateway))
        response = requests.post(url = f"{base_url}/PlanDefinition", headers=headers, data= json.dumps(request.json))
        return jsonify(response.json()), 201


#GET/PUT/DELETE specific plandefinition
@app.route('/PlanDefinition/<id>', methods=['GET', 'PUT', 'DELETE'])
def route_plandefinition_id(id):
    base_url = os.getenv("data_source")
    headers = {"Content-Type": "application/json"}
    if request.method == 'GET':
        response = requests.get(url = f"{base_url}/PlanDefinition/{id}", headers=headers)
        return (response.json())  
    if request.method == 'PUT':
        trigger = request.json["action"][0]["trigger"][0]['extension'][0]['valueCodeableConcept']['coding'][0]['code']
        pd_id = request.json['id']
        pd_status = request.json['status']
        apisix_gateway = os.getenv("apisix_gateway")
        requests.post(url=f"{base_url}/Subscription", headers=headers, data=create_subscription(pd_status, trigger, apisix_gateway))
        response = requests.put(url = f"{base_url}/PlanDefinition/{id}", headers=headers, data= json.dumps(request.json))
        return jsonify(response.json()), 201
    if request.method == 'DELETE':
        response = requests.delete(url = f"{base_url}/PlanDefinition/{id}", headers=headers)
        return jsonify(response.json())
    #Create neccessary subscriptions #Use trigger codes from pd ka


if __name__ == '__main__':
    app.run(debug=True)
