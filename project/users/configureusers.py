try:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QPushButton, QSpinBox, QLabel, QLineEdit, QFormLayout, \
        QHBoxLayout, QListWidget, QMessageBox, QCheckBox
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import subprocess
    import concurrent.futures
    from datetime import datetime
except ImportError as e:
    print(f'package not found\n{e}\n')


class CreateUsersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("Configure System")
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.progeesBar = QProgressBar()
        self.progeesBar.setHidden(True)
        self.okBtn=QPushButton("Ok")
        self.okBtn.clicked.connect(self.cancelAction)
        self.okBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60" )
        self.okBtn.setHidden(True)
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn=QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.submitBtn.setHidden(False)
        self.cancelBtn.setHidden(False)
        self.okBtn.setFixedHeight(30)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60" )
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.okBtn)
        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.progeesBar)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def widgets(self):
        self.usersNbr = QSpinBox(self)
        self.usersNbr.setMinimum(1)
        self.usersNbr.setMaximum(1000)
        self.usersNbr.setSuffix(" user")
        self.createHomeDir=QCheckBox('Create Home Directory')

        self.form=QFormLayout()
        self.editLineUsername=QLineEdit('')
        self.editLineUsername.setPlaceholderText('enter username')
        self.form.addRow(QLabel('Username :'),self.editLineUsername)
        self.editLineUserShell=QLineEdit('')
        self.editLineUserShell.setPlaceholderText('enter shell')
        self.form.addRow(QLabel('User Shell :'),self.editLineUserShell)
        self.editLineUserComment=QLineEdit('')
        self.editLineUserComment.setPlaceholderText('enter comment')
        self.form.addRow(QLabel('Comment :'),self.editLineUserComment)
        self.note=QLabel('')

        self.topLayout.addWidget(self.usersNbr)
        self.topLayout.addWidget(self.editLineUsername)
        self.topLayout.addWidget(self.editLineUserShell)
        self.topLayout.addWidget(self.editLineUserComment)
        self.topLayout.addWidget(self.createHomeDir)
        self.topLayout.addWidget(self.note)

    def submitAction(self):
        self.progeesBar.setHidden(False)
        self.progeesBar.setMaximum(self.usersNbr.value())
        self.progeesBar.setValue(0)
        usersList = self.generateList()
        txt = ''
        nbr = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.createuserThreading, usersList)
            for result in results:
                nbr+=1
                self.progeesBar.setValue(nbr)
                txt = txt + result + "\n"
                self.note.setText(txt)
        self.okBtn.setHidden(False)
        self.submitBtn.setHidden(True)
        self.cancelBtn.setHidden(True)

    def generateList(self):
        usersList = []
        homeDir = 'False'
        if self.createHomeDir.isChecked():
            homeDir = 'True'

        if int(self.usersNbr.value()) == 1:
            usersList.append([self.editLineUsername.text(),self.editLineUserComment.text(),self.editLineUserShell.text(),homeDir])
        else:
            for user in range(self.usersNbr.value()):
                usersList.append([self.editLineUsername.text()+str(user+1),self.editLineUserComment.text()+str(user+1),self.editLineUserShell.text(),homeDir])
        return usersList

    def createuserThreading(self,user):
        if user[3]=='True':
            homedir = '-m'
        else:
            homedir = ''
        try:
            c = f'useradd {homedir} -s {user[2]} -c "{user[1]}" {user[0]}'
            subprocess.run(c,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL ,shell=True,check=True)
        except subprocess.CalledProcessError:
            return f"error occured during creating {user[0]} "
        else:
            return f"{user[0]} has been created succesfully!"

    def cancelAction(self):
        self.close()


