#!/usr/bin/env python3
# coding: utf-8

import xmlrpc.client
import json
import time
import os
import logging
from flask import Flask
from flask_restful import Resource, Api, reqparse
from queue import Queue
from threading import Thread, Lock

f=open('config.json')
config=json.load(f)
f.close()

def set_mode(mode):
    s.rig.set_mode(mode.upper())

def set_freq(hz):
    s.rig.set_vfo(hz*1.0)
    
def set_volume(n):
    s.rig.set_verify_volume(n)

def get_volume():
    return(s.rig.get_volume())

def get_rig():
    return(s.rig.get_xcvr())

def tune():
    s.rig.tune()

class Hamalert(Resource):
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
        lock.acquire()
        q.put(parser.parse_args())
        lock.release()
        return({mycall:"73"},200)

def ha_listener(host,port):
    print("Starting network listener...")
    app.run(host,port,False)

if __name__ == '__main__':
    if(int(config['debug'])==0):
        debug=False
    else:
        debug=True
    if(int(config['auto_tune'])==0):
        auto_tune=False
    else:
        auto_tune=True
    mycall=config['call']
    mute_level=int(config['mute_level'])
    listen_time=int(config['listen_time'])

    last=0

    q=Queue()
    lock=Lock()

    s=xmlrpc.client.ServerProxy(f'http://{config["flrig_ip"]}:{str(config["flrig_port"])")
    listen_level=get_volume()
    if(listen_level==0):
        listen_level=15
    print(f"Radio: {get_rig()}")
    print(f"Volume: {str(listen_level)}")
    print()
    
    app=Flask(__name__)
    api=Api(app)
    api.add_resource(Hamalert, '/hamalert')

    t1=Thread(target=ha_listener,args=(config['server_listen_ip'],int(config['server_listen_port'])))
    t1.start()
    logging.getLogger('werkzeug').disabled = True
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'

    while(True):
        if(not(q.empty())):
            args=q.get()

            if(debug):
                print()
                print(args)
            if(args['mode'] and
               args['callsign'] and
               args['frequency'] and
               get_volume()==0):
                print()
                # SOTA
                if(args['source']=='sotawatch'):
                    print("SOTA")
                    print(f"Summit: {args['summitRef']} - {args['summitName']}")
                    print(f"Points: {args['summitPoints']}")
                # POTA/WWFF
                if(args['wwffName'] or args['wwffDivision'] or args['wwffRef']):
                    print("POTA/WWFF")
                    print(f"Park: {args['wwffDivision']} - {args['wwffRef']} - {args['wwffName']}")
                # IOTA
                if(args['iotaGroupRef'] or args['iotaGroupName']):
                    print("IOTA")
                    print(f"Island: {args['iotaGroupRef']} - {args['iotaGroupName']}")
                print(f"Call: {args['callsign']}")
                print(f"Freq: {args['frequency']}")
                print(f"Mode: {args['mode']}")
                if(args['entity']):
                    print(f"Entity: {args['entity']}")
                if(args['state']):
                    print(f"State: {args['state']}")
                mode=args['mode']
                if(mode=="ssb"):
                    if(float(args['frequency'])>10.0):
                        mode="usb"
                    else:
                        mode="lsb"
                set_mode(mode)
                set_freq(float(args['frequency'])*1000000.0)
                set_volume(listen_level)
                last=time.time()
                f=float(args['frequency'])
                if(auto_tune):
                    tune()

        time.sleep(0.5)
        if(int(time.time())-listen_time>last):
            if(get_volume()==listen_level):
                set_volume(mute_level)

# Local Variables:
# mode: Python
# coding: utf-8
# End:
