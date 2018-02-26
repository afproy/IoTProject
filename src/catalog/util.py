#!/usr/local/bin/python
# -*- coding: utf-8 -*-

""" Module providing utility functions to access catalog:

- to register
- to get information regarding the broker
"""
import requests
import json

from classes import IamAlive

def registration(conf):
    # Retrieving catalog URL to register to it
    url = conf["catalog"]["URL"] + conf["catalog"]["registration"]["URI"]
    # Retrieving the payload expected by the catalog
    payload = conf["catalog"]["registration"]["expected_payload"]
    # Retrieving the interval of time at which our actor should communicate
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
    url = conf["catalog"]["URL"] + conf["catalog"]["next_actor"]["URI"]
    # Request's params
    params = conf["catalog"]["next_actor"]["params"]
    # Request's header
    headers = conf["catalog"]["next_actor"]["headers"]
    # Making the request
    r = requests.get(url, params=params, headers=headers)

    requirements = json.loads(r.content.decode("utf-8", "ignore"))

    return requirements