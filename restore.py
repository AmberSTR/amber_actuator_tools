#!/usr/bin/python
# -*- coding: UTF-8 -*-
import amber_actuator as a
import sys, getopt
import json
import datetime


def setFromFile(data, actuatorID, ipaddr="127.0.0.1", safemode=1):
    wroteSuccessFlag = 0
    wroteErrorFlag = 0

    j = a.AmberActuator(int(actuatorID), ipaddr)
    j.position.kp = float(data['Position']['Kp'])
    j.position.ki = float(data['Position']['Ki'])
    j.position.up_limit = float(data['Position']['UpLimit'])
    j.position.down_limit = float(data['Position']['DownLimit'])
    j.speed.kp = float(data['Speed']['Kp'])
    j.speed.ki = float(data['Speed']['Ki'])
    j.speed.acceleration = float(data['Speed']['Acceleration'])
    j.speed.deceleration = float(data['Speed']['Deceleration'])
    j.speed.speed_limit = float(data['Speed']['SpeedLimit'])
    j.current.kp = float(data['Current']['Kp'])
    j.current.ki = float(data['Current']['Ki'])
    j.current.current_limit = float(data['Current']['CurrentLimit'])

    outputData = [j.position.kp,
                  j.position.ki,
                  j.position.up_limit,
                  j.position.down_limit,
                  j.speed.kp,
                  j.speed.ki,
                  j.speed.acceleration,
                  j.speed.deceleration,
                  j.speed.speed_limit,
                  j.current.kp,
                  j.current.ki,
                  j.current.current_limit
                  ]
    inputData = [float(data['Position']['Kp']),
                 float(data['Position']['Ki']),
                 float(data['Position']['UpLimit']),
                 float(data['Position']['DownLimit']),
                 float(data['Speed']['Kp']),
                 float(data['Speed']['Ki']),
                 float(data['Speed']['Acceleration']),
                 float(data['Speed']['Deceleration']),
                 float(data['Speed']['SpeedLimit']),
                 float(data['Current']['Kp']),
                 float(data['Current']['Ki']),
                 float(data['Current']['CurrentLimit'])]
    if safemode == "0":
        j.attribute.gear = int(data['Attribute']['Gear'])
        j.attribute.pole_number = int(data['Attribute']['PoleNumber'])
        inputData.append(float(data['Attribute']['Gear']))
        inputData.append(float(data['Attribute']['PoleNumber']))
        outputData.append(j.attribute.gear)
        outputData.append(j.attribute.pole_number)
    for i in range(len(inputData)):
        outputData[i] = inputData[i]
    for i in range(len(outputData)):
        if outputData[i] == inputData[i]:
            print(" S ",end="")
            wroteSuccessFlag += 1
        else:
            print(" E ",end="")
            wroteErrorFlag += 1
    print("")
    print(f"Success = {wroteSuccessFlag}")

    print(f"Error = {wroteErrorFlag}")

def main(argv):
    actuatorID = -1
    t = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    inputFile = "null"
    ipaddr = "127.0.0.1"
    safemode = 1
    try:
        opts, args = getopt.getopt(argv, "h:j:i:a:s:", ["actuator=", "ifile=", "ipaddr=", "safemode="])
    except getopt.GetoptError:
        print('restore.py --j <jointID(actuatorID)> -i <inputfile> -a <ipAddress>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('restore.py  -j <jointID(actuatorID)> -i <inputfile> -a <ipAddress>')
            sys.exit()
        elif opt in ("-j", "--actuator"):
            actuatorID = arg
        elif opt in ("-i", "--ifile"):
            inputFile = arg

        elif opt in ("-a", "--ipaddr"):
            ipaddr = arg
        elif opt in ("-s", "--safemode"):
            safemode = arg

    f = open(inputFile)

    data = json.load(f)

    if actuatorID == -1:
        print(f"No input ActuatorID, using ID from file")
        actuatorID = data['Attribute']['ActuatorID']
        print(f"ActuatorID = {actuatorID}")
    else:
        print("Using ActuatorID from file: ")
        print(f"ActuatorID = {actuatorID}")
    if safemode != "0":
        print("Safemode is on, Gear and PoleNumber won't be changed.")
    else:
        print("Safemode is off, Gear and PoleNumber will be changed.")
    print(f"Restore Parameter from  {inputFile} to actuator {actuatorID}")

    setFromFile(data, actuatorID, ipaddr, safemode=safemode)

    # Closing file
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
