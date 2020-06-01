import os, subprocess


def restarted():
    command = 'systemctl restart firewalld > /tmp/zones 2> /tmp/firewallZonesError'
    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error restarted()")


def listZones():
    command = 'firewall-cmd --get-zones > /tmp/firewallZones 2> /tmp/firewallZonesError'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("listZones() ")

    file = open('/tmp/firewallZones', 'rt')
    file = file.read()
    zones = file.replace('\n', ':')
    zones = zones.replace(' ', ':')
    list = zones.split(':')
    list.pop()
    return list


def defaultZone():
    command = 'firewall-cmd --get-default-zone > /tmp/firDefZone 2> /tmp/firewalldefZoneError'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("defaultZone():")

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

        print("activeZone(): ")

    file = open('/tmp/activeZone', 'rt')
    file = file.read()
    default = file.replace('\n', ':')

    return default


def setDefaultZone(zone):
    command = f'firewall-cmd --set-default-zone={zone} '

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")

    restarted()


######################### {ADD} RUN ####################################################################################################

def addInterfaceToZone(interface, zone):
    command = f'firewall-cmd --zone={zone} --add-interface={interface}'

    try:
        subprocess.run(command, check=True, shell=True)


    except subprocess.CalledProcessError:

        print("Error on addInterfaceToZone ")



def addServiceToDefaultZone(service):
    command = f'firewall-cmd  --add-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error on addServiceToDefaultZone ")


def addServiceToSpecificZone(service, zone):
    command = f'firewall-cmd --zone={zone} --add-service={service} > /tmp/state'

    try:
        subprocess.run(command, check=True, shell=True)


    except subprocess.CalledProcessError:

        print("addServiceToSpecificZone(service, zone): ")


def addPort(port, protocol):
    command = f'firewall-cmd  --add-port={port}/{protocol}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error on addPort ")


################################ {EDIT} --permanent   ##############################################################################


def addPermanentNewZone(name):
    name = str(name)
    command = f'firewall-cmd --permanent --new-zone={name}'
    try:
        subprocess.run(command, check=True, shell=True)
        restarted()
    except subprocess.CalledProcessError:
        print("Error on addPermanentNewZone ")


# add interface to zone

def addPermanentInterfaceToZone(interface, zone):
    command = f'firewall-cmd --permanent --zone={zone} --add-interface={interface}'

    try:
        subprocess.run(command, check=True, shell=True)
        restarted()


    except subprocess.CalledProcessError:

        print("Error on addPermanentInterfaceToZone(interface, zone):")



def addPermanentServiceDefaultZone(service):
    command = f'firewall-cmd --permanent --add-service={service} > /tmp/state'

    try:
        subprocess.run(command, check=True, shell=True)
        restarted()
        
    except subprocess.CalledProcessError:

        print("Error on addPermanentServiceDefaultZone ")



#   add service to specified Zone

def addPermanentServiceToSpecificZone(service, zone):
    command = f'firewall-cmd --permanent --zone={zone} --add-service={service} > /tmp/state'

    try:
        subprocess.run(command, check=True, shell=True)
        restarted()


    except subprocess.CalledProcessError:

        print("Error on addPermanentServiceToSpecificZone ")


def addPermanetProtocolPort(port, protocol):
    command = f'firewall-cmd --permanent --add-port={port}/{protocol}'

    try:
        subprocess.run(command, check=True, shell=True)
        restarted()



    except subprocess.CalledProcessError:

        print("Error on addPermanetProtocolPort(port, protocol): ")


# remove interface from a zone

def RemovePermanetInterfaceFromZone(service, zone):
    command = f'firewall-cmd --permanent --zone={zone} --remove-interface={service}'

    try:
        subprocess.run(command, check=True, shell=True)
        restarted()

    except subprocess.CalledProcessError:

        print("Error on RemoveInterfaceFromZone ")

# remove service from default zone


def removePermanentServiceFromDefaultZone(service):
    command = f'firewall-cmd --permanent --remove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)
        restarted()

    except subprocess.CalledProcessError:
        print("Error  on removePermanentServiceFromDefaultZone")


def RemovePermanetServiceFromSpecificZone(service, zone):
    command = f'firewall-cmd --permanent  --zone={zone} --remove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)
        restarted()

    except subprocess.CalledProcessError:

        print("Error on RemovePermanetServiceFromSpecificZone ")


def RemovePermanetProtocolPort(port, protocol):
    command = f'firewall-cmd --permanent --remove-port={port}/{protocol}'
    try:
        subprocess.run(command, check=True, shell=True)
        restarted()

    except subprocess.CalledProcessError:
        print("Error on RemovePermanetProtocolPort  ")


################################   DELETE    ##############################################################################

# remove interface to zone

def RemoveInterfaceFromZone(int, zone):
    command = f'firewall-cmd --zone={zone} --remove-interface={int}'

    try:
        subprocess.run(command, check=True, shell=True)


    except subprocess.CalledProcessError:

        print("Error on  RemoveInterfaceFromZone ")



# remove specific zone

def RemoveZone(zone):
    command = f'firewall-cmd --remove- zone={zone}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error on RemoveZone ")

def removeServiceFromDefaultZone(service):

    command = f'firewall-cmd --remove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)


    except subprocess.CalledProcessError:

        print("Error on removeServiceFromDefaultZone ")



def RemoveServiceToZone(service, zone):
    command = f'firewall-cmd --zone={zone} --remove-service={service}'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error on RemoveServiceToZone ")



def RemoveProtocolPort(port, protocol):
    command = f'firewall-cmd  --remove-port={port}/{protocol}'
    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error on RemoveProtocolPort ")






##############################################################################################################################
def listAllServices():
    list = []
    command = f'firewall-cmd --get-services > /tmp/listAllServices'

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:

        print("Error While fetching Data ")
    with open('/tmp/listAllServices', 'r') as file:
        file = file.read()

    default = file
    default = default.replace(' ', ':')
    default = default.replace('\n', ':')
    default = default.split(':')
    default.pop()
    return default


def firewallGlobalInfo():
    list = []
    output = listZones()
    s = ''
    command = 'firewall-cmd --list-all-zones > /tmp/listallzones'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("Error While fetching Data ")

    with open('/tmp/listallzones', 'r') as file:
        file = file.read()
        s = file.replace(' ', '')
        s = file.replace('\n', '')

        for i in output:
            s = s.replace(f'{i}', f'++{i}')
        s = s.replace('icmp-++block', 'icmp-blocks')
        s = s.replace('richrules', ' ')
        s = s.replace('forward-ports', ' ')
        s = s.replace('source-ports', ' ')
        s = s.replace('forward-ports', ' ')
        s = s.replace('masquerade', ' ')
        s = s.replace('ports', ' ')
        s = s.replace('services', ' ')
        s = s.replace('interfaces', ' ')
        s = s.replace('icmp-blockss', ' ')
        s = s.replace('sources', ' ')
        s = s.replace('protocols', ' ')
        s = s.replace('target', ' ')
        s = s.replace('icmp-blocks-inversion', '')
        s = s.replace('rich rules', '')
        for i in output:
            s = s.replace(f'{i}   ', f'{i}')
        here = s.split('++')
        here.pop(0)

        for i in here:
            i = i.split(':')
            list.append(i)
        return (list)






