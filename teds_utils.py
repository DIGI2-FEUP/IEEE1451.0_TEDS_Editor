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

from ctypes import sizeof
from dataclasses import fields
from operator import length_hint
import uuid
from sys import getsizeof, stdout
import numpy as np
from numpy import float32, uint16, int16, uint32, int32, uint8, int8, frombuffer
from struct import unpack, pack
from json import loads

# Type 4, UUID, Globally Unique Identifier UUID, size 10
# TO-DO, implement as in the standard definition
def generate_uuid(north = None, west = None, year = None, date = None, sequence = None):
    return uuid.uuid4().bytes[:10]

def calc_length(data_block):
    return getsizeof(data_block, 0)
def calc_checksum(byte_array):
    
    sum=0
    for byte in byte_array:
        sum += byte
    
    return 0xFFFF - (sum%0xFFFF)

# Utility functions to convert data
# Functions to convert a string to simple type
string_to_uint8 = lambda value : uint8(value)
string_to_int8 = lambda value : int8(value)
string_to_uint16 = lambda value : uint16(value)
string_to_int16 = lambda value : int16(value)
string_to_uint32 = lambda value : uint32(value)
string_to_int32 = lambda value : int32(value)
string_to_float32 = lambda value : float32(value)
# Functions to convert a literal string list to list of type
string_list_to_uint8 = lambda flist : np.array(loads(flist),dtype="uint8")[0]
string_list_to_int8 = lambda flist : np.array(loads(flist),dtype="int8")[0]
string_list_to_uint16 = lambda flist : np.array(loads(flist),dtype="uint16")[0]
string_list_to_int16 = lambda flist : np.array(loads(flist),dtype="int16")[0]
string_list_to_uint32 = lambda flist : np.array(loads(flist),dtype="uint32")[0]
string_list_to_int32 = lambda flist : np.array(loads(flist),dtype="int32")[0]
string_list_to_float32 = lambda flist : np.array(loads(flist),dtype="float")[0]
# Functions to convert bytes to simple type
bytes_to_uint8 = lambda value : unpack('>B', value)[0]
bytes_to_int8 = lambda value : unpack('>b', value)[0]
bytes_to_uint16 = lambda value : unpack('>H', value)[0]
bytes_to_int16 = lambda value : unpack('>h', value)[0]
bytes_to_uint32 = lambda value : unpack('>I', value)[0]
bytes_to_int32 = lambda value : unpack('>i', value)[0]
bytes_to_float32 = lambda value : unpack('>f', value)[0]
# Functions to convert simple type to bytes
uint8_to_bytes = lambda value : bytearray(pack(">B", value))
int8_to_bytes = lambda value : bytearray(pack(">b", value))
uint16_to_bytes = lambda value : bytearray(pack(">H", value))
int16_to_bytes = lambda value : bytearray(pack(">h", value))
uint32_to_bytes = lambda value : bytearray(pack(">I", value)) 
int32_to_bytes = lambda value : bytearray(pack(">i", value)) 
float32_to_bytes = lambda value : bytearray(pack(">f", value)) 
# Functions to convert list of types to list of bytes
list_of_uint8_to_bytes = lambda flist : b''.join([pack(">B",x) for x in flist])
list_of_int8_to_bytes = lambda flist : b''.join([pack(">b",x) for x in flist])
list_of_uint16_to_bytes = lambda flist : b''.join([pack(">H",x) for x in flist])
list_of_int16_to_bytes = lambda flist : b''.join([pack(">h",x) for x in flist])
list_of_uint32_to_bytes = lambda flist : b''.join([pack(">I",x) for x in flist])
list_of_int32_to_bytes = lambda flist : b''.join([pack(">i",x) for x in flist])
list_of_float32_to_bytes = lambda flist : b''.join([pack(">f",x) for x in flist])
# Functions to convert bytes to list of type
byte_list_to_uint8 = lambda flist : [unpack('>B',flist[x:x+1])[0] for x in range(0,len(flist))]
byte_list_to_int8 = lambda flist : [unpack('>b',flist[x:x+1])[0] for x in range(0,len(flist))]
byte_list_to_uint16 = lambda flist : [unpack('>H',flist[x:x+2])[0] for x in range(0,len(flist),2)]
byte_list_to_int16 = lambda flist : [unpack('>h',flist[x:x+2])[0] for x in range(0,len(flist),2)]
byte_list_to_uint32 = lambda flist : [unpack('>I',flist[x:x+4])[0] for x in range(0,len(flist),4)]
byte_list_to_int32 = lambda flist : [unpack('>i',flist[x:x+4])[0] for x in range(0,len(flist),4)]
byte_list_to_float32 = lambda flist : [unpack('>f',flist[x:x+4])[0] for x in range(0,len(flist),4)]

# Infer what conversion function is most appropriate to a TEDS Field
def infer_conversion_functions(teds_field):

    if teds_field.data_type == uint8:
        # Keep this attribute to help in data conversions
        teds_field.dtype_octets = 1
        # If the data type octets are less than the field value octets
        # Then assume the value is a list with N values
        # N = field_octets/dtype_octets
        if teds_field.dtype_octets < teds_field.get_value_length():
            teds_field.value_from_bytes = byte_list_to_uint8
            teds_field.value_from_string = string_list_to_uint8
            teds_field.value_as_bytes = list_of_uint8_to_bytes
        else:
            teds_field.value_from_bytes = bytes_to_uint8
            teds_field.value_from_string = string_to_uint8
            teds_field.value_as_bytes = uint8_to_bytes
    elif teds_field.data_type == int8:
        teds_field.dtype_octets = 1
        if teds_field.dtype_octets < teds_field.get_value_length():
            teds_field.value_from_bytes = byte_list_to_int8
            teds_field.value_from_string = string_list_to_int8
            teds_field.value_as_bytes = list_of_int8_to_bytes
        else:
            teds_field.value_from_bytes = bytes_to_int8
            teds_field.value_from_string = string_to_int8
            teds_field.value_as_bytes = int8_to_bytes
    elif teds_field.data_type == uint16:
        teds_field.dtype_octets = 2
        if teds_field.dtype_octets < teds_field.get_value_length():
            teds_field.value_from_bytes = byte_list_to_uint16
            teds_field.value_from_string = string_list_to_uint16
            teds_field.value_as_bytes = list_of_uint16_to_bytes
        else:
            teds_field.value_from_bytes = bytes_to_uint16
            teds_field.value_from_string = string_to_uint16
            teds_field.value_as_bytes = uint16_to_bytes
    elif teds_field.data_type == int16:
        teds_field.dtype_octets = 2
        if teds_field.dtype_octets < teds_field.get_value_length():
            teds_field.value_from_bytes = byte_list_to_int16
            teds_field.value_from_string = string_list_to_int16
            teds_field.value_as_bytes = list_of_int16_to_bytes
        else:
            teds_field.value_from_bytes = bytes_to_int16
            teds_field.value_from_string = string_to_int16
            teds_field.value_as_bytes = int16_to_bytes
    elif teds_field.data_type == uint32:
        teds_field.dtype_octets = 4
        if teds_field.dtype_octets < teds_field.get_value_length():
            teds_field.value_from_bytes = byte_list_to_uint32
            teds_field.value_from_string = string_list_to_uint32
            teds_field.value_as_bytes = list_of_uint32_to_bytes
        else:
            teds_field.value_from_bytes = bytes_to_uint32
            teds_field.value_from_string = string_to_uint32
            teds_field.value_as_bytes = uint32_to_bytes
    elif teds_field.data_type == int32:
        teds_field.dtype_octets = 4
        if teds_field.dtype_octets < teds_field.get_value_length():
            teds_field.value_from_bytes = byte_list_to_int32
            teds_field.value_from_string = string_list_to_int32
            teds_field.value_as_bytes = list_of_int32_to_bytes
        else:
            teds_field.value_from_bytes = bytes_to_int32
            teds_field.value_from_string = string_to_int32
            teds_field.value_as_bytes = int32_to_bytes
    elif teds_field.data_type == float32:
        teds_field.dtype_octets = 4
        if teds_field.dtype_octets < teds_field.get_value_length():
            teds_field.value_from_bytes = byte_list_to_float32
            teds_field.value_from_string = string_list_to_float32
            teds_field.value_as_bytes = list_of_float32_to_bytes
        else:
            teds_field.value_from_bytes = bytes_to_float32
            teds_field.value_from_string = string_to_float32
            teds_field.value_as_bytes = float32_to_bytes

# Number of octets in Type, Length of a TEDS TLV field
TL_OCTETS = 2

# Utility classes

class TEDS_Block:

    def __init__(self, teds_data_block):
        self.teds_data_block = teds_data_block
        self.length = calc_length(self.value)
        self.checksum = calc_checksum(self.teds_data_block)

# Utility class that holds functions and attributes common to all TEDS data blocks
class TEDS_Data_Block():

    def __init__(self):
        # List to hold references to all teds fields
        self.fields = []

    def to_bytes_with_length_and_checksum(self):
        barray = self.to_bytes()
        barray = uint32_to_bytes((len(barray)+2)) + barray
        checksum = calc_checksum(barray)
        barray = barray + uint16_to_bytes(uint16(checksum))
        return barray


    def to_bytes(self):
        barray = bytearray(b'')
        for field in self.fields:
            if field.optional and field.include == False:
                # If the teds field is optional, and not set for inclusion, skip it
                continue
            try:
                print("Writing bytes from field: {}, value: {}".format(field.name, field.get_value()))
                print("Value as bytes: ")
                stdout.write(field.get_value_as_bytes().hex('-'))
                print("")
                stdout.flush()
            except:
                pass
            try:
                barray.append(field.get_TLV().get_bytes())
            except:
                barray.extend(field.get_TLV().get_bytes())
        return barray

    # This method will only load a TEDS with the fields defined in the constructor
    # A Meta TEDS will all fields will fail to load
    def load_from_bytearray(self, bytearr):
        # bytearr must be 'bytearray object
        assert isinstance(bytearr, bytearray)

        # Current position in bytearray
        seek = 0
        while seek < len(bytearr):
            field_type = uint8(bytearr[seek])
            seek += 1
            field_length = uint8(bytearr[seek])
            seek +=1
            field_value = bytearr[seek:seek+field_length]
            seek += field_length
            print("Loading field type: {}, length: {}, value: ".format(field_type, field_length), end='')
            stdout.write(field_value.hex('-'))
            print("")
            stdout.flush()
            self.set_field(TEDS_TLV_Block(field_type, field_length, field_value))

    def set_field(self, tlv_block):
        for field in self.fields:
            if field.type == tlv_block.field_type:
                field.load_bytes_from_TLV(tlv_block)
                field.include = True
                break

