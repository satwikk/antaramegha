#!/usr/bin/python

import requests
from pprint import pprint
import json
import os

node_ip = "oscip.enlight.dev"
keystone_api = "https://%s:5000/v3/"%node_ip
neutron_api = "https://%s:9696"%node_ip

# Auth Creds for oscip.enlight.dev
#"""
user_name = os.environ["OS_USERNAME"]
user_password = os.environ["OS_PASSWORD"]
project_id = "need to fetch from project list"
domain = "need to fecth from domain list"
#"""

# Check for basic API connectivity
print("\n---------------------- Check for basic API connectivity")
print("\n** API URL for checking API Connectivity - \n\tType : GET, URL : " + keystone_api)
keystone_response = requests.get(keystone_api).content
print( "\n** Base API endpoint response : ")
pprint(json.loads(keystone_response))
print("\n----------------------")

# Get token
print("\n---------------------- User Authentication and Token Generation")

# Auth Data payload for unscoped token
#auth_user_data = { "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "name": user_name, "password": user_password, "domain": { "name": domain } } } }, "scope": { "project": { "name": project_id } } } }

# Auth Data payload for project scoped token
auth_user_data = { "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "name": user_name, "password": user_password, "domain": { "name": domain } } } }, "scope": { "project": { "id": project_id } } } }
print("\n** Data Payload for project Scoped token generation request : ")
pprint(auth_user_data)

auth_user_data = json.dumps(auth_user_data)
auth_user_header = { "Content-Type" : "application/json" }
print("\n** Header Payload for Keystone API Calls (common for most of them) : ")
pprint(auth_user_header)

print("\n** API URL for Authenticate User / Generate Token request - \n\tType POST, URL : " + keystone_api + "auth/tokens")
auth_user_response = requests.post(keystone_api + "auth/tokens",data=auth_user_data,headers=auth_user_header)
auth_user_dict = json.loads(auth_user_response.content)

x_auth_token = auth_user_response.headers["X-Subject-Token"]
print("\n** Get Token successful : ", x_auth_token)
print("Issued at : %s, Expires at : %s"%(auth_user_dict["token"]["issued_at"],auth_user_dict["token"]["expires_at"]))

# Check for basic API connectivity for Neutron
print("\n---------------------- Check for basic API connectivity for Neutron")
print("\n** API URL for checking API Connectivity - \n\tType : GET, URL : " + neutron_api)
neutron_response = requests.get(neutron_api).content
print( "\n** Base API endpoint response : ")
pprint(json.loads(neutron_response))
print("\n----------------------")

nw_auth_user_header = { "Content-Type" : "application/json", "X-Auth-Token" : x_auth_token, "User-Agent" : "python-glanceclient" }
print "\n** Header Payload for common Neutron operations : "
pprint(nw_auth_user_header)


print("\n---------------------- Get basic v2.0 API details")
print("\n** API URL for checking API Connectivity - \n\tType : GET, URL : " + neutron_api)
neutron_response = requests.get(neutron_api + "/v2.0/", headers=nw_auth_user_header).content
print( "\n** Base API endpoint response : ")
pprint(json.loads(neutron_response))
print("\n----------------------")

print("\n---------------------- Get List of Floating IPs")
print("\n** API URL to get list of Floating IPs - \n\tType : GET, URL : " + neutron_api + "/v2.0/floatingips")
neutron_response = requests.get(neutron_api + "/v2.0/floatingips", headers=nw_auth_user_header).content
print( "\n** Base API endpoint response : ")
pprint(json.loads(neutron_response))
print("\n----------------------")

