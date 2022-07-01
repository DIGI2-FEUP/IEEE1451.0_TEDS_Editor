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
import datetime
from teds_editor import Ui_editorMainWindow
from  teds_data_model import TEDS_ACCESS_CODES, Meta_TEDS_Data_Block, Meta_TEDS_Data_Block, TransducerChannel_TEDS_Data_Block
import teds_utils

# Create meta teds model
meta_teds = Meta_TEDS_Data_Block()
# Create channel teds model
channel_teds = TransducerChannel_TEDS_Data_Block()

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_editorMainWindow()
        self.ui.setupUi(self)
        #self.loadTedsMetaTable()
        #self.loadChannelTeds()
        # Register handle for Generate UUID btn
        self.ui.pushButton.clicked.connect(self.generateUUID)
        # Register handle for Save .bin action
        self.ui.actionSave_bin.triggered.connect(self.saveBin)
        # Init the MetaTEDS table
        self.ui.metaTedsTable.setColumnWidth(0, 400)
        self.ui.metaTedsTable.setColumnWidth(1, 200)
        self.load_teds_data_block(self.ui.metaTedsTable, meta_teds, metaTedsTableChange, None)
        # Init the ChannelTEDS table
        self.ui.transducerChannelTable.setColumnWidth(0, 400)
        self.ui.transducerChannelTable.setColumnWidth(1, 300)
        self.load_teds_data_block(self.ui.transducerChannelTable, channel_teds, channelTedsTableChange, channelTedsComboBoxChanged)

    def load_teds_data_block(self, qtable, teds_data_block, table_edit_callback, combobox_edit_callback):
        # Set the table number of rows
        qtable.setRowCount(len(teds_data_block.fields))
        # Iterate all fields of the teds data block
        for i in range(0,len(teds_data_block.fields)):
            field = teds_data_block.fields[i]
            if field.enum :
                # If the TEDS field domain is an enumeration, use a combobox
                # Use the enumeration to fill the combobox with values
                combo = QtWidgets.QComboBox()                
                combo.currentTextChanged.connect(lambda value, index=i: combobox_edit_callback(value, index))
                for value in field.enum:
                    combo.addItem(value.name)
                qtable.setCellWidget(i,1,combo)
            else:
                # Else, assume the field value is an integer
                blankItem = QtWidgets.QTableWidgetItem()
                if i==0:
                    # Fisrt item is the teds identification field
                    # Make it not editable
                    blankItem.setData(QtCore.Qt.EditRole, TEDS_ACCESS_CODES(field.teds_class).name)
                    blankItem.setFlags(blankItem.flags() ^ QtCore.Qt.ItemIsEditable)
                else:
                    blankItem.setData(QtCore.Qt.EditRole, field.get_value())
                qtable.setItem(i, 1, blankItem)
            # Use the field description to set the description cell of the table
            item = QtWidgets.QTableWidgetItem(field.get_description())
            # Make the description not editable
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            qtable.setItem(i, 0, item)

        # Callback function to catch changes in the table items
        qtable.itemChanged.connect(table_edit_callback)

    def generateUUID(self):
        # Data model generate new uuid
        meta_teds.set_uuid(teds_utils.generate_uuid())
        # Get table uuid cell
        uuid_cell = self.ui.metaTedsTable.item(1, 1)
        # Display uuid as string, int not working
        print(meta_teds.uuid_field.get_value())
        uuid_cell.setData(QtCore.Qt.DisplayRole, meta_teds.uuid_field.get_value().hex('-'))

    def saveBin(self):
        # Name the file with uuid from meta teds
        tab_index = self.ui.metaTedsTab_2.currentIndex()
        if  tab_index == 0:
            metaTedsFile = open(meta_teds.uuid_field.get_value().hex('-')+".bin", "wb")
            metaTedsFile.write(meta_teds.to_bytes())
        elif tab_index == 1:
            channelTedsFile = open("channel_teds_"+datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')+".bin", "wb")
            channelTedsFile.write(channel_teds.to_bytes())

def metaTedsTableChange(item):
    # The item (cell) row is the same index of the TEDS field
    if item.row() != 1:
        # ignore UUID field changes
        meta_teds.fields[item.row()].set_value(item.data(QtCore.Qt.DisplayRole))

# Callback function for the channel TEDS comboboxes
def channelTedsComboBoxChanged(value, index):
    # Get the new value from the enum that defines the TEDS field domain
    new_value = channel_teds.fields[index].enum[value].value
    # Set the new value in the TEDS field
    channel_teds.fields[index].set_value(new_value)
    # print(channel_teds.fields[index].value)

# Callback function for the Channel TEDS table
def channelTedsTableChange(item):
    # The item (cell) row is the same index of the TEDS field
    channel_teds.fields[item.row()].set_value(item.data(QtCore.Qt.DisplayRole))
    # print(channel_teds.fields[item.row()].value)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()