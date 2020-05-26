import subprocess, os

from networking.displayConnections import *
'''

def displayConnection():
    command = 'nmcli connection show > /tmp/listConnection  '

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Connnections ")

    with open('/tmp/listConnection') as f:
        lineList = f.readlines()
    lineList.pop(0)
    con = []
    conAre = ''
    for i in lineList:
        conAre += str(i[0:20])
        conAre += '::'
        con.append(str(i[0:20]))
    conAreor = conAre
    conAreor = conAreor.split(':')
    c = ''
    for i in conAre:
        c += i
    c2 = c.replace('  ', '')
    c2 = c2.replace(' ', '\s')
    c2 = c2.replace('s', ' ')
    c2 = c2.replace("\ ::", ',,,')
    c2 = c2.replace('::', ',,,')
    c2 = c2.strip()
    c2 = c2.split(",,,")
    return (c2)
'''

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
    con=str(con)
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
    output=displayConnection()
    list=[]
    list.append(output[0])
    return list[0]


def AutoConnection(connectionName, par):
    fullCommand = f'nmcli connection modify {connectionName} autoconnect {par} '
    os.system(fullCommand)


#########################################################################
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

'''
def displayIP(connectionName):
    if showIpMethod(connectionName) == 'manual':
        fullCommand = f'nmcli connection  show {connectionName}| grep -F ipv4.addresses: > /tmp/ipAddress'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        # fullCommand = f'cat /etc/sysconfig/network-scripts/ifcfg-{connectionName}| grep -F DNS2 > /tmp/dns2'
        # os.system(fullCommand)

        fullCommand = f'nmcli connection  show {connectionName}| grep -F ipv4.gateway: > /tmp/gateway'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        fullCommand = f'nmcli connection  show {connectionName}| grep -F ipv4.dns:  > /tmp/dns1'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        File = open('/tmp/dns1', 'rt')
        txt = File.read()
        dns1 = txt.strip()
        dns = dns1.replace("ipv4.dns:", "-")
        dns = dns.replace(":", "")
        dns = dns.replace("-", "")
        dns = dns.strip()

        File = open('/tmp/ipAddress', 'rt')
        txt = File.read()
        ipAddress = txt.strip()
        ipAddress = ipAddress.replace("   ", ":")
        ipAddress = ipAddress.replace("ipv4.addresses:", "-")
        ipAddress = ipAddress.replace(":", "")
        ipAddress = ipAddress.replace("-", "")
        ipAddress = ipAddress.strip()

        File = open('/tmp/gateway', 'rt')
        txt = File.read()
        gateway = txt.strip()
        gateway = gateway.replace("ipv4.gateway:", "-")
        gateway = gateway.replace(":", "")
        gateway = gateway.replace("-", "")
        gateway = gateway.strip()

        File = open('/tmp/dns2', 'rt')
        txt = File.read()
        mask = txt.rstrip()
        dns2 = mask.replace("PREFIX=", "  ")

        coninfo = ipAddress + '-' + gateway + '-' + dns
        coninfo = coninfo.split("-")
        print(coninfo)

    else:

        fullCommand = f'nmcli connection  show {connectionName}| grep -F IP4.ADDRESS[1]: > /tmp/ipAddress2'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        # fullCommand = f'cat /etc/sysconfig/network-scripts/ifcfg-{connectionName}| grep -F DNS2 > /tmp/dns2'
        # os.system(fullCommand)

        fullCommand = f'nmcli connection  show {connectionName}| grep -F  IP4.GATEWAY: > /tmp/gateway2'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        fullCommand = f'nmcli connection  show {connectionName}| grep -F  IP4.DNS[1]:  > /tmp/dns12'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        fullCommand = f'nmcli connection  show {connectionName}| grep -F  IP4.DNS[2]:  > /tmp/dns22'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        File = open('/tmp/ipAddress2', 'rt')
        txt2 = File.read()
        ip = txt2.strip()
        ip = ip.replace("IP4.ADDRESS[1]:", "-")
        ip = ip.replace(":", "")
        ip = ip.replace("-", "")
        ip = ip.strip()

        File = open('/tmp/dns12', 'rt')
        txt1 = File.read()
        dns1 = txt1.strip()
        dns1 = dns1.replace("IP4.DNS[1]:", "-")
        dns1 = dns1.replace(":", "")
        dns1 = dns1.replace("-", "")
        dns1 = dns1.strip()

        File = open('/tmp/gateway2', 'rt')
        txt3 = File.read()
        gatway = txt3.strip()
        gatway = gatway.replace("IP4.GATEWAY:", "-")
        gatway = gatway.replace(":", "")
        gatway = gatway.replace("-", "")
        gatway = gatway.strip()

        File = open('/tmp/dns22', 'rt')
        txt4 = File.read()
        dns2 = txt4.strip()
        dns2 = dns2.replace("IP4.DNS[2]:", "-")
        dns2 = dns2.replace(":", "")
        dns2 = dns2.replace("-", "")
        dns2 = dns2.strip()

        coninfo2 = ip + '-' + gatway + '-' + dns1 + ',' + dns2
        coninfo2 = coninfo2.split("-")
        print(coninfo2)

'''
####################"
###########"
##############


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
        #os.system(cm6)
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
    f= f.replace('connection.id', 'connection.id,')
    f= f.replace('connection.autoconnect', ',')
    f= f.replace('connection.autoconnect-priority', ',')
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




