# -*- coding: utf-8 -*-

import os
import sys
import time
from functools import partial
from urllib import request

import yaml
#from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QPixmap, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QFormLayout, QGridLayout, QGroupBox,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QPushButton, QRadioButton, QTableView, QTextEdit,
                             QVBoxLayout, QWidget, QComboBox)

from uptime import upostime

ConfigFileName = "RunTool.yaml"
MaxLogRows = 10
DefaultNtp = 's1a.time.edu.cn'

__author__ = "Wang MingJun"

EnCoding = 'utf-8'

def getruntoken(url):
    try:
        response = request.urlopen(url, timeout=5)
    except TimeoutError:
        pass
    else:
        token = response.read()
        print(token)
        return bytes.decode(token)


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

class WinMain(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        # mainLayout.addWidget(self.buttonlayout)
        # line 1
        if self.loadconfig():
            self.createButtonLayout()
            mainLayout.addLayout(self.buttonlayout)
        # line 2
        self.textedit = QLineEdit()
        button = QPushButton('跟新')
        button.clicked.connect(self.gettoken)
        # self.textedit.setText(getruntoken(self.config['url']))
        self.textedit.setReadOnly(True)
        # self.textedit.setEnabled(False)

        layout2 = QGridLayout()
        layout2.addWidget(QLabel('参数'), 0, 0)
        layout2.addWidget(self.textedit, 0, 1)
        layout2.addWidget(button, 0, 2)

        # self.layout2 = layout2
        self.line2layout = layout2
        mainLayout.addLayout(layout2)
        # line 3
        if self.timeautoup:
            self.line3layout = QGridLayout()
            self.line3layout.addWidget(QLabel('ntp'), 0, 0)
            self.nptedit = QLineEdit()
            self.nptedit.setText(self.ntpaddr)
            # self.nptedit.setReadOnly(True)
            self.line3layout.addWidget(self.nptedit, 0, 1)
            self.radio1 = QRadioButton('系统时间自动跟新')
            # if self.timeautoup:
            self.radio1.setChecked(True)
            self.line3layout.addWidget(self.radio1, 0, 2)
            button2 = QPushButton('跟新系统时间')
            button2.clicked.connect(self.uptime)
            self.line3layout.addWidget(button2, 0, 3)

        combo = QComboBox(self)
        self.confignamelist = []
        for configname in self.config['RunTool']:
            self.confignamelist.append(configname)
            combo.addItem(configname)
        combo.setCurrentText(self.sel)
        combo.currentIndexChanged.connect(self.changesel)
        self.combo = combo
        #self.connect(combo, QtCore.SIGNAL('activated(QString)'), self.OnActivated)
        if self.timeautoup:
            self.line3layout.addWidget(combo, 0, 4)
            mainLayout.addLayout(self.line3layout)
        else:
            self.line2layout.addWidget(combo, 0, 3)

        # log tableview
        self.loglayout = QGridLayout()
        self.model = QStandardItemModel(0, 1)
        self.model.setHorizontalHeaderLabels(['日志'])
        # for row in range(100):
        #    for column in range(3):
        #        item = QStandardItem("row %s, column %s" % (row, column))
        #        self.model.setItem(row, column, item)
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        # 下面代码让表格填满窗口
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.verticalHeader.
        self.loglayout.addWidget(self.tableView)
        mainLayout.addLayout(self.loglayout)

        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 540, 350)
        self.setWindowTitle('RunTool v1.0 Author:wmj')
        # self.show()


    def createButtonLayout(self):
        #self.buttonGroupBox = QGroupBox("Button layout")
        self.buttonlayout = QGridLayout()
        # layout.setSpacing(10)
        self.buttons = []
        # print(self.config['RunTool'][0])
        # for i in self.config['RunTool'][0]["button"]:
        for index, button in enumerate(self.buttonconfig):
            print(index, " ", button)
            btn = QPushButton(button["name"], self)
            btn.clicked.connect(partial(self.line1button_click, index))
            self.buttonlayout.addWidget(btn, 1, index)
            self.buttons.append(btn)
        #self.buttonlayout = layout

    def ButtonLayoutreLoad(self):
        clearLayout(self.buttonlayout)
        self.buttons.clear()
        for index, button in enumerate(self.buttonconfig):
            print(index, " ", button)
            btn = QPushButton(button["name"], self)
            btn.clicked.connect(partial(self.line1button_click, index))
            self.buttonlayout.addWidget(btn, 1, index)
            self.buttons.append(btn)
        #self.buttonlayout.update()
        # widget.setLayout(layout)

    def clearlog(self):
        self.model.removeRows(0, self.model.rowCount())

    def addlog(self, log):
        if self.model.rowCount() > MaxLogRows - 1:
            self.model.removeRow(0)
        #self.model.appendRow([ QStandardItem(QDateTime.currentDateTime().toString("hh:mm:ss.zzz") +" " + log) ])
        self.model.appendRow([QStandardItem(time.strftime("%T") + " " + log)])

    def loadconfig(self):
        try:
            configfile = open(ConfigFileName, 'r', encoding=EnCoding)
            self.config = yaml.load(configfile)
            configfile.close()
            runtoolconfig = None
            if 'sel' in self.config:
                self.sel = self.config['sel']
                if self.sel in self.config['RunTool']:
                    runtoolconfig = self.config['RunTool'][self.sel]
                # for tmpconfig in self.config['RunTool']:
                #    if tmpconfig['name'] is self.sel:
                #        runtoolconfig = tmpconfig
                #        break
            if runtoolconfig is None:
                #self.runtoolconfig = self.config['RunTool'].items()[0]
                self.sel = self.config['RunTool'].keys()[0]
                self.runtoolconfig = self.config['RunTool'][self.sel]
            else:
                self.runtoolconfig = runtoolconfig
            self.workdir = self.runtoolconfig['workdir']
            self.buttonconfig = self.runtoolconfig['button']
            self.ntpaddr = self.config['ntp']
            self.timeautoup = self.config['autouptime']
            # print(self.config)
            print("url=", self.config['url'])
            return True
        except IOError:
            return False

    def saveconfig(self):
        f = open(ConfigFileName, "w", encoding=EnCoding)
        print(yaml.dump(self.config, f,  default_flow_style=False,
                        encoding=EnCoding, allow_unicode=True))
        #print(cofing)
        f.close()

    def changesel(self, selidx):
        print(selidx)
        selstr = self.confignamelist[selidx]
        if not self.sel is selstr:
            if selstr in self.config['RunTool']:
                self.sel = selstr
                self.config['sel'] = selstr
                self.saveconfig()
                self.runtoolconfig = self.config['RunTool'][self.sel]
                self.workdir = self.runtoolconfig['workdir']
                self.buttonconfig = self.runtoolconfig['button']
                # ToDo: reload layout1 ui:
                self.ButtonLayoutreLoad()

    def uptime(self):
        ntpadd = self.nptedit.text()
        upostime(ntpadd)

    def gettoken(self):
        self.token = getruntoken(self.config['url'])
        self.textedit.setText(self.token)
        self.addlog("gettoken " + self.token)
        return self.token

    def docmd(self, cmd):
        os.chdir(self.workdir)
        os.system(cmd)
        self.addlog("docmd " + cmd)

    def line1button_click(self, idx):
        print("idx=", idx)
        bat = self.buttonconfig[idx]['cmd']
        if idx == 0:
            if self.radio1.isChecked():
                self.uptime()
            token = self.gettoken()
            self.docmd(bat + " " + token)
        else:
            self.docmd(bat)


if __name__ == '__main__':

    # print(config)
    app = QApplication(sys.argv)
    ex = WinMain()
    ex.show()
    sys.exit(app.exec_())
