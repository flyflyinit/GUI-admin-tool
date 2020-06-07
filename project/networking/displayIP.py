import subprocess


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


def DisplayIP(connectionName):
    listEmpty = []
    listEmpty.append("")
    listEmpty.append("")
    listEmpty.append("")

    if showIpMethod(connectionName) == 'manual':
        cm1 = f'nmcli connection  show {connectionName}| grep -F ipv4.addresses: > /tmp/MANipAddress'
        cm2 = f'nmcli connection  show {connectionName}| grep -F ipv4.gateway: > /tmp/MANgateway'
        cm3 = f'nmcli connection  show {connectionName}| grep -F ipv4.dns:  > /tmp/MANdns'
        try:
            subprocess.run(cm1, check=True, shell=True)
            subprocess.run(cm2, check=True, shell=True)
            subprocess.run(cm3, check=True, shell=True)

        except subprocess.CalledProcessError:
            print("DisplayIP/manual ")

        File = open('/tmp/MANipAddress', 'rt')
        txt = File.read()
        ipAddress = txt.strip()
        ipAddress = ipAddress.replace("   ", ":")
        ipAddress = ipAddress.replace("ipv4.addresses:", "-")
        ipAddress = ipAddress.replace(":", "")
        ipAddress = ipAddress.replace("-", "")
        ipAddress = ipAddress.strip()

        File = open('/tmp/MANgateway', 'rt')
        txt = File.read()
        gateway = txt.strip()
        gateway = gateway.replace("ipv4.gateway:", "-")
        gateway = gateway.replace(":", "")
        gateway = gateway.replace("-", "")
        gateway = gateway.strip()

        File = open('/tmp/MANdns', 'rt')
        txt = File.read()
        dns = txt.rstrip()
        dns = dns.replace("ipv4.dns:", "  ")
        dns = dns.replace(" ", "")
        coninfo = ipAddress + '-' + gateway + '-' + dns
        coninfo = coninfo.split("-")
        return coninfo
    elif showIpMethod(connectionName) == 'auto':
        cm1 = f'nmcli connection  show {connectionName}| grep -F IP4.ADDRESS[1]: > /tmp/AUTOipAddress'
        cm2 = f'nmcli connection  show {connectionName}| grep -F  IP4.GATEWAY: > /tmp/AUTOgateway'
        cm3 = f'nmcli connection  show {connectionName}| grep -F  IP4.DNS[1]:  > /tmp/AUTOdns1'
        cm4 = f'nmcli connection  show {connectionName}| grep -F  IP4.DNS[2]:  > /tmp/AUTOdns2'
        try:
            subprocess.run(cm1, check=True, shell=True)
            subprocess.run(cm2, check=True, shell=True)
            subprocess.run(cm3, check=True, shell=True)
            subprocess.run(cm4, check=True, shell=True)

        except subprocess.CalledProcessError:
            return listEmpty

        File = open('/tmp/AUTOipAddress', 'rt')
        txt2 = File.read()
        ip = txt2.strip()
        ip = ip.replace("IP4.ADDRESS[1]:", "-")
        ip = ip.replace(":", "")
        ip = ip.replace("-", "")
        ip = ip.strip()

        File = open('/tmp/AUTOgateway', 'rt')
        txt3 = File.read()
        gatway = txt3.strip()
        gatway = gatway.replace("IP4.GATEWAY:", "-")
        gatway = gatway.replace(":", "")
        gatway = gatway.replace("-", "")
        gatway = gatway.strip()

        File = open('/tmp/AUTOdns1', 'rt')
        txt1 = File.read()
        dns1 = txt1.strip()
        dns1 = dns1.replace("IP4.DNS[1]:", "-")
        dns1 = dns1.replace(":", "")
        dns1 = dns1.replace("-", "")
        dns1 = dns1.strip()

        File = open('/tmp/AUTOdns2', 'rt')
        txt4 = File.read()
        dns2 = txt4.strip()
        dns2 = dns2.replace("IP4.DNS[2]:", "-")
        dns2 = dns2.replace(":", "")
        dns2 = dns2.replace("-", "")
        dns2 = dns2.strip()

        coninfo2 = ip + '-' + gatway + '-' + dns1 + ',' + dns2
        coninfo2 = coninfo2.split("-")
        listData = coninfo2
        return listData
