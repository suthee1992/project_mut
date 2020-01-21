# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\root\Desktop\MUT\MUT_Project\frida-script\GUI\hook_process2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import sqlite3 as DB

from PyQt5 import QtCore, QtGui, QtWidgets
import _thread
import sys 
import trace 
import threading 
import time
import frida, sys
class thread_with_trace(threading.Thread): 
  def __init__(self, *args, **keywords): 
    threading.Thread.__init__(self, *args, **keywords) 
    self.killed = False
  
  def start(self): 
    self.__run_backup = self.run 
    self.run = self.__run       
    threading.Thread.start(self) 
  
  def __run(self): 
    sys.settrace(self.globaltrace) 
    self.__run_backup() 
    self.run = self.__run_backup 
  
  def globaltrace(self, frame, event, arg): 
    if event == 'call': 
      return self.localtrace 
    else: 
      return None
  
  def localtrace(self, frame, event, arg): 
    if self.killed: 
      if event == 'line': 
        raise SystemExit() 
    return self.localtrace 
  
  def kill(self): 
    self.killed = True

def hook_process(input_user2):
    print("hook process")
    jscode = """

    recv('input_user', function input_user(user_message) {  

    //console.log("Script loaded successfully ");
    //send("Script loaded successfully");
    Java.perform(function () {
    
    console.log("Inside java perform function");
    
    var MainActivity = Java.use("com.example.simple_app101.MainActivity");

    
    var my_class = Java.use("com.example.simple_app101.encryption_decryption");
    var my_class2 = Java.use("com.example.simple_app101.encryption_decryption");
    console.log("debug2");

    // thread hook encrpytion fun
    my_class.encrypt.implementation = function (data, key) { //hooking the old function
    console.log(user_message.payload);

    user_message.payload="loop2";
    console.log("Paint Text Before Encrpytion");
	  console.log("data-->" + data);
  	data='{"password":"1234","email":"suthee@hotmail.com"}';
  	console.log("data_edit-->" + data);
	  var ret_value_encrypt = this.encrypt(data, key);
	  return ret_value_encrypt;
    };


     //thread hook decrpytion fun
    my_class2.decrypt.implementation = function (data, key) { //hooking the old function
        console.log("Paint Text ->API Response ");
        var ret_value_decrypt = this.decrypt(data, key);
	    console.log("data-->" + ret_value_decrypt);
    
        return ret_value_decrypt;
    };

     console.log("Wait hook");
    
     
    });
    });
    """
    def on_message(message,data):
        print(message['payload'])
    
        

    process = frida.get_usb_device().attach('com.example.simple_app101')
    script = process.create_script(jscode)
    script.on('message', on_message)
    script.load()
    message='hello kim'
    script.post({"type": "input_user","payload": message})
    message='hello kim2'
    script.post({"type": "input_user","payload": message})
    sys.stdin.read()
    
    
    
def start_process():
    #open app start frida hook
    input_user=""
    t1 = thread_with_trace(target = hook_process,args=(input_user,)) 
    t1.start() 
    #time.sleep(20)
    #print("end stop hook")
    #t1.kill()

def print_history_table(self):
        Original_Request="{Original_Request:'aaaa10'}"
        Modified_Request="{Modified_Request:'aaaa20'}"
        Original_Response="{Original_Response:'bbbb10'}"
        Modified_Response="{Modified_Response:'bbbb20'}"
        result=query_db(Original_Request,Modified_Request,Original_Response,Modified_Response)
        self.tableWidget.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for colum_number,data in enumerate(row_data):
                self.tableWidget.setItem(row_number,colum_number,QtWidgets.QTableWidgetItem(str(data)))

    

def insert_db(Original_Request,Modified_Request,Original_Response,Modified_Response):
    con=DB.connect('hook_process_db.sqlite')
    with con:
            ##print(Original_Request,Modified_Request,Original_Response,Modified_Response)
            cur=con.cursor()
            cur.execute("insert into history values(?,?,?,?,datetime('now', 'localtime'))",(Original_Request,Modified_Request,Original_Response,Modified_Response))
            print("insert success")
    con.close()
   
   
def query_db(Original_Request,Modified_Request,Original_Response,Modified_Response):
        con=DB.connect('hook_process_db.sqlite')
        with con:
                #print(Original_Request,Modified_Request,Original_Response,Modified_Response)
                cur=con.cursor()
                cur.execute("select rowid,* from history;")
                rows = cur.fetchall()
                return rows

        con.close()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(731, 401)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 721, 381))
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 701, 311))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setObjectName("tableWidget")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(110, 10, 201, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 10, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.checkBox_4 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_4.setGeometry(QtCore.QRect(140, 80, 101, 16))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_3 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 80, 111, 16))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_2.setGeometry(QtCore.QRect(140, 60, 101, 21))
        self.checkBox_2.setObjectName("checkBox_2")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(370, 140, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 20, 121, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listView = QtWidgets.QListView(self.tab_2)
        self.listView.setGeometry(QtCore.QRect(20, 50, 281, 221))
        self.listView.setObjectName("listView")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab_2)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 10, 271, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton_3.clicked.connect(self.openFile)
        print_history_table(self)
        start_process()
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", " History"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "History"))
        self.label.setText(_translate("MainWindow", "Search"))
        self.pushButton_2.setText(_translate("MainWindow", "Search"))
        self.checkBox_4.setText(_translate("MainWindow", "Modify Response"))
        self.checkBox.setText(_translate("MainWindow", "Original Request"))
        self.checkBox_3.setText(_translate("MainWindow", "Original Response"))
        self.checkBox_2.setText(_translate("MainWindow", "Modify Request"))
        self.pushButton.setText(_translate("MainWindow", "Print Message"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Search"))
        self.pushButton_3.setText(_translate("MainWindow", "Upload Word List"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Upload Word List"))

    

    def openFile(self):
        #t=_thread.start_new_thread( hook_process, ("Thread-1",self,))

        #hook=Process(target=hook_process,args=self)
        
        #hook_process(self)
        #print("openfile")
        #print_history_table(self)
     

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
    