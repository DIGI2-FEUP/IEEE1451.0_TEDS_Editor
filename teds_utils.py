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

import uuid
from sys import getsizeof
import numpy as np
from numpy import float32, isin, uint16, int16, uint32, int32, uint8, int8, frombuffer

# Type 4, UUID, Globally Unique Identifier UUID, size 10
# TO-DO, implement as in the standard definition
def generate_uuid(north = None, west = None, year = None, date = None, sequence = None):
    return uuid.uuid4().bytes[:10]

def calc_length(data_block):
    return getsizeof(data_block, 0)

def calc_checksum(self):
    pass

# Utility functions to convert data
to_uint8 = lambda value : uint8(value)
to_int8 = lambda value : int8(value)
to_uint16 = lambda value : uint16(value)
to_int16 = lambda value : int16(value)
to_uint32 = lambda value : uint32(value)
to_int32 = lambda value : int32(value)
to_float32 = lambda value : float32(value)
list_to_uint8 = lambda flist : np.array(flist,dtype="uint8").tobytes()
list_to_int8 = lambda flist : np.array(flist,dtype="int8").tobytes()
list_to_uint16 = lambda flist : np.array(flist,dtype="uint16").tobytes()
list_to_int16 = lambda flist : np.array(flist,dtype="int16").tobytes()
list_to_uint32 = lambda flist : np.array(flist,dtype="uint32").tobytes()
list_to_int32 = lambda flist : np.array(flist,dtype="int32").tobytes()
list_to_float32 = lambda flist : np.array(flist,dtype="float32").tobytes()
# Infer what conversion function is most appropriate to a TEDS Field
def infer_conversion_function(teds_field):
    dtype_octets = 0
    scalar_conversion_function = None
    list_conversion_function = None

    if teds_field.data_type == uint8:
        dtype_octets = 1
        scalar_conversion_function = to_uint8
        list_conversion_function = list_to_uint8
    elif teds_field.data_type == int8:
        dtype_octets = 1
        scalar_conversion_function = to_int8
        list_conversion_function = list_to_int8
    elif teds_field.data_type == uint16:
        dtype_octets = 2
        scalar_conversion_function = to_uint16
        list_conversion_function = list_to_uint16
    elif teds_field.data_type == int16:
        dtype_octets = 2
        scalar_conversion_function = to_int16
        list_conversion_function = list_to_int16
    elif teds_field.data_type == uint32:
        dtype_octets = 4
        scalar_conversion_function = to_uint32
        list_conversion_function = list_to_uint32
    elif teds_field.data_type == int32:
        dtype_octets = 4
        scalar_conversion_function = to_int32
        list_conversion_function = list_to_int32
    elif teds_field.data_type == float32:
        dtype_octets = 4
        scalar_conversion_function = to_float32
        list_conversion_function = list_to_float32

    if dtype_octets < teds_field.get_value_length():
        # If the data type octets are less than the field value octets
        # Then assume the value is a list with N values
        # N = field_octets/dtype_octets (TO-DO)
        teds_field.value_to_data_type = list_conversion_function
    else:
        teds_field.value_to_data_type = scalar_conversion_function


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

    def to_bytes(self):
        barray = bytearray(b'')
        for field in self.fields:
            if field.optional and field.include == False:
                # If the teds field is optional, and not set for inclusion, skip it
                continue
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
        for field in self.fields:
            # print("Loading array section: {} - {}".format(seek,seek + field.get_total_length()))
            # print("Section size: {}".format(len(bytearr[seek:seek + field.get_total_length()])))
            # print(bytearr[seek:seek + field.get_total_length()])
            field.load_bytes(bytearr[seek:seek + field.get_total_length()])
            seek += field.get_total_length()

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
        self.value_to_data_type = None

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

    def set_conversion_function(self, function):
        self.value_to_data_type = function

    def is_optional(self):
        self.optional = True

    # Use the provided function to convert the value o the correct teds field data type
    # If the function fails, try to cast it
    # If given value has the correct type, do not apply conversion
    def set_value(self, value):
        # print(type(value))
        # print([self.data_type, bytes, bytearray])
        if type(value) not in [self.data_type, bytes, bytearray]:
            try:
                # If a conversion function is not known, try to define it
                if self.value_to_data_type is None:
                    infer_conversion_function(self)
                # Use the generic conversion function
                self.value = self.value_to_data_type(value)
            except:
                # In last resort, try to cast the value
                self.value = type(self.data_type)(value)
        else:
            self.value = value

    def get_value(self):
        return self.value

    def get_TLV(self):
        self.tlv = TEDS_TLV_Block(self)
        return self.tlv

    def get_bytes(self):
        return self.get_TLV().get_bytes()

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
            print("TEDS Field: {}, loaded bytes don't match.".format(self.name))
            #raise ValueError("TEDS Field: {}, loaded bytes don't match.".format(self.name))

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
        barr.append(self.type)
        # If it is another TEDS data block, use specific approach
        if isinstance(self.teds_field.get_value(), TEDS_Data_Block):
            # Get the data block bytes
            subarray = self.teds_field.get_value().to_bytes()
            # This field size is the number of octets in the block + 2
            self.length = uint8(len(subarray))
            barr.append(self.length)
            try:
                barr.extend(subarray)
            except:
                barr.append(subarray)
        else:
            try:
                barr.extend(self.length)
            except:
                barr.append(self.length)
            try:
                if isinstance(self.teds_field.get_value(), type(np.array)):
                    barr.extend(self.teds_field.get_value().to_bytes())
                else:
                    barr.extend(self.teds_field.get_value())
            except:                    
                barr.append(self.teds_field.get_value())
            if len(barr) != self.length + TL_OCTETS:
                raise ValueError("TEDS field type: {}, expected encoding length is: {}, should be: {}"
                    .format(self.type, len(barr)-TL_OCTETS, self.length))
        return barr