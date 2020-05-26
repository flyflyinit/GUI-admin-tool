
import subprocess

from project.networking.networkingScripts import showIpMethod, currentlyActiveConnectionNow, globalInof


def displayIP(connectionName):
    list = []

    if showIpMethod(connectionName) == 'manual':

        fullCommand = f'nmcli connection  show {connectionName} | grep -F ipv4.addresses: > /tmp/INipAddress'
        fullCommand = f'nmcli connection  show {connectionName} | grep -F ipv4.gateway: > /tmp/INgateway'
        fullCommand = f'nmcli connection  show {connectionName} | grep -F ipv4.dns:  >/tmp/INdns1'


        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        # fullCommand = f'cat /etc/sysconfig/network-scripts/ifcfg-{connectionName}| grep -F DNS2 > /tmp/dns2'
        # os.system(fullCommand)


        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")


        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        File = open('/tmp/INdns1', 'rt')
        txt = File.read()
        dns1 = txt.strip()
        dns = dns1.replace("ipv4.dns:", "-")
        dns = dns.replace(":", "")
        dns = dns.replace("-", "")
        dns = dns.strip()

        File = open('/tmp/INipAddress', 'rt')
        txt = File.read()
        ipAddress = txt.strip()
        ipAddress = ipAddress.replace("   ", ":")
        ipAddress = ipAddress.replace("ipv4.addresses:", "-")
        ipAddress = ipAddress.replace(":", "")
        ipAddress = ipAddress.replace("-", "")
        ipAddress = ipAddress.strip()

        File = open('/tmp/INgateway', 'rt')
        txt = File.read()
        gateway = txt.strip()
        gateway = gateway.replace("ipv4.gateway:", "-")
        gateway = gateway.replace(":", "")
        gateway = gateway.replace("-", "")
        gateway = gateway.strip()

        File = open('/tmp/INdns2', 'rt')
        txt = File.read()
        mask = txt.rstrip()
        dns2 = mask.replace("PREFIX=", "  ")

        coninfo = ipAddress + '-' + gateway + '-' + dns
        coninfo = coninfo.split("-")
        list.append(ipAddress)
        list.append(gateway)
        list.append(dns)
        list.append(dns2)



    else:

        fullCommand = f'nmcli connection  show {connectionName} | grep -F IP4.ADDRESS[1]: > /tmp/INipAddress2'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        # fullCommand = f'cat /etc/sysconfig/network-scripts/ifcfg-{connectionName}| grep -F DNS2 > /tmp/dns2'
        # os.system(fullCommand)

        fullCommand = f'nmcli connection  show {connectionName} | grep -F  IP4.GATEWAY: > /tmp/INgateway2'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        fullCommand = f'nmcli connection  show {connectionName} | grep -F  IP4.DNS[1]:  > /tmp/INdns12'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        fullCommand = f'nmcli connection  show {connectionName} | grep -F  IP4.DNS[2]:  > /tmp/INdns22'

        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        File = open('/tmp/INipAddress2', 'rt')
        txt2 = File.read()
        ip = txt2.strip()
        ip = ip.replace("IP4.ADDRESS[1]:", "-")
        ip = ip.replace(":", "")
        ip = ip.replace("-", "")
        ip = ip.strip()

        File = open('/tmp/INdns12', 'rt')
        txt1 = File.read()
        dns1 = txt1.strip()
        dns1 = dns1.replace("IP4.DNS[1]:", "-")
        dns1 = dns1.replace(":", "")
        dns1 = dns1.replace("-", "")
        dns1 = dns1.strip()

        File = open('/tmp/INgateway2', 'rt')
        txt3 = File.read()
        gatway = txt3.strip()
        gatway = gatway.replace("IP4.GATEWAY:", "-")
        gatway = gatway.replace(":", "")
        gatway = gatway.replace("-", "")
        gatway = gatway.strip()

        File = open('/tmp/INdns22', 'rt')
        txt4 = File.read()
        dns2 = txt4.strip()
        dns2 = dns2.replace("IP4.DNS[2]:", "-")
        dns2 = dns2.replace(":", "")
        dns2 = dns2.replace("-", "")
        dns2 = dns2.strip()
        try:
            fullCommand='rm -rf /tmp/IN*'
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

        coninfo2 = ip + '-' + gatway + '-' + dns1 + ',' + dns2
        list.append(ip)
        list.append(gatway)
        list.append(dns1)
        list.append(dns2)
        return list
'''
def fullINFO():

    output=currentlyActiveConnectionNow()
    r1=displayIP(output[0])
    r2=globalInof(output[0])
    r3=r2+r1
    return r3
'''

def AutoConnection(connectionName, par):

        fullCommand = f'nmcli connection modify {connectionName} autoconnect {par} '
        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

def takeIpFromDHCP(connectionName,par):

    if par==True:

        fullCommand = f'nmcli connection modify {connectionName} ipv4.method auto '
        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

    elif par==False:

        fullCommand = f'nmcli connection modify {connectionName} ipv4.method manual '
        try:
            subprocess.run(fullCommand, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("Error While fetching Data ")

