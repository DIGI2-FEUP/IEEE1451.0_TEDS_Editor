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
from ctypes import sizeof
import enum
import uuid
import enum
import teds_utils

from numpy import float32, uint16, uint32, uint8, frombuffer

# Number of octets in Type, Length of a TEDS TLV field
TL_OCTETS = 2

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

# All TEDS prepared by a transducer manufacturer use a Type/Length/Value (TLV) data structure.
# The “Type“ field is a 1 octet tag that identifies the TLV, similar in function to HTML or XML tags. 
# The “Length” field specifies the number of octets of the value field.
# The “Value” field is the actual data.
class TEDS_TLV_Block():

    def __init__(self, teds_field):

        self.type = teds_field.get_type()
        self.length = teds_field.get_value_length()
        self.teds_field = teds_field

    #TO-DO correct this method
    def get_bytes(self):
        barr = bytearray(b'')
        try:
            barr.extend(self.type)
        except:
            barr.append(self.type)
        try:
            barr.extend(self.length)
        except:
            barr.append(self.length)
        try:
            barr.extend(self.teds_field.get_value())
        except:
            barr.append(self.teds_field.get_value())
        if len(barr) != self.length + TL_OCTETS:
            raise ValueError("TEDS field type: {}, expected encoding length is: {}, should be: {}"
                .format(self.type, len(barr)-TL_OCTETS, self.length))
        return barr

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

    def get_type(self):
        return self.type

    def get_TLV(self):
        return TEDS_TLV_Block(self)

    def get_bytes(self):
        return bytes([self.family, self.teds_class, self.version, self.tuple_length])

    def get_value(self):
        return [self.family, self.teds_class, self.version, self.tuple_length]
    
    def get_value_length(self):
        # Fixed length of 4 octects for this structure
        return 4

    def get_total_length(self):
        # Fixed length of 4 octects for this structure
        return self.get_value_length()+TL_OCTETS

    def load_bytes(self, barray):
        try:
            assert type(barray) is bytearray
            assert len(barray) == self.get_total_length()
            assert barray[0] == self.type
            assert barray[1] == self.length
            assert barray[2] == self.family
            assert barray[3] == self.teds_class
            assert barray[4] == self.version
            assert barray[5] == self.tuple_length
        except:
            raise ValueError("TEDS Identifier Structure, loaded bytes don't match.")

class TEDS_Field():

    def __init__(self, type, name, description, data_type, n_octets):
        self.type = uint8(type)
        self.name = name
        self.description = description
        self.data_type = data_type
        self.length = uint8(n_octets)
        self.value = None
        self.tlv = None

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_data_type(self):
        return self.data_type

    def get_value_length(self):
        # Fixed length of 4 octects for this structure
        return self.length

    def get_total_length(self):
        # Fixed length of 4 octects for this structure
        return self.get_value_length()+TL_OCTETS

    # Use reflection to cast the given value to the field data type
    # If iven value has the correct type, do not cast it
    def set_value(self, value):
        if type(value) != type(self.data_type):
            self.value = self.data_type.__class__(value)
        else:
            self.value = value

    def get_value(self):
        return self.value

    def get_TLV(self):
        if self.tlv == None:
            self.tlv = TEDS_TLV_Block(self)
        return self.tlv

    def get_bytes(self):
        return self.get_TLV.get_bytes()

    def load_bytes(self, barray):
        try:
            assert type(barray) is bytearray
            assert len(barray) == self.get_total_length()
            assert barray[0] == self.type
            assert barray[1] == self.length
            # First two elements of the buffer are type and 
            if type(self.data_type) == bytes:
                self.set_value(barray[TL_OCTETS:self.get_total_length()])
            else:
                self.set_value(frombuffer(barray[TL_OCTETS:self.get_total_length()], dtype=self.data_type.dtype))
        except:
            raise ValueError("TEDS Field: {}, loaded bytes don't match.".format(self.name))


