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

#from ctypes import sizeof
import enum
import uuid
import enum
import teds_utils

from numpy import float32, uint16, uint8

#TEDS Access Codes for the TEDS defined by this standard
class TEDS_ACCESS_CODES(enum.IntEnum):
    MetaTEDS = 0x01
    MetaIdTEDS = 0x02
    ChanTEDS = 0x03
    ChanIdTEDS = 0x04
    CalTEDS = 0x05
    CalIdTEDS = 0x06
    EUASTEDS = 0x07
    FreqRespTEDS = 0x08
    TransferTEDS = 0x09
    CommandTEDS = 0x0A
    TitleTEDS = 0x0B
    XdcrName = 0x0C
    PHYTEDS = 0x0D
    GeoLocTEDS = 0x0E
    UnitsExtention = 0x0F

class TEDS_Block:

    def __init__(self, teds_data_block):
        self.teds_data_block = teds_data_block
        self.length = teds_utils.calc_length(self.value)
        self.checksum = teds_utils.calc_checksum(self.teds_data_block)

class TEDS_TLV_Block():

    def __init__(self, type, length, value):

        self.type = uint8(type)
        self.length = uint8(length)
        self.value = value

    def get_bytes(self):
        if isinstance(self.value, bytes):
            return bytes([self.type, self.length]).join(self.value)
        else:
            return bytes([self.type, self.length] + self.value)

class TEDS_Identifier_Structure():

    def __init__(self, teds_class):
        #TEDSID field type = 3
        self.type = 0x03
        #Fixed length of 4 bytess
        self.length = 0x04
        #TEDS IEEE 1451.0 family
        self.family = 0x00
        #This field identifies the TEDS being accessed.
        self.teds_class = uint8(teds_class)
        #Original version
        self.version = 0x01
        #TO-DO
        self.tuple_length = 0x01

    def get_tlv(self):
        return TEDS_TLV_Block(self.type, self.get_value(), self.length)

    def get_bytes(self):
        return bytes([self.family, self.teds_class, self.version, self.tuple_length])

    def get_value(self):
        return [self.family, self.teds_class, self.version, self.tuple_length]

class META_TEDS_TYPES():
    #0–2 — Reserved — —
    TEDSID = [3, 4, "TEDS Identification Header"]
    UUID = [4, 10, "Globally Unique Identifier UUID"]
    #5–9 — Reserved — —
    #Timing-related information
    OholdOff = [10, 4, "Operational time-out"]
    SHoldOff = [11, 4, "Slow-access time-out"]
    TestTime = [12, 4, "Self-Test Time"]
    #Number of implemented TransducerChannels
    MaxChan = [13, 2, "Number of implemented TransducerChannels"]
    CGroup = [14, 0, "CGroup ControlGroup information sub-block"]
    #Types 20, and 21 define one ControlGroup.
    #GrpType = [20,1,"ControlGroup type UInt8"]
    #MemList = [21,0,"ControlGroup member list array of UInt16"]
    VGroup = [15, 0, "VectorGroup information sub-block"]
    #Types 20 and 21 define one VectorGroup.
    #GrpType = [20,1,"VectorGroup type UInt8"]
    #MemList = [21,0,"VectorGroup member list array of UInt16"]
    GeoLoc = [16, 0, "Specialized VectorGroup for geographic location"]
    #Types 24, 20, and 21 define one set of geographic location information.
    #LocEnum = [24,1,"An enumeration defining how location information is provided UInt8"]
    #GrpType = [20,1,"VectorGroup type UInt8"]
    #MemList = [21,0,"VectorGroup member list array of UInt16"]
    Proxies = [17, 0, "TransducerChannel proxy definition sub-block"]
    #Types 22, 23, and 21 define one TransducerChannel proxy.
    #ChanNum = [22,1,"TransducerChannel number of the TransducerChannel proxy UInt16"]
    #Organiz = [23,1,"TransducerChannel proxy data-set organization UInt8"]
    #MemList = [21,0,"TransducerChannel proxy member list array of UInt16"]
    #18–19 — Reserved — —
    GrpType = [20, 1, "ControlGroup type"]
    MemList = [21, 0, "ControlGroup member list array"]
    ChanNum = [22, 1, "TransducerChannel number of the TransducerChannel proxy"]
    Organiz = [23, 1, "TransducerChannel proxy data-set organization"]
    LocEnum = [24, 1, "An enumeration defining how location information is provided"]
    #25–127 — Reserved — —
    #128–255 — Open to manufacturers — —
    EditableTypesList = [UUID, OholdOff, SHoldOff, TestTime, MaxChan]

class Meta_TEDS_Data_Block():

    def __init__(self):
        #TEDS Identification Header UInt8 4
        self.teds_id = TEDS_Identifier_Structure(TEDS_ACCESS_CODES.MetaTEDS)
        #Globally Unique Identifier UUID 10
        self.uuid = uuid.uuid4().bytes[:10]
        #OholdOff Operational time-out Float32 4
        self.oholdoff = float32(0)
        #SHoldOff Slow-access time-out Float32 4
        self.sholdoff = float32(0)
        #TestTime Self-Test Time Float32
        self.test_time = float32(0)
        #MaxChan Number of implemented TransducerChannels UInt16 2
        self.max_chan = uint16(0)

    #TO-DO
    def load(self):
        pass

    def set_uuid(self, uuid):
        self.uuid = uuid

    def set_oholdoff(self, oholdoff):
        self.oholdoff = float32(oholdoff)

    def set_sholdoff(self, sholdoff):
        self.sholdoff = float32(sholdoff)

    def set_test_time(self, test_time):
        self.test_time = float32(test_time)

    def set_max_chan(self, max_chan):
        self.max_chan = uint16(max_chan)

    def to_bytes(self):
        barray = bytearray(b'')
        barray.append(META_TEDS_TYPES.TEDSID[0])
        barray.append(META_TEDS_TYPES.TEDSID[1])
        barray.extend(self.teds_id.get_bytes())
        barray.append(META_TEDS_TYPES.UUID[0])
        barray.append(META_TEDS_TYPES.UUID[1])
        barray.extend(self.uuid)
        barray.append(META_TEDS_TYPES.OholdOff[0])
        barray.append(META_TEDS_TYPES.OholdOff[1])
        barray.extend(self.oholdoff)
        barray.append(META_TEDS_TYPES.SHoldOff[0])
        barray.append(META_TEDS_TYPES.SHoldOff[1])
        barray.extend(self.sholdoff)
        barray.append(META_TEDS_TYPES.TEDSID[0])
        barray.append(META_TEDS_TYPES.TEDSID[1])
        barray.extend(self.test_time)
        barray.append(META_TEDS_TYPES.MaxChan[0])
        barray.append(META_TEDS_TYPES.MaxChan[1])
        barray.extend(self.max_chan)
        return barray

class ControlGroup():

    def __init__(self, group_type):
        self.field_type = uint8(14)
        #GrpType ControlGroup type UInt8
        self.group_type = uint8(group_type)



# ba = Meta_TEDS_Data_Block().to_bytes()
# print([ "0x%02x" % b for b in ba ])