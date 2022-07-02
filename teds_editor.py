# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'teds-editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_editorMainWindow(object):
    def setupUi(self, editorMainWindow):
        editorMainWindow.setObjectName("editorMainWindow")
        editorMainWindow.resize(892, 610)
        self.centralwidget = QtWidgets.QWidget(editorMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.metaTedsTab_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.metaTedsTab_2.setGeometry(QtCore.QRect(4, 0, 891, 561))
        self.metaTedsTab_2.setObjectName("metaTedsTab_2")
        self.metaTedsTab = QtWidgets.QWidget()
        self.metaTedsTab.setObjectName("metaTedsTab")
        self.metaTedsTable = QtWidgets.QTableWidget(self.metaTedsTab)
        self.metaTedsTable.setGeometry(QtCore.QRect(10, 10, 861, 461))
        self.metaTedsTable.setColumnCount(3)
        self.metaTedsTable.setObjectName("metaTedsTable")
        self.metaTedsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.metaTedsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.metaTedsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.metaTedsTable.setHorizontalHeaderItem(2, item)
        self.pushButton = QtWidgets.QPushButton(self.metaTedsTab)
        self.pushButton.setGeometry(QtCore.QRect(10, 480, 93, 41))
        self.pushButton.setObjectName("pushButton")
        self.metaTedsTab_2.addTab(self.metaTedsTab, "")
        self.channelTedsTab_2 = QtWidgets.QWidget()
        self.channelTedsTab_2.setObjectName("channelTedsTab_2")
        self.transducerChannelTable = QtWidgets.QTableWidget(self.channelTedsTab_2)
        self.transducerChannelTable.setGeometry(QtCore.QRect(10, 11, 861, 461))
        self.transducerChannelTable.setColumnCount(3)
        self.transducerChannelTable.setObjectName("transducerChannelTable")
        self.transducerChannelTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.transducerChannelTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transducerChannelTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.transducerChannelTable.setHorizontalHeaderItem(2, item)
        self.metaTedsTab_2.addTab(self.channelTedsTab_2, "")
        editorMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(editorMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 892, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        editorMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(editorMainWindow)
        self.statusbar.setObjectName("statusbar")
        editorMainWindow.setStatusBar(self.statusbar)
        self.actionSave_bin = QtWidgets.QAction(editorMainWindow)
        self.actionSave_bin.setObjectName("actionSave_bin")
        self.actionSabe_xml = QtWidgets.QAction(editorMainWindow)
        self.actionSabe_xml.setObjectName("actionSabe_xml")
        self.actionLoad_bin = QtWidgets.QAction(editorMainWindow)
        self.actionLoad_bin.setObjectName("actionLoad_bin")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_bin)
        self.menuFile.addAction(self.actionLoad_bin)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(editorMainWindow)
        self.metaTedsTab_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(editorMainWindow)

    def retranslateUi(self, editorMainWindow):
        _translate = QtCore.QCoreApplication.translate
        editorMainWindow.setWindowTitle(_translate("editorMainWindow", "IEEE 1451.0 TEDS Editor"))
        item = self.metaTedsTable.horizontalHeaderItem(0)
        item.setText(_translate("editorMainWindow", "Field"))
        item = self.metaTedsTable.horizontalHeaderItem(1)
        item.setText(_translate("editorMainWindow", "Value"))
        item = self.metaTedsTable.horizontalHeaderItem(2)
        item.setText(_translate("editorMainWindow", "Include"))
        self.pushButton.setText(_translate("editorMainWindow", "Generate UUID"))
        self.metaTedsTab_2.setTabText(self.metaTedsTab_2.indexOf(self.metaTedsTab), _translate("editorMainWindow", "Meta TEDS"))
        item = self.transducerChannelTable.horizontalHeaderItem(0)
        item.setText(_translate("editorMainWindow", "Field"))
        item = self.transducerChannelTable.horizontalHeaderItem(1)
        item.setText(_translate("editorMainWindow", "Value"))
        item = self.transducerChannelTable.horizontalHeaderItem(2)
        item.setText(_translate("editorMainWindow", "Include"))
        self.metaTedsTab_2.setTabText(self.metaTedsTab_2.indexOf(self.channelTedsTab_2), _translate("editorMainWindow", "TransducerChannel TEDS"))
        self.menuFile.setTitle(_translate("editorMainWindow", "File"))
        self.actionSave_bin.setText(_translate("editorMainWindow", "Save .bin"))
        self.actionSabe_xml.setText(_translate("editorMainWindow", "Sabe .xml"))
        self.actionLoad_bin.setText(_translate("editorMainWindow", "Load .bin"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    editorMainWindow = QtWidgets.QMainWindow()
    ui = Ui_editorMainWindow()
    ui.setupUi(editorMainWindow)
    editorMainWindow.show()
    sys.exit(app.exec_())