class EditUsersWindow(QWidget):
    def __init__(self,userDetails):
        super().__init__()
        self.setGeometry(200,50,500,500)
        self.setWindowTitle("Edit User")
        self.userDetails = userDetails
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.text = QLabel('')
        self.progeesBar = QProgressBar()
        self.progeesBar.setHidden(True)
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn=QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.okBtn=QPushButton("Ok")
        self.okBtn.clicked.connect(self.okAction)
        self.okBtn.setHidden(True)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.okBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )
        self.okBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.bottomLayout.addWidget(self.okBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def widgets(self):
        self.form = QFormLayout()

        print(self.userDetails)
        self.username=QLineEdit(self.userDetails[0])
        self.form.addRow(QLabel('Username :'),self.username)
        self.id=QLineEdit(self.userDetails[1])
        self.form.addRow(QLabel('User ID :'),self.id)

        self.primaryGroup=self.userDetails[2].split('(')[1].split(')')[0]
        self.priGroup=QLineEdit(self.primaryGroup)
        self.form.addRow(QLabel('Primary Group :'),self.priGroup)

        self.comment=QLineEdit(self.userDetails[4])
        self.form.addRow(QLabel('Comment :'),self.comment)
        self.homeDir=QLineEdit(self.userDetails[5])
        self.form.addRow(QLabel('Home Directory :'),self.homeDir)
        self.shell=QLineEdit(self.userDetails[6])
        self.form.addRow(QLabel('Shell :'),self.shell)

        if self.userDetails[7]=='never':
            self.expirationDate=QLineEdit()
        else:
            import dateutil.parser as parser
            self.expirationDate_adapted = datetime.strptime(self.userDetails[7], '%b %d, %Y').strftime('%Y-%m-%d')
            date = parser.parse(self.expirationDate_adapted)
            self.expirationDate=QLineEdit(date.isoformat().split('T')[0])
        self.form.addRow(QLabel('Expiration Date :'),self.expirationDate)

        self.groupsBtns=QVBoxLayout()
        self.lineEditAddGroup=QLineEdit()
        self.lineEditAddGroup.setPlaceholderText('enter group name')
        self.addGroupBtn=QPushButton('Add')
        self.addGroupBtn.clicked.connect(self.addGroup)
        self.deleteGroupBtn=QPushButton('Delete')
        self.deleteGroupBtn.clicked.connect(self.deleteGroup)
        self.deleteAllGroupsBtn=QPushButton('Delete All')
        self.deleteAllGroupsBtn.clicked.connect(self.deleteAllGroups)
        self.groupsBtns.addWidget(self.lineEditAddGroup)
        self.groupsBtns.addWidget(self.addGroupBtn)
        self.groupsBtns.addWidget(self.deleteGroupBtn)
        self.groupsBtns.addWidget(self.deleteAllGroupsBtn)
        self.groupsBtns.addStretch()
        self.listGroups=QListWidget()

        self.form.addRow(QLabel('Groups :'),self.middleLayout)

        groups = self.userDetails[3].split(',')
        for group in groups:
            grp = group.split('(')[1].split(')')[0]
            if grp == self.primaryGroup:
                continue
            else:
                self.listGroups.addItem(grp)

        self.middleLayout.addWidget(self.listGroups)
        self.middleLayout.addLayout(self.groupsBtns)
        self.topLayout.addLayout(self.form)
        self.topLayout.addWidget(self.text)
        self.topLayout.addWidget(self.progeesBar)

    def addGroup(self):
        group = self.lineEditAddGroup.text()
        if group == "":
            pass
        else:
            self.listGroups.addItem(group)

    def deleteGroup(self):
        listGroups = self.listGroups.selectedItems()
        if not listGroups: return
        for group in listGroups:
            self.listGroups.takeItem(self.listGroups.row(group))

    def deleteAllGroups(self):
        self.listGroups.clear()

    def submitAction(self):
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setMaximum(1)
            self.progeesBar.setValue(0)
            self.edituser()
        except subprocess.CalledProcessError :
            QMessageBox.warning(self,'warning',f"error occured during editing this user\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def okAction(self):
        self.close()

    def edituser(self):
        usernamee=self.username.text()
        idd=self.id.text()
        priGroupp=self.priGroup.text()
        commentt=self.comment.text()
        homeDirr=self.homeDir.text()
        shelll=self.shell.text()
        expirationDatee=self.expirationDate.text()
        txt = ''

        groupsitems = []
        for index in range(self.listGroups.count()):
            groupsitems.append(str(self.listGroups.item(index).text()))
        groupsitemsstring = ",".join(groupsitems)
        print(groupsitemsstring)
        if expirationDatee == "never":
            QMessageBox.warning(self,'expiration field error',"expiration field can't be 'never' ")
            return 0
        elif expirationDatee == '':
            pass
        else:
            try:
                subprocess.run(f'usermod -e {expirationDatee} {self.userDetails[0]}',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, check=True,shell=True)
            except subprocess.CalledProcessError:
                txt = txt + "error occured during editing expiration date for this user\n"
                self.text.setText(txt)
            else:
                txt = txt + "expiration date edited succesfully\n"
                self.text.setText(txt)
        try:
            subprocess.run(f'usermod -g {priGroupp} {self.userDetails[0]}',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, check=True,shell=True)
        except subprocess.CalledProcessError:
            txt = txt + "error occured during editing primary group for this user\n"
            self.text.setText(txt)
        else:
            txt = txt + "primary group edited succesfully\n"
            self.text.setText(txt)

        try:
            subprocess.run(f'usermod -G {groupsitemsstring} {self.userDetails[0]}', stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, check=True, shell=True)
        except subprocess.CalledProcessError:
            txt = txt + "error occured during editing supplementary groups for this user\n"
            self.text.setText(txt)
        else:
            txt = txt + "supplementary groups edited succesfully\n"
            self.text.setText(txt)

        try:
            subprocess.run(f'usermod -s {shelll} {self.userDetails[0]}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        except subprocess.CalledProcessError:
            txt = txt + "error occured during editing shell for this user\n"
            self.text.setText(txt)
        else:
            txt = txt + "shell edited succesfully\n"
            self.text.setText(txt)

        try:
            subprocess.run(f'usermod -d {homeDirr} {self.userDetails[0]}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        except subprocess.CalledProcessError:
            txt = txt + "error occured during editing home directory for this user\n"
            self.text.setText(txt)
        else:
            txt = txt + "home directory edited succesfully\n"
            self.text.setText(txt)

        try:
            subprocess.run(f"usermod -c '{commentt}' {self.userDetails[0]}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        except subprocess.CalledProcessError:
            txt = txt + "error occured during editing comment for this user\n"
            self.text.setText(txt)
        else:
            txt = txt + "comment edited succesfully\n"
            self.text.setText(txt)

        try:
            subprocess.run(f"usermod -u {idd} {self.userDetails[0]}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        except subprocess.CalledProcessError:
            txt = txt + "error occured during editing user id for this user\n"
            self.text.setText(txt)
        else:
            txt = txt + "user id edited succesfully\n"
            self.text.setText(txt)

        try:
            subprocess.run(f'usermod -l {usernamee} {self.userDetails[0]}', stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, check=True, shell=True)
        except subprocess.CalledProcessError:
            txt = txt + "error occured during editing username for this user\n"
            self.text.setText(txt)
        else:
            txt = txt + "username edited succesfully\n"
            self.text.setText(txt)

        self.progeesBar.setValue(1)

    def cancelAction(self):
        self.close()


class DeleteUsersWindow(QWidget):
    def __init__(self,d):
        super().__init__()
        self.setGeometry(200,50,300,300)
        self.setWindowTitle("Delete Users")
        self.listUsersToDelete = d
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.progeesBar = QProgressBar()
        self.progeesBar.setHidden(True)
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn=QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.okBtn=QPushButton("Ok")
        self.okBtn.clicked.connect(self.okAction)
        self.okBtn.setHidden(True)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.okBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )
        self.okBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.bottomLayout.addWidget(self.okBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def widgets(self):
        self.a = ', '.join(self.listUsersToDelete)
        self.text = QLabel(f'Are You Sure You want To Delete The Following Users :\n\n{self.a}')
        self.text2 = QLabel()
        self.topLayout.addWidget(self.text)
        self.topLayout.addWidget(self.text2)
        self.topLayout.addWidget(self.progeesBar)

    def submitAction(self):
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setMaximum(len(self.listUsersToDelete))
            self.progeesBar.setValue(0)
            self.deleteuser()
        except subprocess.CalledProcessError :
            QMessageBox.warning(self,'warning',f"error occured during setting this hostname\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def okAction(self):
        self.close()

    def deleteuserThreading(self,username):
        try:
            subprocess.run(f'userdel -r {username}',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, check=True,shell=True)
        except subprocess.CalledProcessError:
            return f"error occured during deleting {username}"
        else:
            return f"{username} deleted succesfully!"

    def deleteuser(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.deleteuserThreading, self.listUsersToDelete)
            i = 0
            r = ''
            for result in results:
                i = i + 1
                r = r +"\n"+result
                self.progeesBar.setValue(i)
                self.text2.setText(r)

    def cancelAction(self):
        self.close()


class MoreUsersWindow(QWidget):
    def __init__(self,text,username):
        super().__init__()
        self.setGeometry(200,50,300,300)
        self.setWindowTitle(username)
        self.text = text
        self.layouts()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.label = QLabel(self.text)
        self.okBtn=QPushButton("Ok")
        self.okBtn.clicked.connect(self.okAction)
        self.okBtn.setFixedHeight(30)
        self.okBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )

        self.topLayout.addWidget(self.label)
        self.bottomLayout.addWidget(self.okBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def okAction(self):
        self.close()