'''
def globalInfo():

    output=displayConnection()
    output.pop()
    turn=0
    for j in output:
        cm1 ='nmcli connection  show {} | grep -F connection.id:  >  /tmp/info-{}-'.format(j,output.index(j))
        cm2='nmcli connection  show {} | grep -F connection.type:  >> /tmp/info-{}-'.format(j,output.index(j))
        cm5='nmcli connection  show {}  | grep -F ipv4.method:  >> /tmp/info-{}-'.format(j,output.index(j))
        cm3 = 'nmcli connection  show {} | grep -F GENERAL.DEVICES: >> /tmp/info-{}-'.format(j, output.index(j))
        cm4 = 'nmcli connection  show {} | grep -F GENERAL.STATE: >> /tmp/info-{}-'.format(j, output.index(j))
        cm7 = 'nmcli connection  show {} | grep -F  connection.autoconnect: >> /tmp/info-{}-'.format(j, output.index(j))
        cm6=''
        if showIpMethod(j)=='auto':
            cm6='nmcli connection  show {}| grep -F IP4.ADDRESS[1]: >> /tmp/info-{}-'.format(j,output.index(j))
        else:
            cm6='nmcli connection  show {}| grep -F ipv4.addresses: >> /tmp/info-{}-'.format(j,output.index(j))

        try:
            os.system(cm1)
            os.system(cm2)
            os.system(cm5)
            os.system(cm7)
            #os.system(cm6)
            #os.system(cm3)
            #os.system(cm4)
        except os.error:
            return None
    c=[]
    cs=''
    try:
        fullCommand='rm -rf /tmp/allGlobalCon'
        subprocess.run(fullCommand, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Data ")

    for i in range(len(displayConnection())-1):
        f=open(f'/tmp/info-{i}-','rt')
        f=f.read()
        all=open('/tmp/allGlobalCon','a')
        all.write(f)
        all.close()
        try:
            fullCommand = f'rm -rf /tmp/info-{i}-'
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")


    f=open('/tmp/allGlobalCon','rt')
    f=f.read()
    f=f.replace('ipv4.method',',')
    f=f.replace('connection.type:',',')
    f=f.replace('IP4.ADDRESS[1]:',',')
    f=f.replace('ipv4.addresses',',')

    f=f.replace('  ','')
    f=f.replace(':','')
    f=f.replace('802-3-ethernet','ethernet')
    f=f.replace('802-11-wireless','wifi')
    f=f.replace('GENERAL.STATE',',')
    f=f.replace('GENERAL.DEVICES',',')
    f=f.replace('connection.id',':')
    f=f.replace('\n','')
    here=f
    here=f.replace('GENERAL.DEVICES',',')
    here=f.replace('connection.autoconnect',',')

    File=open('/tmp/listCO','w')
    File.write(here)
    File.close()

    list_of_users = []
    with open("/tmp/listCO", mode='r') as passwd_content:
        passwd_content=passwd_content.read()
        each_user2 = passwd_content.split(":")
        each_user2.pop(0)
    for i in each_user2:

        k = i.split(',')
        list_of_users.append(k)

    return list_of_users

'''