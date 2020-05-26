'''/*
part services

ALL FUNCTIONS ARE WORKING CORRECTLY
THERE INS NOT INPUT VALIDATION
author:jawed


*/'''

import os,subprocess


def isEnable(name):
    name=str(name)
    command=f'systemctl is-enabled {name} >/tmp/isEnabled '
    os.system(command)
    File= open('/tmp/isEnabled', 'rt')
    txt = File.read()
    isEnable= txt.rstrip()
    if(isEnable=='enabled'):
        return True

    else:
         return False

def checkService(name):
    name+='d'
    command=f'sudo systemctl is-active {name} >/tmp/isActive '

    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")

    File= open('/tmp/isActive', 'rt')
    txt = File.read()
    isActive = txt.rstrip()
    if(isActive=='active'):

        print(isActive)
        print("service is running ")

    else:
        print(isActive)
        print("service is not running")


def enableServices(name):
    name = str(name)
    command = f'systemctl enable {name} 2>/dev/null  '
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")


def disableServices(name):
    name = str(name)
    command = f'systemctl disable {name} 2>/dev/null  '
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")


def startServices(name):
    name=str(name)
    command=f'systemctl start {name} 2>/dev/null  '
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")


def stopServices(name):
    name = str(name)
    command = f'systemctl stop {name} 2>/dev/null  '
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")

def reloadConfig(name):
    name += 'd.service'
    command = f'sudo systemctl reload {name} 2>/dev/null  '
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")

def listfailedServices():
    command = "sudo systemctl --failed --type=service |grep -vF LOAD| grep -vF SUB | grep -vF To | grep -vF Pass | awk '{print$1}' >/tmp/failedServices"
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")
    File = open('/tmp/failedServices', 'rt')
    txt = File.read()
    isfaild = str(txt.rstrip())

    if(isfaild=='0'):

        print('\n\nthere are not failed services are loaded\n\n')
    else:

        print(txt)


def listAllServices():
    units = []
    command = "systemctl list-units  --type=service --all |grep  -vF LOAD| grep -vF listed| grep -vF SUB | grep -vF To | grep -vF Pass  > /tmp/allServices"
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")
    File = open('/tmp/allServices', 'rt')
    string = File.read()
    string = string.replace("●", "")
    string = string.replace(".service", "")
    string = string.replace("loaded", ", loaded")
    string = string.replace("not-found", ", not-found")
    string = string.replace("active", ", active ,")
    string = string.replace("in, active", ", inactive")
    string = string.replace("running", "running ,")
    string = string.replace("exited", "exited ,")
    string = string.replace("dead", "dead ,")
    string = string.replace("LSB:", "")
    string = string.replace("\n", ":")
    list1 = string.split(':')

    for i in list1:
        i = i.replace("  ", "")
        i = i.split(',')
        units.append(i)

    units.pop()
    units.pop()
    units.pop()

    return units



