import os,subprocess
from project.networking.displayConnections import displayConnection
from project.networking.networkingScripts import showIpMethod
from project.networking.networkingScripts import currentlyActiveConnectionNow


def globalInfo():

    output=displayConnection()
    output.pop()
    turn=0
    for j in output:
        cm1 ='nmcli connection  show {} | grep -F connection.id:  >  /tmp/info-{}-'.format(j,output.index(j))
        cm2='nmcli connection  show {} | grep -F connection.type:  >> /tmp/info-{}-'.format(j,output.index(j))
        cm3 = 'nmcli connection  show {} | grep -F GENERAL.DEVICES: >> /tmp/info-{}-'.format(j, output.index(j))
        cm4 = 'nmcli connection  show {} | grep -F  connection.autoconnect: >> /tmp/info-{}-'.format(j, output.index(j))
        cm6=''
        if showIpMethod(j)=='auto':
            cm6='nmcli connection  show {}| grep -F IP4.ADDRESS[1]: >> /tmp/info-{}-'.format(j,output.index(j))
        else:
            cm6='nmcli connection  show {}| grep -F ipv4.addresses: >> /tmp/info-{}-'.format(j,output.index(j))

        try:
            os.system(cm1)
            os.system(cm2)
            os.system(cm3)
            os.system(cm4)
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

def globalInfoZero(con):
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
        os.system(cm5)
        os.system(cm7)
        #os.system(cm6)


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
    f= f.replace('connection.id', 'connection.id,')
    f= f.replace('connection.autoconnect', ',')
    f= f.replace('connection.autoconnect-priority', ',')
    f = f.replace('\n', '')
    ff = f.split('connection.id,')
    ff.pop(0)
    set = (ff)
    return set

def globalInfoTwo():
    con=displayConnection()
    listinfo=[]
    index=[]
    counter=0
    for i in range(len(con)):
        output=globalInfoZero(con[i])
        output=output[0]
        output=output.split(',')
        listinfo.append(output)
    return listinfo
