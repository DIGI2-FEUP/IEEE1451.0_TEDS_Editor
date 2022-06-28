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

    def get_description(self):
        return "TEDS Identification Header"

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
    #GrpType = [20,1,"ControlGroup type uint8"]
    #MemList = [21,0,"ControlGroup member list array of uint16"]
    VGroup = [15, 0, "VectorGroup information sub-block"]
    #Types 20 and 21 define one VectorGroup.
    #GrpType = [20,1,"VectorGroup type uint8"]
    #MemList = [21,0,"VectorGroup member list array of uint16"]
    GeoLoc = [16, 0, "Specialized VectorGroup for geographic location"]
    #Types 24, 20, and 21 define one set of geographic location information.
    #LocEnum = [24,1,"An enumeration defining how location information is provided uint8"]
    #GrpType = [20,1,"VectorGroup type uint8"]
    #MemList = [21,0,"VectorGroup member list array of uint16"]
    Proxies = [17, 0, "TransducerChannel proxy definition sub-block"]
    #Types 22, 23, and 21 define one TransducerChannel proxy.
    #ChanNum = [22,1,"TransducerChannel number of the TransducerChannel proxy uint16"]
    #Organiz = [23,1,"TransducerChannel proxy data-set organization uint8"]
    #MemList = [21,0,"TransducerChannel proxy member list array of uint16"]
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
        #TEDS Identification Header uint8 4
        self.teds_id = TEDS_Identifier_Structure(TEDS_ACCESS_CODES.MetaTEDS)
        self.fields.append(self.teds_id)
        #Globally Unique Identifier UUID 10
        self.uuid_field = TEDS_Field(3, "TEDSID", "TEDS Identification Header", bytes(),  10)
        self.uuid_field.set_value(uuid.uuid4().bytes[:10])
        self.fields.append(self.uuid_field)
        #OholdOff Operational time-out float32 4
        self.oholdoff_field = TEDS_Field(10, "OholdOff", "Operational time-out", float32(), 4)
        self.oholdoff_field.set_value(0)
        self.fields.append(self.oholdoff_field)
        #SHoldOff Slow-access time-out float32 4
        self.sholdoff_field = TEDS_Field(11, "SholdOff", "Slow-access time-out", float32(), 4)
        self.sholdoff_field.set_value(0)
        self.fields.append(self.sholdoff_field)
        #TestTime Self-Test Time float32
        self.test_time_field = TEDS_Field(12, "TestTime", "Self-Test Time", float32(), 4)
        self.test_time_field.set_value(0)
        self.fields.append(self.test_time_field)
        #MaxChan Number of implemented TransducerChannels uint16 2
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
        #GrpType ControlGroup type uint8
        self.group_type = uint8(group_type)

class UNITS_TEDS_Data_Block():

    # As in Table 3—Physical Units interpretation
    class PHY_UNITS_INTR:
        PUI_SI_UNITS = 0
        PUI_RATIO_SI_UNITS = 1
        PUI_LOG10_SI_UNITS = 2
        PUI_LOG10_RATIO_SI_UNITS = 3
        PUI_DIGITAL_DATA = 4
        PUI_ARBITRARY = 5

    def __init__(self):
        self.fields = []
        self.UnitType = TEDS_Field(50,"UnitType","Physical Units interpretation enumeration",uint8,1)
        self.UnitType.set_value(0)
        self.fields.append(self.UnitType)
        self.Radians = TEDS_Field(51,"Radians","The exponent for Radians",uint8,1)
        self.Radians.set_value(0)
        self.fields.append(self.Radians)
        self.SterRad = TEDS_Field(52,"SterRad","The exponent for Steradians",uint8,1)
        self.SterRad.set_value(0)
        self.fields.append(self.SterRad)
        self.Meters = TEDS_Field(53,"Meters","The exponent for Meters",uint8,1)
        self.Meters.set_value(0)
        self.fields.append(self.Meters)
        self.Kilogram = TEDS_Field(54,"Kilogram","The exponent for Kilograms",uint8,1)
        self.Kilogram.set_value(0)
        self.fields.append(self.Kilogram)
        self.Seconds = TEDS_Field(55,"Seconds","The exponent for Seconds",uint8,1)
        self.Seconds.set_value(0)
        self.fields.append(self.Seconds)
        self.Amperes = TEDS_Field(56,"Amperes","The exponent for Amperes",uint8,1)
        self.Amperes.set_value(0)
        self.fields.append(self.Amperes)
        self.Kelvins = TEDS_Field(57,"Kelvins","The exponent for Kelvins",uint8,1)
        self.Kelvins.set_value(0)
        self.fields.append(self.Kelvins)
        self.Moles = TEDS_Field(58,"Moles","The exponent for Moles",uint8,1)
        self.Moles.set_value(0)
        self.fields.append(self.Moles)
        self.Candelas = TEDS_Field(59,"Candelas","The exponent for Candelas",uint8,1)
        self.Candelas.set_value(0)
        self.fields.append(self.Candelas)
        self.UnitsExt = TEDS_Field(60,"UnitsExt","TEDS access code for units extension",uint8,1)
        self.UnitsExt.set_value(0)
        self.fields.append(self.UnitsExt)
    
    def to_bytes(self):
        barray = bytearray(b'')
        for field in self.fields:
            try:
                barray.append(field.get_TLV().get_bytes())
            except:
                barray.extend(field.get_TLV().get_bytes())
        return barray

