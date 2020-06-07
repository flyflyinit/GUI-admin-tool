import subprocess


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


def listports(zone):
    command = f'firewall-cmd --zone={zone} --list-ports > /tmp/listports'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("listZones() ")

    file = open('/tmp/listports', 'rt')
    file = file.read()
    ports = file.replace('\n', ':')
    ports = ports.replace(' ', ':')
    list = ports.split(':')
    list.pop()

    return list


def listservices(zone):
    command = f'firewall-cmd --zone={zone} --list-services > /tmp/listservices'
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("listZones() ")

    file = open('/tmp/listservices', 'rt')
    file = file.read()
    pro = file.replace('\n', ':')
    pro = pro.replace(' ', ':')
    list = pro.split(':')
    list.pop()

    return list


def listinterfaces(zone):
    command = f'firewall-cmd --zone={zone} --list-interface > /tmp/listinter'

    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("listinterfaces() ")

    file = open('/tmp/listinter', 'rt')
    file = file.read()
    pro = file.replace('\n', ':')
    pro = pro.replace(' ', ':')
    list = pro.split(':')
    list.pop()

    return list


def listZoneModified():
    output = listZones()
    listB = []

    for i in output:
        listA = []
        listA.append(i)
        listB.append(listA)
    return listB
