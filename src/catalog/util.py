#!/usr/local/bin/python
# -*- coding: utf-8 -*-

""" Module providing utility functions to access catalog:
- to register
- to get information regarding the broker
"""
import requests
import json
import time
from classes import IamAlive

def registration(conf):
    # Retrieving catalog URL to register to it
    url = conf["catalog"]["URL"] + conf["catalog"]["registration"]["URI"]
    # Retrieving the payload expected by the catalog
    payload = conf["catalog"]["registration"]["expected_payload"]
    # Retrieving the interval of time at which our actor should communicate
    # with the catalog
    interval = conf["catalog"]["registration"]["interval"]
    
    # Starting to send registration messages to catalog
    IamAlive(url, payload, interval)

def getBroker(conf):
    # Retrieving catalog URL to get information regarding broker
    url = conf["catalog"]["URL"] + conf["catalog"]["broker"]["URI"]
    # Request's header
    headers = conf["catalog"]["broker"]["headers"]
    # Making the request
    r = requests.get(url, headers=headers)
    broker = json.loads(r.content.decode("utf-8", "ignore"))

    return broker["host"], broker["port"]

def getNextActorRequirements(conf):
    # Retrieving catalog URL to get information regarding broker
    url = conf["catalog"]['URL']

    # Taking the parameters list
    params = []
    for req in conf["catalog"]['next_actor']['params']:
        params.append(req)

    # Request's header     
    headers = conf['catalog']['next_actor']['headers']

    # Making the requests
    url = conf["catalog"]["URL"] + conf["catalog"]["next_actor"]["URI"]
    requirements = {}

    while len(params) > 0:
        param = params.pop()
        
        r = requests.get(url, params=param, headers=headers)
        
        response = json.loads(r.content.decode("utf-8", "ignore"))

        if response['status'] == 'success':
            requirements[param['ID']] = response['requirements']
        elif response['status'] == 'failure':
            params.append(param)
            time.sleep(1)
    
    return requirements