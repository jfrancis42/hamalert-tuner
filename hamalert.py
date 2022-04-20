#!/usr/bin/env python3
# coding: utf-8

import xmlrpc.client
import json
import time
from flask import Flask
from flask_restful import Resource, Api, reqparse

s=xmlrpc.client.ServerProxy('http://127.0.0.1:12345')
print("Connected to: "+s.rig.get_xcvr())

app=Flask(__name__)
api=Api(app)

def set_mode(mode):
    s.rig.set_mode(mode.upper())

def set_freq(hz):
    s.rig.set_vfo(hz*1.0)
    
class Users(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('fullCallsign',required=False)
        parser.add_argument('callsign',required=False)
        parser.add_argument('frequency',required=False)
        parser.add_argument('band',required=False)
        parser.add_argument('mode',required=False)
        parser.add_argument('modeDetail',required=False)
        parser.add_argument('time',required=False)
        parser.add_argument('dxcc',required=False)
        parser.add_argument('homeDxcc',required=False)
#        parser.add_argument('spotterDxcc',required=False)
        parser.add_argument('cq',required=False)
        parser.add_argument('continent',required=False)
        parser.add_argument('entity',required=False)
        parser.add_argument('homeEntity',required=False)
#        parser.add_argument('spotterEntity',required=False)
#        parser.add_argument('spotter',required=False)
#        parser.add_argument('spotterCq',required=False)
#        parser.add_argument('spotterContinent',required=False)
        parser.add_argument('rawText',required=False)
        parser.add_argument('title',required=False)
        parser.add_argument('comment',required=False)
        parser.add_argument('source',required=False)
        parser.add_argument('speed',required=False)
        parser.add_argument('snr',required=False)
        parser.add_argument('triggerComment',required=False)
        parser.add_argument('qsl',required=False)
        parser.add_argument('state',required=False)
#        parser.add_argument('spotterState',required=False)
        parser.add_argument('iotaGroupRef',required=False)
        parser.add_argument('iotaGroupName',required=False)
        parser.add_argument('summitName',required=False)
        parser.add_argument('summitHeight',required=False)
        parser.add_argument('summitPoints',required=False)
        parser.add_argument('summitRef',required=False)
        parser.add_argument('wwffName',required=False)
        parser.add_argument('wwffDivision',required=False)
        parser.add_argument('wwffRef',required=False)
        args=parser.parse_args()
        print(args)
        print("")
        print("Call: "+args['callsign'])
        print("Freq: "+args['frequency'])
        print("Mode: "+args['mode'])
        # SOTA
        if(args['source']=='sotawatch'):
            print("SOTA")
            print("Summit: "+args['summitRef']+" - "+args['summitName'])
            print("Points: "+args['summitPoints'])
        # POTA/WWFF
        if(args['wwffName'] or args['wwffDivision'] or args['wwffRef']):
            print("POTA/WWFF")
            print("Park: "+args['wwffDivision']+" - "+args['wwffRef']+" - "+args['wwffName'])
        # IOTA
        if(args['iotaGroupRef'] or args['iotaGroupName']):
            print("IOTA")
            print("Island: "+args['iotaGroupRef']+" - "+args['iotaGroupName'])
        #        if(args['mode'].upper() in s.rig.get_modes()):
        set_mode(args['mode'])
        set_freq(float(args['frequency'])*1000000.0)
        return({'n0gq':"73"},200)

api.add_resource(Users, '/hamalert')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8001,debug=True)

# Local Variables:
# mode: Python
# coding: utf-8
# End:
