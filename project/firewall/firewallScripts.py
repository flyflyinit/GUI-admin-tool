import os,subprocess


def restarted():
    command = 'systemcte restart firewalld > /tmp/zones 2> /tmp/firewallZonesError'
    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Data ")

def listZones():
    command = 'firewall-cmd --get-zones > /tmp/firewallZones 2> /tmp/firewallZonesError'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Data ")


    file = open('/tmp/firewallZones', 'rt')
    file = file.read()
    zones =file.replace('\n',':')
    zones =zones.replace(' ',':')
    list=zones.split(':')
    list.pop()
    return list

def defaultZone():

    command = 'firewall-cmd --get-default-zone > /tmp/firDefZone 2> /tmp/firewalldefZoneError'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")


    file = open('/tmp/firDefZone', 'rt')
    file = file.read()
    default = file
    default = default.replace(' ', ':')
    default = default.replace('\n', ':')
    default = default.split(':')
    default.pop()
    return default


def activeZone():
    command = 'firewall-cmd --get-active-zones > /tmp/activeZone 2> /tmp/activeZoneError'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    file = open('/tmp/activeZone', 'rt')
    file = file.read()
    default=file.replace('\n',':')

    return default

def setDefaultZone(zone):

    command = f'firewall-cmd --set-default-zone={zone} '

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    restarted()

######################### RUN-TIME ####################################################################################################

# ADD NEW ZONE
def NewZone(name):

    name=str(name)
    command = f'firewall-cmd --new-zone={name}'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")

def addInterfaceToZone(interface, zone):
    command = f'firewall-cmd --zone={zone} --addinteface={interface}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    restarted()

def addServiceToDefaultZone(service):

    command = f'firewall-cmd  --add-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")


def addServiceToSpecificZone(service, zone):

    command = f'firewall-cmd --zone={zone} --add-service={service} > /tmp/state'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

def addPort(port, protocol):

    command = f'firewall-cmd  --add-port={port}/{protocol}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    restarted()
################################  --permanent   ##############################################################################

# add new zone

def addPermanentNewZone(name):
    name = str(name)
    command = f'firewall-cmd --permanent --new-zone={name}'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")


# add interface to zone

def addPermanentInterfaceToZone(interface, zone):
    command = f'firewall-cmd --permanent --zone={zone} --addinteface={interface}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    restarted()



def addPermanentServiceDefaultZone(service):

    command = f'firewall-cmd --permanent --add-service={service} > /tmp/state'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    restarted()
#   add service to specified Zone

def addPermanentServiceToSpecificZone(service, zone):

    command = f'firewall-cmd --permanent --zone={zone} --add-service={service} > /tmp/state'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")


def addPermanetProtocolPort(port, protocol):
    command = f'firewall-cmd --permanent --add-port={port}/{protocol}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    restarted()

# remove service from default zone


def removePermanentServiceFromDefaultZone(service):

    command = f'firewall-cmd --permanent --remmove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")



def RemovePermanetServiceFromSpecificZone(service, zone):

    command = f'firewall-cmd --permanent  --zone={zone} --remove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")



def RemovePermanetProtocolPort(port, protocol):
    command = f'firewall-cmd --permanent --remove-port={port}/{protocol}'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")
        restarted()

################################   DELETE    ##############################################################################

# remove service defaultl zone

def removeServiceFromDefaultZone(service):

    command = f'firewall-cmd --remmove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")



def RemoveServiceFromSpecificZone(service, zone):

    command = f'firewall-cmd   --zone={zone} --remove-service={service} '

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")



def RemoveProtocolPort(port, protocol):
    command = f'firewall-cmd  --remove-port={port}/{protocol}'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")
        restarted()



def RemoveServiceToZone(service, zone):

    command = f'firewall-cmd --zone={zone} --remove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

# remove interface

def RemoveServiceToZone(service, zone):
    command = f'firewall-cmd --zone={zone} --remove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

# remove interface to zone

def RemoveServiceToZone(service, zone):
    command = f'firewall-cmd --zone={zone} --remove-interface={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

# remove specific zone

def RemoveServiceToZone(zone):
    command = f'firewall-cmd --remove- zone={zone}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")


def listAllServices():
    list=[]
    command = f'firewall-cmd --get-services > /tmp/listAllServices'


    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")
    with open('/tmp/listAllServices','r') as file:
        file = file.read()

    default=file
    default=default.replace(' ',':')
    default=default.replace('\n',':')
    default=default.split(':')
    default.pop()
    return default

def firewallGlobalInfo():
    list = []
    output=listZones()
    s=''
    command ='firewall-cmd --list-all-zones > /tmp/listallzones'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")


    with open('/tmp/listallzones', 'r') as file:
        file= file.read()
        s=file.replace(' ','')
        s=file.replace('\n','')

        for i in output:

            s=s.replace(f'{i}',f'++{i}')
        s=s.replace('icmp-++block','icmp-blocks')
        s=s.replace('richrules',' ')
        s=s.replace('forward-ports',' ')
        s=s.replace('source-ports',' ')
        s=s.replace('forward-ports',' ')
        s=s.replace('masquerade',' ')
        s=s.replace('ports',' ')
        s=s.replace('services',' ')
        s=s.replace('interfaces',' ')
        s=s.replace('icmp-blockss',' ')
        s=s.replace('sources',' ')
        s=s.replace('protocols',' ')
        s=s.replace('target',' ')
        s=s.replace('icmp-blocks-inversion','')
        s=s.replace('rich rules','')
        for i in output:
            s = s.replace(f'{i}   ', f'{i}')
        here=s.split('++')
        here.pop(0)

        for i in here:
            i=i.split(':')
            list.append(i)
        return (list)






