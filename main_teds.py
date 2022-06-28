# *****************************************************************************************
# *    Copyright 2022 by Digital and Intelligent Industry Lab (DIGI2), systecfof@fe.up.pt *
# *    You may use, edit, run or distribute this file                                     *
# *    as long as the above copyright notice remains                                      *
# * THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED           *
# * OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF                    *
# * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE.          *
# * DIGI2 Lab SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL,         *
# * OR CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.                                  *
# * For more information about the lab, see:                                              *
# * http://digi2.fe.up.pt                                                                 *
# *****************************************************************************************

from PyQt5 import QtWidgets, QtCore
import sys
from teds_editor import Ui_editorMainWindow
from  teds_data_model import Meta_TEDS_Data_Block, Meta_TEDS_Data_Block, TransducerChannel_TEDS_Data_Block
import teds_utils

# Create meta teds model
meta_teds = Meta_TEDS_Data_Block()

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_editorMainWindow()
        self.ui.setupUi(self)
        self.loadTedsMetaTable()
        self.loadChannelTeds()
        # Register handle for Generate UUID btn
        self.ui.pushButton.clicked.connect(self.generateUUID)
        # Register handle for Save .bin action
        self.ui.actionSave_bin.triggered.connect(self.saveBin)

    def loadTedsMetaTable(self):
        self.ui.metaTedsTable.setColumnWidth(0, 400)
        self.ui.metaTedsTable.setColumnWidth(1, 200)
        self.ui.metaTedsTable.setRowCount(9)
        # Set field description
        self.ui.metaTedsTable.setItem(0, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.UUID[2]))
        self.ui.metaTedsTable.setItem(1, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.OholdOff[2]))
        self.ui.metaTedsTable.setItem(2, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.SHoldOff[2]))
        self.ui.metaTedsTable.setItem(3, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.TestTime[2]))
        self.ui.metaTedsTable.setItem(4, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.MaxChan[2]))
        self.ui.metaTedsTable.setItem(5, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.CGroup[2]))
        self.ui.metaTedsTable.setItem(6, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.VGroup[2]))
        self.ui.metaTedsTable.setItem(7, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.GeoLoc[2]))
        self.ui.metaTedsTable.setItem(8, 0, QtWidgets.QTableWidgetItem(Meta_TEDS_Data_Block.Proxies[2]))

        for i in range(self.ui.metaTedsTable.rowCount()):
            item = self.ui.metaTedsTable.item(i, 0)
            # Make this item not editable
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            blankItem = QtWidgets.QTableWidgetItem()
            blankItem.setData(QtCore.Qt.EditRole, 0)
            self.ui.metaTedsTable.setItem(i, 1, blankItem)
            # Callback function to catch item changes
        self.ui.metaTedsTable.itemChanged.connect(metaTedsTableChange)

    def loadChannelTeds(self):
        tctdb = TransducerChannel_TEDS_Data_Block()
        self.ui.transducerChannelTable.setColumnWidth(0, 400)
        self.ui.transducerChannelTable.setColumnWidth(1, 200)
        self.ui.transducerChannelTable.setRowCount(len(tctdb.fields))
        # Set field description
        i = 0
        for field in tctdb.fields:
            self.ui.transducerChannelTable.setItem(i, 0, QtWidgets.QTableWidgetItem(field.get_description()))
            i += 1

        for i in range(self.ui.transducerChannelTable.rowCount()):
            item = self.ui.transducerChannelTable.item(i, 0)
            # Make this item not editable
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            blankItem = QtWidgets.QTableWidgetItem()
            blankItem.setData(QtCore.Qt.EditRole, 0)
            self.ui.transducerChannelTable.setItem(i, 1, blankItem)
            # Callback function to catch item changes

    def generateUUID(self):
        # Data model generate new uuid
        meta_teds.set_uuid(teds_utils.generate_uuid())
        # Get table uuid cell
        uuid_cell = self.ui.metaTedsTable.item(0, 1)
        # Display uuid as string, int not working
        uuid_cell.setData(QtCore.Qt.DisplayRole, meta_teds.uuid_field.get_value().hex())

    def saveBin(self):
        # Name the file with uuid from meta teds
        metaTedsFile = open(meta_teds.uuid_field.get_value().hex()+".bin", "wb")
        metaTedsFile.write(meta_teds.to_bytes())

def metaTedsTableChange(item):
    # TO-DO, implement remaining items
    if item.row() > 0 and item.row() < 5:
        print("Item row: {}, item column: {}, item value: {}\n".format(item.row(), item.column(), item.data(QtCore.Qt.DisplayRole)))
        if item.row() == 1:
            meta_teds.set_oholdoff(item.data(QtCore.Qt.DisplayRole))
        elif item.row() == 2:
            meta_teds.set_sholdoff(item.data(QtCore.Qt.DisplayRole))
        elif item.row() == 3:
            meta_teds.set_test_time(item.data(QtCore.Qt.DisplayRole))
        elif item.row() == 4:
            meta_teds.set_max_chan(item.data(QtCore.Qt.DisplayRole))
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()