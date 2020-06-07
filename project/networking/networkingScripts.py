import subprocess, os
from project.networking.displayConnections import displayConnection


def displayNetworkInterface():
    command = " ls /sys/class/net > /tmp/networkInterface"
    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Connnections ")

    deviceFile = open('/tmp/networkInterface', 'rt')
    device = deviceFile.read()
    device2 = device.splitlines()
    return device2


def fillTable():
    command = 'nmcli connection show > /tmp/listConnection  '

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Connnections ")

    with open('/tmp/listConnection') as f:
        lineList = f.readlines()
    lineList.pop(0)
    print(lineList)


def upConnection(connectionName):
    fullCommand = f'nmcli connection up {connectionName}'
    try:
        subprocess.run(fullCommand, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Connnections ")


def downConnection(connectionName):
    fullCommand = f'nmcli connection down {connectionName}'
    try:
        subprocess.run(fullCommand, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Connnections ")


def currentlyActiveConnection(con):
    con = str(con)
    command = " nmcli connection show --active > /tmp/activeNow"
    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Connnections ")

    File = open('/tmp/activeNow', 'rt')
    conFile = File.read()
    if conFile in con:

        return True
    else:
        return False


def currentlyActiveConnectionNow():
    output = displayConnection()
    list = []
    list.append(output[0])
    return list[0]


def AutoConnection(connectionName, par):
    fullCommand = f'nmcli connection modify {connectionName} autoconnect {par} '
    os.system(fullCommand)


def showIpMethod(con):
    fullCommand = f'nmcli connection  show {con}  | grep -F ipv4.method >  /tmp/ConIpMethod2'
    try:
        subprocess.run(fullCommand, check=True, shell=True)

    except subprocess.CalledProcessError:
        return None
    File = open('/tmp/ConIpMethod2', 'rt')
    txt = File.read()
    con = txt.strip()
    con = con.replace("ipv4.method:", "-")
    # con = con.replace(":", "")
    con = con.replace("-", "")
    con = con.strip()
    return con


def isActivated(connectionName):
    command = f'nmcli connection show {connectionName} |grep -F GENERAL.STATE:  > /tmp/isActivated '
    os.system(command)
    File = open('/tmp/isActivated', 'rt')
    txt = File.read()
    txt = txt.rstrip()
    x = str(txt.find("activated"))
    if (x == -1):
        return False

    else:
        return True


def globalInof(con):
    j = con
    num = '11'
    cm1 = 'nmcli connection  show {} | grep -F connection.id:  >  /tmp/info-{}-'.format(j, num)
    cm2 = 'nmcli connection  show {} | grep -F connection.type:  >> /tmp/info-{}-'.format(j, num)
    cm5 = 'nmcli connection  show {} | grep -F ipv4.method:  >> /tmp/info-{}-'.format(j, num)
    cm3 = 'nmcli connection  show {} | grep -F GENERAL.DEVICES: >> /tmp/info-{}-'.format(j, num)
    cm4 = 'nmcli connection  show {} | grep -F GENERAL.STATE: >> /tmp/info-{}-'.format(j, num)
    cm7 = 'nmcli connection  show {} | grep -F connection.autoconnect: >> /tmp/info-{}-'.format(j, num)
    cm8 = 'nmcli connection  show {} | grep -F connection.autoconnect-priority:  >> /tmp/info-{}-'.format(j, num)
    try:
        os.system(cm1)
        os.system(cm2)
        os.system(cm3)
        os.system(cm5)
        # os.system(cm6)
        os.system(cm4)
        os.system(cm7)
        os.system(cm8)

    except os.error:
        return None

    f = open(f'/tmp/info-{num}-', 'rt')
    f = f.read()
    try:
        fullCommand = f'rm -rf /tmp/info-{num}-'
        subprocess.run(fullCommand, check=True, shell=True)

    except subprocess.CalledProcessError:
        return None

    f = f.replace('ipv4.method', ',')
    f = f.replace('connection.type:', ',')
    f = f.replace('IP4.ADDRESS[1]:', ',')
    f = f.replace('ipv4.addresses', ',')
    f = f.replace('  ', '')
    f = f.replace(':', '')
    f = f.replace('802-3-ethernet', 'ethernet')
    f = f.replace('802-11-wireless', 'wifi')
    f = f.replace('GENERAL.STATE', ',')
    f = f.replace('GENERAL.DEVICES', ',')
    f = f.replace('connection.id', 'connection.id,')
    f = f.replace('connection.autoconnect', ',')
    f = f.replace('connection.autoconnect-priority', ',')
    f = f.replace('\n', '')
    ff = f.split('connection.id,')
    ff.pop(0)
    set = (ff)
    return set


def globalInofslice():
    f = globalInof()
    output = displayConnection()
    for i in range(len(f)):
        print(f[i])
