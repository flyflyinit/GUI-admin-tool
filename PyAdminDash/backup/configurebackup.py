try:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, \
        QFormLayout, \
        QLineEdit, QCheckBox, QListWidget, QMessageBox, QScrollArea, QGroupBox, QComboBox
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import sqlite3
    import concurrent.futures
    import subprocess
    import concurrent.futures
    from datetime import datetime
except ImportError as e:
    print(f'package not found\n{e}\n')


class CreateFullBackupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,500,500)
        self.setWindowTitle("Create Full Backup")
        self.layouts()
        self.widgets()
        global con
        global cur
        con = sqlite3.connect('backup/backupshistory.db')
        cur = con.cursor()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.middleLayout = QHBoxLayout()

        self.frame = QFrame()
        self.middleLayoutcontainer = QVBoxLayout()
        self.frame.setLayout(self.middleLayoutcontainer)
        self.frame.hide()

        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.text = QLabel('')
        self.progeesBar = QProgressBar()
        self.progeesBar.setMaximum(1)
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
        self.form=QFormLayout()
        self.editLineFullBackupName=QLineEdit('')
        self.editLineFullBackupName.setPlaceholderText('enter full backup name')
        self.form.addRow(QLabel('Backup Name :'),self.editLineFullBackupName)
        self.editLineFullBackupSrc=QLineEdit('')
        self.editLineFullBackupSrc.setPlaceholderText('what you are going to backup')
        self.form.addRow(QLabel('Backup Path :'),self.editLineFullBackupSrc)
        self.editLineFullBackupDst=QLineEdit('')
        self.editLineFullBackupDst.setPlaceholderText('where you are going to store the backup')
        self.form.addRow(QLabel('Backup Destination :'),self.editLineFullBackupDst)
        self.exclude=QCheckBox('Exclude Items')
        self.exclude.stateChanged.connect(self.showExclude)

        self.form.addRow(self.exclude)
        self.note=QLabel('\nNote: make sure to provide absolute paths\nexample, /home/user/folder , /root/dir/subdir')
        self.noteexcluded=QLabel('\nexcluded items examples, /home/user/folder/excludedfile \n/root/dir/subdir/excludeddir')
        self.status=QLabel('')

        self.excludedBtns=QVBoxLayout()
        self.lineEditAddExclude=QLineEdit()
        self.lineEditAddExclude.setPlaceholderText('enter path')
        self.addExcludeBtn=QPushButton('Add')
        self.addExcludeBtn.clicked.connect(self.addExclude)
        self.deleteExcludeBtn=QPushButton('Delete')
        self.deleteExcludeBtn.clicked.connect(self.deleteExclude)
        self.deleteAllExcludeBtn=QPushButton('Delete All')
        self.deleteAllExcludeBtn.clicked.connect(self.deleteAllExclude)
        self.excludedBtns.addWidget(self.addExcludeBtn)
        self.excludedBtns.addWidget(self.deleteExcludeBtn)
        self.excludedBtns.addWidget(self.deleteAllExcludeBtn)
        self.excludedBtns.addStretch()
        self.listExclude=QListWidget()

        self.middleLayoutcontainer.addWidget(self.lineEditAddExclude)
        self.middleLayoutcontainer.addLayout(self.middleLayout)
        self.middleLayoutcontainer.addWidget(self.noteexcluded)
        self.form.addRow(self.frame)

        self.middleLayout.addWidget(self.listExclude)
        self.middleLayout.addLayout(self.excludedBtns)
        self.topLayout.addLayout(self.form)
        self.topLayout.addWidget(self.note)
        self.topLayout.addWidget(self.status)
        self.topLayout.addWidget(self.progeesBar)

    def addExclude(self):
        exclude = self.lineEditAddExclude.text()
        if exclude == "":
            pass
        else:
            self.listExclude.addItem(exclude)

    def showExclude(self):
        if self.exclude.isChecked():
            self.frame.show()
        else:
            self.frame.hide()

    def deleteExclude(self):
        listExclude = self.listExclude.selectedItems()
        if not listExclude: return
        for exclude in listExclude:
            self.listExclude.takeItem(self.listExclude.row(exclude))

    def deleteAllExclude(self):
        self.listExclude.clear()

    def submitAction(self):
        try:
            global cur
            global con
            self.progeesBar.setHidden(False)
            self.progeesBar.setValue(0)
            fullbackupList = self.generateList()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(self.createfullbackupThreading, fullbackupList)
                for result in results:
                    self.progeesBar.setValue(1)
                    self.status.setText(result)
            fullbackup = fullbackupList[0]
            query = "INSERT INTO FullBackups (date,name,srcpath,dstpath,excluded) VALUES (?,?,?,?,?)"
            cur.execute(query, (fullbackup[0], fullbackup[1], fullbackup[2], fullbackup[3], fullbackup[4]))
            con.commit()
            self.okBtn.setHidden(False)
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
        except Exception :
            QMessageBox.warning(self,'warning',f"error occured during creating this backup\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)


    def okAction(self):
        self.close()

    def generateList(self):
        fullbackupList = []
        excluded = ''
        if self.exclude.isChecked():
            for index in range(self.listExclude.count()):
                excluded = excluded + " --exclude=" + str(self.listExclude.item(index).text())
        now = datetime.today()
        now = str(now).replace(' ', '-').split('.')[0]
        fullbackupList.append([now,self.editLineFullBackupName.text()+now,self.editLineFullBackupSrc.text(),self.editLineFullBackupDst.text(),excluded])
        return fullbackupList

    def createfullbackupThreading(self,fullbackup):
        try:
            c = "tar -cvvpzf " + fullbackup[3] + "/" + fullbackup[1] + ".tar.gz " + fullbackup[4] + " " + fullbackup[2]
            subprocess.run(c,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL ,shell=True,check=True)
        except Exception as e:
            return f"error occured during creating this full backup {fullbackup[1]}"
        else:
            return f"{fullbackup[1]} has been created succesfully! {fullbackup[3]}/{fullbackup[1]}.tar.gz"

    def cancelAction(self):
        self.close()


class CreateIncBackupWindow(QWidget):
    def __init__(self,incBackupList):
        super().__init__()
        self.setGeometry(200,50,500,500)
        self.setWindowTitle("Create Incremental Backup")
        self.incBackupList=incBackupList
        global con
        global cur
        con = sqlite3.connect('backup/backupshistory.db')
        cur = con.cursor()
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.middleLayout = QHBoxLayout()

        self.frame = QFrame()
        self.middleLayoutcontainer = QVBoxLayout()
        self.frame.setLayout(self.middleLayoutcontainer)
        self.frame.hide()

        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.text = QLabel('')
        self.progeesBar = QProgressBar()
        self.progeesBar.setMaximum(1)
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
        self.form=QFormLayout()

        self.existingInc=QCheckBox('Existing Incremental Backup')
        self.existingInc.stateChanged.connect(self.showexistinginc)
        self.form.addRow(self.existingInc)

        self.cretecombo()

        self.editLineIncBackupMetaNametxt=QLabel('Backup Meta Name :')
        self.editLineIncBackupMetaName=QLineEdit('')
        self.editLineIncBackupMetaName.setPlaceholderText('enter Inc backup meta name')
        self.form.addRow(self.editLineIncBackupMetaNametxt,self.editLineIncBackupMetaName)
        self.editLineIncBackupName=QLineEdit('')
        self.editLineIncBackupName.setPlaceholderText('enter Inc backup name')
        self.form.addRow(QLabel('Backup Name :'),self.editLineIncBackupName)
        self.editLineIncBackupSrctxt=QLabel('Backup Path :')
        self.editLineIncBackupSrc=QLineEdit('')
        self.editLineIncBackupSrc.setPlaceholderText('what you are going to backup')
        self.form.addRow(self.editLineIncBackupSrctxt,self.editLineIncBackupSrc)
        self.editLineIncBackupDsttxt=QLabel('Backup Destination :')
        self.editLineIncBackupDst=QLineEdit('')
        self.editLineIncBackupDst.setPlaceholderText('where you are going to store the backup')
        self.form.addRow(self.editLineIncBackupDsttxt,self.editLineIncBackupDst)
        self.exclude=QCheckBox('Exclude Items')
        self.exclude.stateChanged.connect(self.showExclude)

        self.form.addRow(self.exclude)
        self.note=QLabel('\nNote: make sure to provide absolute paths\nexample, /home/user/folder , /root/dir/subdir')
        self.noteexcluded=QLabel('\nexcluded items examples, /home/user/folder/excludedfile \n/root/dir/subdir/excludeddir')
        self.status=QLabel('')

        self.excludedBtns=QVBoxLayout()
        self.lineEditAddExclude=QLineEdit()
        self.lineEditAddExclude.setPlaceholderText('enter path')
        self.addExcludeBtn=QPushButton('Add')
        self.addExcludeBtn.clicked.connect(self.addExclude)
        self.deleteExcludeBtn=QPushButton('Delete')
        self.deleteExcludeBtn.clicked.connect(self.deleteExclude)
        self.deleteAllExcludeBtn=QPushButton('Delete All')
        self.deleteAllExcludeBtn.clicked.connect(self.deleteAllExclude)
        self.excludedBtns.addWidget(self.addExcludeBtn)
        self.excludedBtns.addWidget(self.deleteExcludeBtn)
        self.excludedBtns.addWidget(self.deleteAllExcludeBtn)
        self.excludedBtns.addStretch()
        self.listExclude=QListWidget()

        self.middleLayoutcontainer.addWidget(self.lineEditAddExclude)
        self.middleLayoutcontainer.addLayout(self.middleLayout)
        self.middleLayoutcontainer.addWidget(self.noteexcluded)
        self.form.addRow(self.frame)

        self.middleLayout.addWidget(self.listExclude)
        self.middleLayout.addLayout(self.excludedBtns)
        self.topLayout.addLayout(self.form)
        self.topLayout.addWidget(self.note)
        self.topLayout.addWidget(self.status)
        self.topLayout.addWidget(self.progeesBar)

    def cretecombo(self):
        self.combo=QComboBox()
        self.txt = QLabel('Existing Incremental Backups :')
        self.txt.setHidden(True)
        self.combo.setHidden(True)
        for item in self.incBackupList:
            self.combo.addItem(item)
        self.form.addRow(self.txt,self.combo)

    def addExclude(self):
        exclude = self.lineEditAddExclude.text()
        if exclude == "":
            pass
        else:
            self.listExclude.addItem(exclude)

    def showExclude(self):
        if self.exclude.isChecked():
            self.frame.show()
        else:
            self.frame.hide()

    def showexistinginc(self):
        if self.existingInc.isChecked():
            self.combo.setHidden(False)
            self.txt.setHidden(False)
            self.editLineIncBackupMetaNametxt.setHidden(True)
            self.editLineIncBackupMetaName.setHidden(True)
            self.editLineIncBackupSrc.setHidden(True)
            self.editLineIncBackupSrctxt.setHidden(True)
            self.editLineIncBackupDsttxt.setHidden(True)
            self.editLineIncBackupDst.setHidden(True)
            self.exclude.setHidden(True)
            self.frame.hide()
        else:
            self.combo.setHidden(True)
            self.txt.setHidden(True)
            self.editLineIncBackupMetaNametxt.setHidden(False)
            self.editLineIncBackupMetaName.setHidden(False)
            self.editLineIncBackupSrc.setHidden(False)
            self.editLineIncBackupSrctxt.setHidden(False)
            self.editLineIncBackupDsttxt.setHidden(False)
            self.editLineIncBackupDst.setHidden(False)
            self.exclude.setHidden(False)
            self.showExclude()

    def deleteExclude(self):
        listExclude = self.listExclude.selectedItems()
        if not listExclude: return
        for exclude in listExclude:
            self.listExclude.takeItem(self.listExclude.row(exclude))

    def deleteAllExclude(self):
        self.listExclude.clear()

    def submitAction(self):
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setValue(0)
            self.submit()
        except Exception :
            QMessageBox.warning(self,'warning',f"error occured during creating this backup\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def okAction(self):
        self.close()

    def submit(self):
        incbackupList = []
        if self.existingInc.isChecked():
            now = datetime.today()
            now = str(now).replace(' ','-').split('.')[0]
            metaname = self.combo.currentText()
            backupname = self.editLineIncBackupName.text()+now
            incbackupList.append(str(now))
            incbackupList.append(metaname)
            incbackupList.append(backupname)
            self.createincbackup(incbackupList)
        else:
            excluded = ''
            if self.exclude.isChecked():
                for index in range(self.listExclude.count()):
                    excluded = excluded + " --exclude=" + str(self.listExclude.item(index).text())
            now = datetime.today()
            now = str(now).replace(' ','-').split('.')[0]
            backupname = self.editLineIncBackupName.text()+now
            backupsrc= self.editLineIncBackupSrc.text()
            backupdst = self.editLineIncBackupDst.text()
            metaname = self.editLineIncBackupMetaName.text()
            incbackupList.append(metaname)
            incbackupList.append('0')
            incbackupList.append(str(now))
            incbackupList.append(backupname)
            incbackupList.append(backupsrc)
            incbackupList.append(backupdst)
            incbackupList.append(excluded)
            self.createnewincbackup(incbackupList)

    def createincbackup(self,incbackupList):
        global cur
        try:
            query = "SELECT * FROM IncrementalBackups WHERE metaname=?"
            incbackups = cur.execute(query, (incbackupList[1],)).fetchall()
            incbackups = incbackups[0]
            c="tar -cvvpzg "+incbackups[6]+"/"+incbackupList[1]+"/"+incbackupList[1]+".snar "+" -f "+incbackups[6]+"/"+incbackupList[1]+"/"+incbackupList[2]+".tar.gz "+incbackups[7]+" "+incbackups[5]
            subprocess.run(c,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL ,shell=True,check=True)
        except Exception as e:
            self.status.setText(f"error occured during creating this incremental backup {incbackupList[2]}\n{e}")
        else:
            maxlevel = self.getlastlevel(incbackupList[1])
            maxlevel+=1
            query = "INSERT INTO IncrementalBackups (metaname,level,date,name,srcpath,dstpath,excluded) VALUES (?,?,?,?,?,?,?)"
            cur.execute(query, (incbackupList[1],maxlevel,incbackupList[0], incbackupList[2], incbackups[5], incbackups[6], incbackups[7]))
            con.commit()

            result=f"{incbackupList[2]} has been created succesfully! \n{incbackups[6]}/{incbackupList[1]}/{incbackupList[2]}.tar.gz"
            self.progeesBar.setValue(1)
            self.status.setText(result)

    def getlastlevel(self,metaname):
        global cur
        query = "SELECT MAX(level) FROM IncrementalBackups WHERE metaname=?"
        maxlevel = cur.execute(query,(metaname,)).fetchone()
        maxlevel = int(maxlevel[0])
        return maxlevel

    def createnewincbackup(self,incbackupList):
        global cur
        try:
            subprocess.run(f'mkdir {incbackupList[5]}/{incbackupList[0]}', shell=True)
            c="tar -cvvpzg "+incbackupList[5]+"/"+incbackupList[0]+"/"+incbackupList[0]+".snar "+" -f "+incbackupList[5]+"/"+incbackupList[0]+"/"+incbackupList[3]+".tar.gz "+incbackupList[6]+" "+incbackupList[4]
            subprocess.run(c,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL ,shell=True,check=True)
        except Exception as e:
            self.status.setText(f"error occured during creating this incremental backup {incbackupList[3]}")
        else:
            query = "INSERT INTO IncrementalBackups (metaname,level,date,name,srcpath,dstpath,excluded) VALUES (?,?,?,?,?,?,?)"
            cur.execute(query, (incbackupList[0],incbackupList[1],incbackupList[2], incbackupList[3], incbackupList[4], incbackupList[5], incbackupList[6]))
            con.commit()

            result=f"{incbackupList[3]} has been created succesfully! \n{incbackupList[5]}/{incbackupList[0]}/{incbackupList[3]}.tar.gz"
            self.progeesBar.setValue(1)
            self.status.setText(result)

    def cancelAction(self):
        self.close()


class DeleteFullBackupWindow(QWidget):
    def __init__(self,d):
        super().__init__()
        self.setGeometry(200,50,300,300)
        self.setWindowTitle("Delete Full Backups")
        self.listFullBackupsToDelete = d
        global con
        global cur
        con = sqlite3.connect('backup/backupshistory.db')
        cur = con.cursor()
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
        self.a = ', '.join(self.listFullBackupsToDelete)
        self.text = QLabel(f'\n\nAre You Sure You want To Delete The Following Full Backups :\n\n{self.a}')
        self.text2 = QLabel()
        self.topLayout.addWidget(QLabel("NOTE: the backups will be deleted from the tool's database\nif you wanted to delete them completely from your disk, delete them manually!"))
        self.topLayout.addWidget(self.text)
        self.topLayout.addWidget(self.text2)
        self.topLayout.addWidget(self.progeesBar)

    def submitAction(self):
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setMaximum(len(self.listFullBackupsToDelete))
            self.progeesBar.setValue(0)
            self.deletefullbackup(self.listFullBackupsToDelete)
        except Exception :
            QMessageBox.warning(self,'warning',f"error occured during deleteting this full backup\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def okAction(self):
        self.close()

    def deletefullbackup(self,ids):
        global con
        global cur
        text = ''
        i = 0
        for id in ids:
            try:
                query = "DELETE FROM FullBackups WHERE id=?"
                cur.execute(query, (int(id),))
                con.commit()
            except Exception as e :
                text += f"error occured during deleting this backup ID {str(id)}\n"
            else:
                text += f"{str(id)} backup ID deleted succesfully!\n"
            finally:
                i += 1
                self.progeesBar.setValue(i)
                self.text2.setText(text)

    def cancelAction(self):
        self.close()

class DeleteIncBackupWindow(QWidget):
    def __init__(self,d):
        super().__init__()
        self.setGeometry(200,50,300,300)
        self.setWindowTitle("Delete Incremental Backups")
        self.listIncBackupsToDelete = d
        global con
        global cur
        con = sqlite3.connect('backup/backupshistory.db')
        cur = con.cursor()
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
        self.a = ', '.join(self.listIncBackupsToDelete)
        self.text = QLabel(f'\n\nAre You Sure You want To Delete The Following Incremental Backups :\n\n{self.a}')
        self.text2 = QLabel()
        self.topLayout.addWidget(QLabel("NOTE: the backups will be deleted from the tool's database\nif you wanted to delete them completely from your disk, delete them manually!"))
        self.topLayout.addWidget(self.text)
        self.topLayout.addWidget(self.text2)
        self.topLayout.addWidget(self.progeesBar)

    def submitAction(self):
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setMaximum(len(self.listIncBackupsToDelete))
            self.progeesBar.setValue(0)
            self.deleteincbackup(self.listIncBackupsToDelete)
        except Exception :
            QMessageBox.warning(self,'warning',f"error occured during deleteting this incremental backup\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def okAction(self):
        self.close()

    def deleteincbackup(self,ids):
        global con
        global cur
        text = ''
        i = 0
        for id in ids:
            try:
                query = "DELETE FROM IncrementalBackups WHERE id=?"
                cur.execute(query, (int(id),))
                con.commit()
            except Exception as e :
                text += f"error occured during deleting this backup ID {str(id)}\n"
            else:
                text += f"{str(id)} backup ID deleted succesfully!\n"
            finally:
                i += 1
                self.progeesBar.setValue(i)
                self.text2.setText(text)

    def cancelAction(self):
        self.close()


class RestoreFullBackupWindow(QWidget):
    def __init__(self,d):
        super().__init__()
        self.setGeometry(200,50,300,300)
        self.setWindowTitle("Restore Full Backup")
        self.fullBackupsToRestore = d
        global con
        global cur
        con = sqlite3.connect('backup/backupshistory.db')
        cur = con.cursor()
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
        self.lineEditrestoringDst = QLineEdit()
        self.lineEditrestoringDst.setPlaceholderText('where you are going to restore your full backup')
        self.text = QLabel('')
        self.topLayout.addWidget(QLabel('Restoring Destination : '))
        self.topLayout.addWidget(self.lineEditrestoringDst)
        self.topLayout.addWidget(self.text)
        self.topLayout.addWidget(self.progeesBar)

    def submitAction(self):
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setMaximum(1)
            self.progeesBar.setValue(0)
            self.restorefullbackup(self.fullBackupsToRestore)
        except Exception :
            QMessageBox.warning(self,'warning',f"error occured during restoring this full backup\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def okAction(self):
        self.close()

    def restorefullbackup(self,id):
        global con
        global cur
        text = ''
        try:
            query = "SELECT name,dstpath FROM FullBackups WHERE id=?"
            fullbackup = cur.execute(query,(int(id),)).fetchone()
            c= f"tar -xvvpzf {fullbackup[1]}/{fullbackup[0]}.tar.gz -C {self.lineEditrestoringDst.text()}"
            subprocess.run(c, shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except Exception as e :
            text += f"error occured during restoring this backup ID {str(id)}\n"
        else:
            text += f"{str(id)} backup ID restored succesfully!\n{str(id)}"
        finally:
            self.progeesBar.setValue(1)
            self.text.setText(text)

    def cancelAction(self):
        self.close()


class RestoreIncBackupWindow(QWidget):
    def __init__(self,incBackupList):
        super().__init__()
        self.setGeometry(200,50,300,300)
        self.setWindowTitle("Restore Incremental Backup")
        self.incBackupList=incBackupList
        global con
        global cur
        con = sqlite3.connect('backup/backupshistory.db')
        cur = con.cursor()
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()
        self.form = QFormLayout()

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
        self.container=QHBoxLayout()
        self.icon=QLabel('=>')
        self.combobeginning=QComboBox()
        self.comboend=QComboBox()
        self.container.addWidget(self.combobeginning)
        self.container.addWidget(self.icon)
        self.container.addWidget(self.comboend)
        self.container.addStretch()

        self.alllevels=QCheckBox('All Levels')
        self.alllevels.stateChanged.connect(self.alllevelsAction)

        self.cretecombo()

        self.topLayout.addWidget(self.txt)
        self.topLayout.addWidget(self.combo)
        self.topLayout.addWidget(self.alllevels)

        self.lineEditrestoringDst = QLineEdit()
        self.lineEditrestoringDst.setPlaceholderText('where you are going to restore your incremental backup')
        self.text = QLabel('')
        self.topLayout.addLayout(self.container)
        self.topLayout.addWidget(QLabel('Restoring Destination : '))
        self.topLayout.addWidget(self.lineEditrestoringDst)
        self.topLayout.addWidget(self.text)
        self.topLayout.addWidget(self.progeesBar)

    def alllevelsAction(self):
        if self.alllevels.isChecked():
            self.combobeginning.setHidden(True)
            self.comboend.setHidden(True)
            self.icon.setHidden(True)
        else:
            self.combobeginning.setHidden(False)
            self.comboend.setHidden(False)
            self.icon.setHidden(False)

    def cretecombo(self):
        self.combo=QComboBox()
        self.txt = QLabel('Chose Meta Name :')
        self.combo.currentTextChanged.connect(self.updateLevels)
        for item in self.incBackupList:
            self.combo.addItem(item)

    def updateLevels(self,value):
        global cur
        if self.alllevels.isChecked():
            pass
        else:
            self.combobeginning.clear()
            self.comboend.clear()
            query = "SELECT level FROM IncrementalBackups WHERE metaname=? ORDER BY LEVEL ASC"
            levels = cur.execute(query, (value,)).fetchall()
            for item in levels:
                self.combobeginning.addItem(str(item[0]))
                self.comboend.addItem(str(item[0]))

    def submitAction(self):
        global cur
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setMaximum(1)
            self.progeesBar.setValue(0)
            self.restoreincbackup()
        except Exception :
            QMessageBox.warning(self,'warning',f"error occured during restoring these incremental backups\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def okAction(self):
        self.close()

    def restoreincbackup(self):
        global cur
        try:
            query = "SELECT metaname,name,dstpath FROM IncrementalBackups "
            incbackups = cur.execute(query).fetchall()
            restoreDst=self.lineEditrestoringDst.text()
            begin = int(self.combobeginning.currentText())
            end = int(self.comboend.currentText())
            if self.alllevels.isChecked():
                for incbackup in incbackups:
                    c=f"tar --extract --verbose --verbose --preserve-permissions --listed-incremental=/dev/null --file={incbackup[2]}/{incbackup[0]}/{incbackup[1]}.tar.gz  --directory={restoreDst}"
                    subprocess.run(c,shell=True)
            else:
                for incbackup in incbackups[begin:end]:
                    c=f"tar --extract --verbose --verbose --preserve-permissions --listed-incremental=/dev/null --file={incbackup[2]}/{incbackup[0]}/{incbackup[1]}.tar.gz  --directory={restoreDst}"
                    subprocess.run(c,shell=True)
        except Exception as e :
            self.text.setText(f"error occured during restoring these backups\n{e}")
        else:
            self.text.setText("Backups restored succesfully!")
        finally:
            self.progeesBar.setValue(1)

    def cancelAction(self):
        self.close()


class MoreFullBackupWindow(QWidget):
    def __init__(self,id):
        super().__init__()
        self.setGeometry(50,50,900,400)
        self.setWindowTitle('Backup Contents')
        self.id = id
        self.layouts()
        self.getFullBackupContents(id)

    def layouts(self):
        self.container=QHBoxLayout(self)
        self.text = QLabel()
        self.container.addWidget(self.text)
        self.groupBox = QGroupBox()

        self.groupBox.setLayout(self.container)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)

        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.okBtn=QPushButton("Ok")
        self.okBtn.clicked.connect(self.okAction)
        self.okBtn.setFixedHeight(30)
        self.okBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )

        self.topLayout.addWidget(self.scroll)
        self.bottomLayout.addWidget(self.okBtn)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def getFullBackupContents(self,id):
        try:
            con = sqlite3.connect('backup/backupshistory.db')
            cur = con.cursor()
        except Exception:
            QMessageBox.critical(self,'error',"error occured, can't open connection with backupshistory.db")
        else:
            try:
                query = "SELECT name,dstpath FROM FullBackups WHERE id=?"
                fullbackup = cur.execute(query,(int(id),)).fetchone()
                self.setWindowTitle(f'Backup Contents {fullbackup[1]}/{fullbackup[0]}')
                c= f"tar --list --verbose --verbose --file={fullbackup[1]}/{fullbackup[0]}.tar.gz"
                out = subprocess.run(c, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                self.text.setText(str(out.stdout.decode('utf-8')))
            except Exception as e :
                self.text.setText(f"error occured during getting contents of this backup ID {str(id)}\n{e}")

    def okAction(self):
        self.close()


class MoreIncBackupWindow(QWidget):
    def __init__(self,id):
        super().__init__()
        self.setGeometry(50,50,900,400)
        self.setWindowTitle('Backup Contents')
        self.id = id
        self.layouts()
        self.getIncBackupContents(id)

    def layouts(self):
        self.container=QHBoxLayout(self)
        self.text = QLabel()
        self.container.addWidget(self.text)
        self.groupBox = QGroupBox()

        self.groupBox.setLayout(self.container)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)

        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.okBtn=QPushButton("Ok")
        self.okBtn.clicked.connect(self.okAction)
        self.okBtn.setFixedHeight(30)
        self.okBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )

        self.topLayout.addWidget(self.scroll)
        self.bottomLayout.addWidget(self.okBtn)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def getIncBackupContents(self,id):
        try:
            con = sqlite3.connect('backup/backupshistory.db')
            cur = con.cursor()
        except Exception:
            QMessageBox.critical(self,'error',"error occured, can't open connection with backupshistory.db")
        else:
            try:
                query = "SELECT metaname,name,dstpath FROM IncrementalBackups WHERE id=?"
                incbackup = cur.execute(query,(int(id),)).fetchone()
                self.setWindowTitle(f'Backup Contents {incbackup[2]}/{incbackup[0]}/{incbackup[1]}.tar.gz')
                c= f"tar --list --verbose --verbose --file={incbackup[2]}/{incbackup[0]}/{incbackup[1]}.tar.gz"
                out = subprocess.run(c, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                self.text.setText(str(out.stdout.decode('utf-8')))
            except Exception as e :
                self.text.setText(f"error occured during getting contents of this backup ID {str(id)}\n{e}")

    def okAction(self):
        self.close()