class TransducerChannel_TEDS_Data_Block():

    # As in Table 49—Enumeration of calibration keys
    class CALIBRATION_KEYS(enum.IntEnum):
        CAL_NONE = 0
        CAL_SUPPLIED = 1
        CAL_CUSTOM = 3
        TIM_CAL_SUPPLIED = 4
        TIM_CAL_SELF = 5
        TIM_CAL_CUSTOM = 6

    # As in Table 50—Enumeration of TransducerChannel types
    class TRANSDUCER_CHAN_TYPE(enum.IntEnum):
        SENSOR = 0
        ACTUATOR = 1
        EVENT_SENSOR = 3

    # As in Table 51—Enumeration of self-test keys
    class SELF_TEST_KEY(enum.IntEnum):
        NO_SELF_TEST = 0
        SELF_TEST_PROVIDED = 1

    # As in Table 52—Enumeration of data models
    class SELF_TEST_KEY(enum.IntEnum):
        NO_SELF_TEST = 0
        SELF_TEST_PROVIDED = 1

    def __init__(self):
        self.fields = []
        #TEDS Identification Header uint8 4
        self.teds_id = TEDS_Identifier_Structure(TEDS_ACCESS_CODES.ChanTEDS)
        self.fields.append(self.teds_id)

        # TransducerChannel related information
        self.CalKey = TEDS_Field(10,"CalKey","Calibration key",uint8,1)
        self.CalKey.set_value(0)
        self.fields.append(self.CalKey)
        self.ChanType = TEDS_Field(11,"ChanType","TransducerChannel type key",uint8,1)
        self.ChanType.set_value(0)
        self.fields.append(self.ChanType)
        self.PhyUnits = TEDS_Field(12,"PhyUnits","Physical Units",UNITS_TEDS_Data_Block,11)
        self.PhyUnits.set_value(0)
        self.fields.append(self.PhyUnits)
        self.LowLimit = TEDS_Field(13,"LowLimit","Design operational lower range limit",float32,4)
        self.LowLimit.set_value(0)
        self.fields.append(self.LowLimit)
        self.HiLimit = TEDS_Field(14,"HiLimit","Design operational upper range limit",float32,4)
        self.HiLimit.set_value(0)
        self.fields.append(self.HiLimit)
        self.OError = TEDS_Field(15,"OError","Worst-case uncertainty",float32,4)
        self.OError.set_value(0)
        self.fields.append(self.OError)
        self.SelfTest = TEDS_Field(16,"SelfTest","Self-test key",uint8,1)
        self.SelfTest.set_value(0)
        self.fields.append(self.SelfTest)
        self.MRange = TEDS_Field(17,"MRange","Multi-range capability",uint8,1)
        self.MRange.set_value(0)
        self.fields.append(self.MRange)
        # Data converter-related information — —
        #18 Sample — —
        self.DatModel = TEDS_Field(40,"DatModel","Data model",uint8,1)
        self.DatModel.set_value(0)
        self.fields.append(self.DatModel)
        self.ModLenth = TEDS_Field(41,"ModLenth","Data model length",uint8,1)
        self.ModLenth.set_value(0)
        self.fields.append(self.ModLenth)
        self.SigBits = TEDS_Field(42,"SigBits","Model significant bits",uint16,2)
        self.SigBits.set_value(0)
        self.fields.append(self.SigBits)
        #19 DataSet
        self.Repeats = TEDS_Field(43,"Repeats","Maximum data repetitions",uint16,2)
        self.Repeats.set_value(0)
        self.fields.append(self.Repeats)
        self.SOrigin = TEDS_Field(44,"SOrigin","Series origin",float32,4)
        self.SOrigin.set_value(0)
        self.fields.append(self.SOrigin)
        self.StepSize = TEDS_Field(45,"StepSize","Series increment",float32,4)
        self.StepSize.set_value(0)
        self.fields.append(self.StepSize)
        self.SUnits = TEDS_Field(46,"SUnits","Series units",UNITS_TEDS_Data_Block,11)
        self.SUnits.set_value(0)
        self.fields.append(self.SUnits)
        self.PreTrigg = TEDS_Field(47,"PreTrigg","Maximum pre-trigger samples",uint16,2)
        self.PreTrigg.set_value(0)
        self.fields.append(self.PreTrigg)
        # Timing-related information
        self.UpdateT = TEDS_Field(20,"UpdateT","TransducerChannel update time (tu)",float32,4)
        self.UpdateT.set_value(0)
        self.fields.append(self.UpdateT)
        self.WSetupT = TEDS_Field(21,"WSetupT","TransducerChannel write setup time (tws)",float32,4)
        self.WSetupT.set_value(0)
        self.fields.append(self.WSetupT)
        self.RSetupT = TEDS_Field(22,"RSetupT","TransducerChannel read setup time (trs)",float32,4)
        self.RSetupT.set_value(0)
        self.fields.append(self.RSetupT)
        self.SPeriod = TEDS_Field(23,"SPeriod","TransducerChannel sampling period (tsp)",float32,4)
        self.SPeriod.set_value(0)
        self.fields.append(self.SPeriod)
        self.WarmUpT = TEDS_Field(24,"WarmUpT","TransducerChannel warm-up time",float32,4)
        self.WarmUpT.set_value(0)
        self.fields.append(self.WarmUpT)
        self.RDelayT = TEDS_Field(25,"RDelayT","TransducerChannel read delay time (tch)",float32,4)
        self.RDelayT.set_value(0)
        self.fields.append(self.RDelayT)
        self.TestTime = TEDS_Field(26,"TestTime","TransducerChannel self-test time requirement",float32,4)
        self.TestTime.set_value(0)
        self.fields.append(self.TestTime)
        # Time of the sample information
        self.TimeSrc = TEDS_Field(27,"TimeSrc","Source for the time of sample",uint8,1)
        self.TimeSrc.set_value(0)
        self.fields.append(self.TimeSrc)
        self.InPropDl = TEDS_Field(28,"InPropDl","Incoming propagation delay through the data transport logic",float32,4)
        self.InPropDl.set_value(0)
        self.fields.append(self.InPropDl)
        self.OutPropD = TEDS_Field(29,"OutPropD","Outgoing propagation delay through the data transport logic",float32,4)
        self.OutPropD.set_value(0)
        self.fields.append(self.OutPropD)
        self.TSError = TEDS_Field(30,"TSError","Trigger-to-sample delay uncertainty",float32,4)
        self.TSError.set_value(0)
        self.fields.append(self.TSError)
        # Attributes
        #31 Sampling Sampling attribute — —
        self.SampMode = TEDS_Field(48,"SampMode","Sampling mode capability",uint8,1)
        self.SampMode.set_value(0)
        self.fields.append(self.SampMode)
        self.SDefault = TEDS_Field(49,"SDefault","Default sampling mode",uint8,1)
        self.SDefault.set_value(0)
        self.fields.append(self.SDefault)
        self.DataXmit = TEDS_Field(32,"DataXmit","Data transmission attribute",uint8,1)
        self.DataXmit.set_value(0)
        self.fields.append(self.DataXmit)
        self.Buffered = TEDS_Field(33,"Buffered","Buffered attribute",uint8,1)
        self.Buffered.set_value(0)
        self.fields.append(self.Buffered)
        self.EndOfSet = TEDS_Field(34,"EndOfSet","End-of-data-set operation attribute",uint8,1)
        self.EndOfSet.set_value(0)
        self.fields.append(self.EndOfSet)
        self.EdgeRpt = TEDS_Field(35,"EdgeRpt","Edge-to-report attribute",uint8,1)
        self.EdgeRpt.set_value(0)
        self.fields.append(self.EdgeRpt)
        self.ActHalt = TEDS_Field(36,"ActHalt","Actuator-halt attribute",uint8,1)
        self.ActHalt.set_value(0)
        self.fields.append(self.ActHalt)
        # Sensitivity
        self.Directon = TEDS_Field(37,"Directon","Sensitivity direction",float32,4)
        self.Directon.set_value(0)
        self.fields.append(self.Directon)
        self.DAngles = TEDS_Field(38,"DAngles","Direction angles Two",float32,8)
        self.DAngles.set_value(0)
        self.fields.append(self.DAngles)
        # Options
        self.ESOption = TEDS_Field(39,"ESOption","Event sensor options",uint8,1)
        self.ESOption.set_value(0)
        self.fields.append(self.ESOption)

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