class TEDS_Field():

    def __init__(self, type, name, description, data_type, n_octets):
        self.type = uint8(type)
        self.name = name
        self.description = description
        self.data_type = data_type
        self.length = uint8(n_octets)
        self.value = None
        self.tlv = None
        self.enum = None
        self.optional = False
        self.include = False
        self.value_from_bytes = None
        self.value_from_string = None
        self.value_as_bytes = None
        infer_conversion_functions(self)

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

    def set_value_enum(self,enum):
        # If the value is based in an enumeration, keep a reference
        self.enum = enum

    def is_optional(self):
        self.optional = True

    def set_value_from_bytes(self, barray):
        self.value = self.value_from_bytes(barray)

    def set_value_from_string(self, str_value):
        self.value = self.value_from_string(str_value)

    def get_value_as_string(self):
        return str(self.value)

    def get_value_as_bytes(self):
        #print("Field {} name {}, as bytes".format(self.type, self.name))
        return self.value_as_bytes(self.value)

    # Use the provided function to convert the value o the correct teds field data type
    # If the function fails, try to cast it
    # If given value has the correct type, do not apply conversion
    def set_value(self, value):
        # print(type(value))
        # print([self.data_type, bytes, bytearray])
        try:
            if isinstance(self.value, TEDS_Data_Block):
                # This should never happen, return
                return
            else:
                self.value = value
        except:
            # In last resort, try to cast the value
            self.value = type(self.data_type)(value)

    def get_value(self):
        return self.value

    def get_TLV(self):
        if isinstance(self.value, TEDS_Data_Block):
            barray = self.value.to_bytes()
            self.tlv = TEDS_TLV_Block(self.type, len(barray), barray)
        else:
            self.tlv = TEDS_TLV_Block(self.type, self.length, self.get_value_as_bytes())
        return self.tlv

    def get_bytes(self):
        return self.get_TLV().get_bytes()

    def load_bytes_from_TLV(self, tlv_block):
        try:
            # Assert this is the correct field
            assert tlv_block.field_type == self.type
            # Assert the TLV value is a bytearray
            assert isinstance(tlv_block.field_value, bytearray)
            # Assert the bytearray has the length anounced
            assert tlv_block.field_length == len(tlv_block.field_value)
            # If this field type is a TEDS Data Block
            if isinstance(self.value, TEDS_Data_Block):
                self.value.load_from_bytearray(tlv_block.field_value)
            else:
                self.set_value_from_bytes(tlv_block.field_value)
        except:
            # print("TEDS Field: {}, loaded bytes don't match.".format(self.name))
            raise ValueError("TEDS Field: {}, loaded bytes don't match.".format(self.name))

# All TEDS prepared by a transducer manufacturer use a Type/Length/Value (TLV) data structure.
# The “Type“ field is a 1 octet tag that identifies the TLV, similar in function to HTML or XML tags. 
# The “Length” field specifies the number of octets of the value field.
# The “Value” field is the actual data.
class TEDS_TLV_Block():

    def __init__(self, field_type, field_length, field_value):
        self.field_type = field_type
        self.field_length = field_length
        self.field_value = field_value

    #TO-DO correct this method
    def get_bytes(self):
        barr = bytearray(b'')
        barr.append(self.field_type)
        # If it is another TEDS data block, use specific approach
        if isinstance(self.field_value, TEDS_Data_Block):
            # Get the data block bytes
            subarray = self.field_value.to_bytes()
            # This field size is the number of octets in the block + 2
            self.field_length = uint8(len(subarray))
            barr.append(self.field_length)
            try:
                barr.extend(subarray)
            except:
                barr.append(subarray)
        else:
            barr.append(self.field_length)
            try:
                barr.extend(self.field_value)
            except:                    
                barr.append(self.field_value)
            if len(barr) != self.field_length + TL_OCTETS:
                raise ValueError("TEDS field type: {}, value encoding length is: {}, should be: {}"
                    .format(self.field_type, len(barr)-TL_OCTETS, self.field_length))
        return barr