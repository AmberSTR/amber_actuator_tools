#!/usr/bin/python
# -*- coding: UTF-8 -*-
import amber_actuator as a
import sys, getopt
import json
import datetime


def getFromActuator(actuatorID=1, ipaddr="127.0.0.1"):
    param = []
    j = a.AmberActuator(actuatorID,ipaddr)

    # param = [
    #    j.position.kp,
    #    j.position.ki,
    #    j.position.up_limit,
    #    j.position.down_limit,
    #    j.speed.kp,
    #    j.speed.ki,
    #    j.speed.acceleration,
    #    j.speed.deceleration,
    #    j.speed.speed_limit,
    #    j.current.kp,
    #    j.current.ki,
    #    j.current.current_limit,
    # ]
    dictparam = {
        'Attribute': {
            'ActuatorID': j.actuator_id,
            'Gear': j.attribute.gear,
            'PoleNumber': j.attribute.pole_number,
        },
        'Position': {
            'Kp': j.position.kp,
            'Ki': j.position.ki,
            'UpLimit': j.position.up_limit,
            'DownLimit': j.position.down_limit,
        },
        'Speed': {
            'Kp': j.speed.kp,
            'Ki': j.speed.ki,
            'Acceleration': j.speed.acceleration,
            'Deceleration': j.speed.deceleration,
            'SpeedLimit': j.speed.speed_limit,
        },
        'Current': {
            'Kp': j.current.kp,
            'Ki': j.current.ki,
            'CurrentLimit': j.current.current_limit,
        }
    }
    return dictparam


def main(argv):
    actuatorID = 1
    t = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    outputfile = t + '(' + str(actuatorID) + ')' + '.json'
    ipaddr = "127.0.0.1"
    try:
        opts, args = getopt.getopt(argv, "h:j:o:a:", ["actuator=", "ofile=", "ipaddr="])
    except getopt.GetoptError:
        print('backup.py -j <jointID(actuatorID)> -o <outputfile> -a <ipAddress>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('backup.py  -j <jointID(actuatorID)> -o <outputfile> -a <ipAddress>')
            sys.exit()
        elif opt in ("-j", "--actuator"):
            actuatorID = arg
            outputfile = t + '-j' + str(actuatorID) + '.json'

        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-a", "--ipaddr"):
            ipaddr = arg
    dictParam = getFromActuator(actuatorID=int(actuatorID), ipaddr=ipaddr)
    with open(outputfile, 'w', encoding='utf-8') as outfile:
        print(f"Backup Parameter from actuator {actuatorID} to {outputfile}")
        json.dump(dictParam, outfile, indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
