import subprocess

def displayConnection():
    lisData=[]
    lisData2=[]
    command = 'nmcli connection show > /tmp/listConnection  '

    try:
        subprocess.run(command, check=True, shell=True)

    except subprocess.CalledProcessError:
        print("Error While fetching Connnections ")

    with open('/tmp/listConnection') as f:
        lineList = f.readlines()
    lineList.pop(0)
    for i in lineList:
        i=i[::-1]
        i=i[56:]
        i=i[::-1]
        lisData.append(i)
    for i in lisData:
        i=i.replace('\n','')
        #i=i.replace(' ','\\\\')
        i=i.replace(' ','\\ ')
        i=i.replace('\\',',')
        i=i.replace(', ,','')
        i=i.replace('\n','')
        i=i.replace(',','\\')
        i=i.replace(' \\','')
        lisData2.append(i)

    return lisData2