# This class and GUI are not complete
# Only the types defined in the constructor can be used
# TO-DO: Implement all types from META_TEDS_TYPES
class Meta_TEDS_Data_Block():

    # This block holds the Meta TEDS fields defined in Table 43 — Structure of the Meta-TEDS data block
    # For each field, the list defines [field type, # octets, field description]
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
    # This list is used to work woth the editable fields
    EditableTypesList = [TEDSID, UUID, OholdOff, SHoldOff, TestTime, MaxChan]

    def __init__(self):
        self.fields = []
        #TEDS Identification Header UInt8 4
        self.teds_id = TEDS_Identifier_Structure(TEDS_ACCESS_CODES.MetaTEDS)
        self.fields.append(self.teds_id)
        #Globally Unique Identifier UUID 10
        self.uuid_field = TEDS_Field(3, "TEDSID", "TEDS Identification Header", bytes(),  10)
        self.uuid_field.set_value(uuid.uuid4().bytes[:10])
        self.fields.append(self.uuid_field)
        #OholdOff Operational time-out Float32 4
        self.oholdoff_field = TEDS_Field(10, "OholdOff", "Operational time-out", float32(), 4)
        self.oholdoff_field.set_value(0)
        self.fields.append(self.oholdoff_field)
        #SHoldOff Slow-access time-out Float32 4
        self.sholdoff_field = TEDS_Field(11, "SholdOff", "Slow-access time-out", float32(), 4)
        self.sholdoff_field.set_value(0)
        self.fields.append(self.sholdoff_field)
        #TestTime Self-Test Time Float32
        self.test_time_field = TEDS_Field(12, "TestTime", "Self-Test Time", float32(), 4)
        self.test_time_field.set_value(0)
        self.fields.append(self.test_time_field)
        #MaxChan Number of implemented TransducerChannels UInt16 2
        self.max_chan_field = TEDS_Field(13, "MaxChan", "Number of implemented TransducerChannels", uint16(), 2)
        self.max_chan_field.set_value(0)
        self.fields.append(self.max_chan_field)

    #TO-DO
    def load(self):
        pass

    # This method will only load a TEDS with the fields defined in the constructor
    # A Meta TEDS will all fields will fail to load
    def load_from_bytearray(self, bytearr):
        # bytearr must be 'bytearray object
        assert isinstance(bytearr, bytearray)

        # Current position in bytearray
        seek = 0
        for field in self.fields:
            # print("Loading array section: {} - {}".format(seek,seek + field.get_total_length()))
            # print("Section size: {}".format(len(bytearr[seek:seek + field.get_total_length()])))
            # print(bytearr[seek:seek + field.get_total_length()])
            field.load_bytes(bytearr[seek:seek + field.get_total_length()])
            seek += field.get_total_length()

    def set_uuid(self, uuid):
        self.uuid_field.set_value(uuid)

    def set_oholdoff(self, oholdoff):
        self.oholdoff_field.set_value(oholdoff)

    def set_sholdoff(self, sholdoff):
        self.sholdoff_field.set_value(sholdoff)   

    def set_test_time(self, test_time):
        self.test_time_field.set_value(test_time)

    def set_max_chan(self, max_chan):
        self.max_chan_field.set_value(max_chan)

    def to_bytes(self):
        barray = bytearray(b'')
        for field in self.fields:
            try:
                barray.append(field.get_TLV().get_bytes())
            except:
                barray.extend(field.get_TLV().get_bytes())
        return barray

class ControlGroup():

    def __init__(self, group_type):
        self.field_type = uint8(14)
        #GrpType ControlGroup type UInt8
        self.group_type = uint8(group_type)


# ba = Meta_TEDS_Data_Block()
# print([ "0x%02x" % b for b in ba.to_bytes()])

# fh = open('b4cf95ef3ca347729fa1.bin', 'rb')
# barray = bytearray(b'')
# try:
#     barray = bytearray(fh.read())
# finally:
#     fh.close
# ba.load_from_bytearray(barray)
# print([ "0x%02x" % b for b in ba.to_bytes()])
