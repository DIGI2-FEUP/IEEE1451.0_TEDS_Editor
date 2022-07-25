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

import enum
import enum
from numpy import uint32, uint64, uint8, uint16, float32, frombuffer
from pandas import array
from teds_utils import TEDS_Data_Block, TEDS_Field, TEDS_TLV_Block, TL_OCTETS, generate_uuid

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
        self.name = "Header"
        self.enum = None
        self.optional = False

    def get_type(self):
        return self.type

    def get_description(self):
        return "TEDS Identification Header"

    def get_TLV(self):
        return TEDS_TLV_Block(self.type, self.length, self.get_bytes())

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
        if isinstance(barray, TEDS_TLV_Block):
            self.load_bytes_from_TLV(barray)
        else:
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

    def load_bytes_from_TLV(self, tlv_block):
        try:
            assert tlv_block.field_type == self.type
            assert tlv_block.field_length == self.length
            barray = tlv_block.field_value
            assert barray[0] == self.family
            assert barray[1] == self.teds_class
            assert barray[2] == self.version
            assert barray[3] == self.tuple_length
        except:
            raise ValueError("TEDS Identifier Structure, loaded bytes don't match.")

# This class and GUI are not complete
# Only the types defined in the constructor can be used
# TO-DO: Implement all types from META_TEDS_TYPES
class Meta_TEDS_Data_Block(TEDS_Data_Block):

    # This block holds the Meta TEDS fields defined in Table 43 — Structure of the Meta-TEDS data block
    def __init__(self):
        super().__init__()
        #TEDS Identification Header uint8 4
        self.teds_id = TEDS_Identifier_Structure(TEDS_ACCESS_CODES.MetaTEDS)
        self.fields.append(self.teds_id)
        #Globally Unique Identifier UUID 10
        self.uuid_field = TEDS_Field(4, "TEDSID", "Globally Unique Identifier", uint8,  10)
        self.uuid_field.set_value_from_bytes(generate_uuid())
        self.fields.append(self.uuid_field)

        #self.uuid_field_2 = TEDS_Field(4, "TEDSID", "Globally Unique Identifier", UUID_TEDS_Data_Block,  10)
        #self.uuid_field_2.set_value(UUID_TEDS_Data_Block())
        #self.fields.append(self.uuid_field_2)
        #OholdOff Operational time-out float32 4
        self.oholdoff_field = TEDS_Field(10, "OholdOff", "Operational time-out", float32, 4)
        self.oholdoff_field.set_value(0.0)
        self.fields.append(self.oholdoff_field)
        #SHoldOff Slow-access time-out float32 4
        self.sholdoff_field = TEDS_Field(11, "SholdOff", "Slow-access time-out", float32, 4)
        self.sholdoff_field.set_value(0.0)
        self.sholdoff_field.is_optional()
        self.fields.append(self.sholdoff_field)
        #TestTime Self-Test Time float32
        self.test_time_field = TEDS_Field(12, "TestTime", "Self-Test Time", float32, 4)
        self.test_time_field.set_value(0.0)
        self.fields.append(self.test_time_field)
        #MaxChan Number of implemented TransducerChannels uint16 2
        self.max_chan_field = TEDS_Field(13, "MaxChan", "Number of implemented TransducerChannels", uint16, 2)
        self.max_chan_field.set_value(0)
        self.fields.append(self.max_chan_field)

    def set_uuid(self, uuid):
        self.uuid_field_2.set_value(uuid)

'''class UUID_TEDS_Data_Block(TEDS_Data_Block):
    def __init__(self):
        super().__init__()
        self.UUID = TEDS_Field(4,"UUID","Unique Universal Identifier",uint8,10)
        self.UUID.set_value([])
        self.fields.append(self.UUID)
        self.UUID.include = True
        self.North = TEDS_Field(0,"North","North(1)/South(0)",uint8,1)
        self.North.set_value(0)
        self.North.include = False
        self.fields.append(self.North)
        self.Latitude = TEDS_Field(0,"Latitude", "Latitude in arcdegrees",uint32,4)
        self.Latitude.set_value(0)
        self.Latitude.include = False
        self.fields.append(self.Latitude)
        self.East = TEDS_Field(0,"East","East(1)/West(0)",uint8,1)
        self.East.set_value(0)
        self.East.include = False
        self.fields.append(self.East)
        self.Longitude = TEDS_Field(0,"Longitude", "Longitude in arcdegrees",uint32,4)
        self.Longitude.set_value(0)
        self.Longitude.include = False
        self.fields.append(self.Longitude)
        self.Manufacturer = TEDS_Field(0,"Manufacturer", "Manufacturer",uint8,1)
        self.Manufacturer.include = False
        self.Manufacturer.set_value(0)
        self.fields.append(self.Manufacturer)
        self.Year = TEDS_Field(0,"Year", "Year",uint16,2)
        self.Year.set_value(0)
        self.Year.include = False
        self.fields.append(self.Year)
        self.DateSequence = TEDS_Field(0,"Date/Sequence", "Date/Sequence",uint32,4)
        self.DateSequence.set_value(0)
        self.DateSequence.include = False
        self.fields.append(self.DateSequence)
       
    def set_value(self,uuid):
        self.UUID.set_value(uuid)
    
    def calcUUID(self):
        value = 0
        value = value| (self.North.get_value() & 0x1)
        value = value | (self.Latitude.get_value() & 0xFFFFF) << 1 
        value = value | (self.East.get_value() & 0x1) << 21
        value = value | (self.Longitude.get_value() & 0x3FFFFF) << 22
        value = value | (self.Manufacturer.get_value() & 0xF) << 42
        value = value | (self.Year.get_value() & 0xFFF) << 46
        value = value | (self.DateSequence.get_value() & 0x3F) << 58
        
        self.UUID.set_value(uint64(value).tobytes().)

    def update(self):
        self.calcUUID()

    def to_bytes(self):
        barray = bytearray(b'')
        try:
            barray.append(self.UUID.get_TLV().get_bytes())
        except:
            barray.extend(self.UUID.get_TLV().get_bytes())
        return barray


'''
class UNITS_TEDS_Data_Block(TEDS_Data_Block):

    # As in Table 3—Physical Units interpretation
    class PHY_UNITS_INTR(enum.IntEnum):
        PUI_SI_UNITS = 0
        PUI_RATIO_SI_UNITS = 1
        PUI_LOG10_SI_UNITS = 2
        PUI_LOG10_RATIO_SI_UNITS = 3
        PUI_DIGITAL_DATA = 4
        PUI_ARBITRARY = 5

    def __init__(self):
        super().__init__()
        self.UnitType = TEDS_Field(50,"UnitType","Physical Units interpretation enumeration",uint8,1)
        self.UnitType.set_value(self.PHY_UNITS_INTR.PUI_SI_UNITS)
        self.UnitType.set_value_enum(self.PHY_UNITS_INTR)
        self.fields.append(self.UnitType)
        self.Radians = TEDS_Field(51,"Radians","The exponent for Radians",uint8,1)
        self.Radians.set_value(128)
        self.Radians.is_optional()
        self.fields.append(self.Radians)
        self.SterRad = TEDS_Field(52,"SterRad","The exponent for Steradians",uint8,1)
        self.SterRad.set_value(128)
        self.SterRad.is_optional()
        self.fields.append(self.SterRad)
        self.Meters = TEDS_Field(53,"Meters","The exponent for Meters",uint8,1)
        self.Meters.set_value(128)
        self.Meters.is_optional()
        self.fields.append(self.Meters)
        self.Kilogram = TEDS_Field(54,"Kilogram","The exponent for Kilograms",uint8,1)
        self.Kilogram.set_value(128)
        self.Kilogram.is_optional()
        self.fields.append(self.Kilogram)
        self.Seconds = TEDS_Field(55,"Seconds","The exponent for Seconds",uint8,1)
        self.Seconds.set_value(128)
        self.Seconds.is_optional()
        self.fields.append(self.Seconds)
        self.Amperes = TEDS_Field(56,"Amperes","The exponent for Amperes",uint8,1)
        self.Amperes.set_value(128)
        self.Amperes.is_optional()
        self.fields.append(self.Amperes)
        self.Kelvins = TEDS_Field(57,"Kelvins","The exponent for Kelvins",uint8,1)
        self.Kelvins.set_value(128)
        self.Kelvins.is_optional()
        self.fields.append(self.Kelvins)
        self.Moles = TEDS_Field(58,"Moles","The exponent for Moles",uint8,1)
        self.Moles.set_value(128)
        self.Moles.is_optional()
        self.fields.append(self.Moles)
        self.Candelas = TEDS_Field(59,"Candelas","The exponent for Candelas",uint8,1)
        self.Candelas.set_value(128)
        self.Candelas.is_optional()
        self.fields.append(self.Candelas)
        self.UnitsExt = TEDS_Field(60,"UnitsExt","TEDS access code for units extension",uint8,1)
        self.UnitsExt.set_value(0)
        self.UnitsExt.is_optional()
        self.fields.append(self.UnitsExt)

class SAMPLE_TEDS_Data_Block(TEDS_Data_Block):

    # As in Table 52—Enumeration of data models
    class DATA_MODELS(enum.IntEnum):
        N_OCTET_INTEGER = 0
        SINGLE_PRECISION_REAL = 1
        DOUBLE_PRECISION_REAL = 2
        N_OCTET_FRACTION = 3
        BIT_SEQUENCE = 4
        LONG_INTEGER = 5
        LONG_FRACTION = 6
        TIME_INSTANCE = 7

    def __init__(self):
        super().__init__()
        self.DatModel = TEDS_Field(40,"DatModel","Data model",uint8,1)
        self.DatModel.set_value_enum(self.DATA_MODELS)
        self.DatModel.set_value(self.DATA_MODELS.BIT_SEQUENCE)
        self.fields.append(self.DatModel)
        self.ModLenth = TEDS_Field(41,"ModLenth","Data model length",uint8,1)
        self.ModLenth.set_value(0)
        self.fields.append(self.ModLenth)
        self.SigBits = TEDS_Field(42,"SigBits","Model significant bits",uint16,2)
        self.SigBits.set_value(0)
        self.fields.append(self.SigBits)

class DATASET_TEDS_Data_Block(TEDS_Data_Block):

    def __init__(self):
        super().__init__()
        self.Repeats = TEDS_Field(43,"Repeats","Maximum data repetitions",uint16,2)
        self.Repeats.set_value(0)
        self.fields.append(self.Repeats)
        self.SOrigin = TEDS_Field(44,"SOrigin","Series origin",float32,4)
        self.SOrigin.set_value(0.0)
        self.fields.append(self.SOrigin)
        self.StepSize = TEDS_Field(45,"StepSize","Series increment",float32,4)
        self.StepSize.set_value(0.0)
        self.fields.append(self.StepSize)
        self.SUnits = TEDS_Field(46,"SUnits","Series units",UNITS_TEDS_Data_Block,11)
        self.SUnits.set_value(UNITS_TEDS_Data_Block())
        self.fields.append(self.SUnits)
        self.PreTrigg = TEDS_Field(47,"PreTrigg","Maximum pre-trigger samples",uint16,2)
        self.PreTrigg.set_value(0)
        self.fields.append(self.PreTrigg)

class SAMPLING_TEDS_Data_Block(TEDS_Data_Block):

    # As in Table 54—Sampling mode capability attribute
    # TO-DO: Each sampling mode represents a bit from lsb to msb
    # For this to be correct all combinations must be available
    class SAMPLING_MODE_CAPABILITY(enum.IntEnum):
        TRIGGER_INITIATED = 1
        FREE_RUNNING = 2
        FREE_RUN_PRE_TRIGGER = 4
        CONTINUOUS_SAMPLING = 8
        IMMEDIATE_SAMPLING = 16
        ALL_MODES = 31
    
    # As in Table 55—Default sampling mode attribute
    class DEFAULT_SAMPLING_MODE(enum.IntEnum):
        TRIGGER_INITIATED = 1
        FREE_RUNNING = 2
        FREE_RUN_PRE_TRIGGER = 4
        CONTINUOUS_SAMPLING = 8
        IMMEDIATE_OPERATION = 16

    def __init__(self):
        super().__init__()
        self.SampMode = TEDS_Field(48,"SampMode","Sampling mode capability",uint8,1)
        self.SampMode.set_value_enum(self.SAMPLING_MODE_CAPABILITY)
        self.SampMode.set_value(self.SAMPLING_MODE_CAPABILITY.ALL_MODES)
        self.fields.append(self.SampMode)
        self.SDefault = TEDS_Field(49,"SDefault","Default sampling mode",uint8,1)
        self.SDefault.set_value_enum(self.DEFAULT_SAMPLING_MODE)
        self.SDefault.set_value(self.DEFAULT_SAMPLING_MODE.IMMEDIATE_OPERATION)
        self.fields.append(self.SDefault)

class TransducerChannel_TEDS_Data_Block(TEDS_Data_Block):

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

    # As in Table 53—Enumeration of sample time sources
    class SAMPLE_TIME_SOURCES(enum.IntEnum):
        NO_HELP = 0
        INCOMING = 1
        OUTGOING = 2
        MINTERVAL = 3
        SINTERVAL = 4
        TODSENSE = 5
        
    # As in Table 56—Buffered attribute
    class BUFFERED_ATTRIBUTE(enum.IntEnum):
        NO_MORE_THAN_ONE_BUFFER = 0
        MULTIPLE_BUFFER_ONLY_BUFFER_MODE = 1
        MULTIPLE_BUFFER_DEFAULT_UNBUFFERED_MODE = 2
        MULTIPLE_BUFFER_DEFAULT_BUFFERED_MODE = 3

    # As in Table 57—End-of-data-set operation attribute
    class END_OF_DATA_SET_ATTRIBUTE(enum.IntEnum):
        NOT_APPLICABLE = 0
        HOLD = 1
        RECIRCULATE = 2
        DEFAULT_HOLD_OR_RECIRCULATE = 3
        DEFAULT_RECIRCULATE_OR_HOLD = 4

    # As in Table 58—Data transmission attribute
    class DATA_TRANSMISSION_ATTRIBUTE(enum.IntEnum):
        ONLY_WHEN_COMMANDED = 0
        BUFFER_FULL_OR_COMMANDED = 1
        FIXED_INTERVAL_OR_COMMANDED = 2
        ALL_MODES = 3

    # As in Table 59—Edge-to-report options
    class EDGE_TO_REPORT(enum.IntEnum):
        NOT_APPLICABLE = 0
        RISING_EDGE = 1
        FALLING_EDGE = 2
        BOTH_EDGES = 3
        BOTH_EDGES_DEFAULT_RISING = 5
        BOTH_EDGES_DEFAULT_FALLING = 6
        BOTH_EDGES_DEFAULT_BOTH = 7

    # As in Table 61—Sensitivity direction enumeration
    class SENSITIVITY_DIRECTION(enum.IntEnum):
        NOT_APPLICABLE = 0
        PLUS_X = 1
        MINUS_X = 2
        PLUS_Y = 3
        MINUS_Y = 4
        PLUS_Z = 5
        MINUS_Z = 6

    # As in Table 60—Actuator-halt operations
    class ACTUATOR_HALT_OPERATIONS(enum.IntEnum):
        NOT_APPLICABLE = 0
        HALT_IMMEDIATE = 1
        HALT_END_DATA_SET = 2
        RAMP_TO_PREDEFINED_STATE = 3

    # As in Table 62—Event sensor options
    class EVENT_SENSOR_OPTIONS(enum.IntEnum):
        NOT_APPLICABLE = 0
        NOT_CHANGEABLE = 1
        CHANGEABLE_INCONSISTENCIES_DETECTED = 2
        CHANGEABLE_INCONSISTENCIES_NOT_DETECTED = 3

    def __init__(self):
        super().__init__()
        #TEDS Identification Header uint8 4
        self.teds_id = TEDS_Identifier_Structure(TEDS_ACCESS_CODES.ChanTEDS)
        self.fields.append(self.teds_id)

        # TransducerChannel related information
        self.CalKey = TEDS_Field(10,"CalKey","Calibration key",uint8,1)
        self.CalKey.set_value_enum(self.CALIBRATION_KEYS)
        self.CalKey.set_value(self.CALIBRATION_KEYS.CAL_NONE)
        self.fields.append(self.CalKey)
        self.ChanType = TEDS_Field(11,"ChanType","TransducerChannel type key",uint8,1)
        self.ChanType.set_value_enum(self.TRANSDUCER_CHAN_TYPE)
        self.ChanType.set_value(self.TRANSDUCER_CHAN_TYPE.SENSOR)
        self.fields.append(self.ChanType)
        self.PhyUnits = TEDS_Field(12,"PhyUnits","Physical Units",UNITS_TEDS_Data_Block,11)
        self.PhyUnits.set_value(UNITS_TEDS_Data_Block())
        self.fields.append(self.PhyUnits)
        self.LowLimit = TEDS_Field(13,"LowLimit","Design operational lower range limit",float32,4)
        self.LowLimit.set_value(0.0)
        self.fields.append(self.LowLimit)
        self.HiLimit = TEDS_Field(14,"HiLimit","Design operational upper range limit",float32,4)
        self.HiLimit.set_value(0.0)
        self.fields.append(self.HiLimit)
        self.OError = TEDS_Field(15,"OError","Worst-case uncertainty",float32,4)
        self.OError.set_value(0.0)
        self.fields.append(self.OError)
        self.SelfTest = TEDS_Field(16,"SelfTest","Self-test key",uint8,1)
        self.SelfTest.set_value_enum(self.SELF_TEST_KEY)
        self.SelfTest.set_value(self.SELF_TEST_KEY.NO_SELF_TEST)
        self.fields.append(self.SelfTest)
        self.MRange = TEDS_Field(17,"MRange","Multi-range capability",uint8,1)
        self.MRange.set_value(0)
        self.MRange.is_optional()
        self.fields.append(self.MRange)
        # Data converter-related information — —
        self.Sample = TEDS_Field(18,"Sample","Sample definition",DATASET_TEDS_Data_Block,10)
        self.Sample.set_value(DATASET_TEDS_Data_Block())
        self.fields.append(self.Sample)
        self.DataSet = TEDS_Field(19,"DataSet","DataSet information structure",DATASET_TEDS_Data_Block,55)
        self.DataSet.set_value(DATASET_TEDS_Data_Block())
        self.fields.append(self.DataSet)
        # Timing-related information
        self.UpdateT = TEDS_Field(20,"UpdateT","TransducerChannel update time (tu)",float32,4)
        self.UpdateT.set_value(0.0)
        self.fields.append(self.UpdateT)
        self.WSetupT = TEDS_Field(21,"WSetupT","TransducerChannel write setup time (tws)",float32,4)
        self.WSetupT.set_value(0.0)
        self.fields.append(self.WSetupT)
        self.RSetupT = TEDS_Field(22,"RSetupT","TransducerChannel read setup time (trs)",float32,4)
        self.RSetupT.set_value(0.0)
        self.fields.append(self.RSetupT)
        self.SPeriod = TEDS_Field(23,"SPeriod","TransducerChannel sampling period (tsp)",float32,4)
        self.SPeriod.set_value(0.0)
        self.fields.append(self.SPeriod)
        self.WarmUpT = TEDS_Field(24,"WarmUpT","TransducerChannel warm-up time",float32,4)
        self.WarmUpT.set_value(0.0)
        self.fields.append(self.WarmUpT)
        self.RDelayT = TEDS_Field(25,"RDelayT","TransducerChannel read delay time (tch)",float32,4)
        self.RDelayT.set_value(0.0)
        self.fields.append(self.RDelayT)
        self.TestTime = TEDS_Field(26,"TestTime","TransducerChannel self-test time requirement",float32,4)
        self.TestTime.set_value(0.0)
        self.fields.append(self.TestTime)
        # Time of the sample information
        self.TimeSrc = TEDS_Field(27,"TimeSrc","Source for the time of sample",uint8,1)
        self.TimeSrc.set_value_enum(self.SAMPLE_TIME_SOURCES)
        self.TimeSrc.set_value(self.SAMPLE_TIME_SOURCES.NO_HELP)
        self.TimeSrc.is_optional()
        self.fields.append(self.TimeSrc)
        self.InPropDl = TEDS_Field(28,"InPropDl","Incoming propagation delay through the data transport logic",float32,4)
        self.InPropDl.set_value(0.0)
        # In fact is not, if the previous field is set to "incoming"
        # TO-DO check how to solve these dependencies
        self.InPropDl.is_optional()
        self.fields.append(self.InPropDl)
        self.OutPropD = TEDS_Field(29,"OutPropD","Outgoing propagation delay through the data transport logic",float32,4)
        self.OutPropD.set_value(0.0)
        # May be required
        self.OutPropD.is_optional()
        self.fields.append(self.OutPropD)
        self.TSError = TEDS_Field(30,"TSError","Trigger-to-sample delay uncertainty",float32,4)
        self.TSError.set_value(0.0)
        self.fields.append(self.TSError)
        # Attributes
        self.Sampling = TEDS_Field(31,"Sampling","Sampling attribute",SAMPLING_TEDS_Data_Block,6)
        self.Sampling.set_value(SAMPLING_TEDS_Data_Block())
        self.fields.append(self.Sampling)
        self.DataXmit = TEDS_Field(32,"DataXmit","Data transmission attribute",uint8,1)
        self.DataXmit.set_value_enum(self.DATA_TRANSMISSION_ATTRIBUTE)
        self.DataXmit.set_value(self.DATA_TRANSMISSION_ATTRIBUTE.ONLY_WHEN_COMMANDED)
        self.fields.append(self.DataXmit)
        self.Buffered = TEDS_Field(33,"Buffered","Buffered attribute",uint8,1)
        self.Buffered.set_value_enum(self.BUFFERED_ATTRIBUTE)
        self.Buffered.set_value(self.BUFFERED_ATTRIBUTE.NO_MORE_THAN_ONE_BUFFER)
        self.Buffered.is_optional()
        self.fields.append(self.Buffered)
        self.EndOfSet = TEDS_Field(34,"EndOfSet","End-of-data-set operation attribute",uint8,1)
        self.EndOfSet.set_value_enum(self.END_OF_DATA_SET_ATTRIBUTE)
        self.EndOfSet.set_value(self.END_OF_DATA_SET_ATTRIBUTE.NOT_APPLICABLE)
        # May not be
        self.EndOfSet.is_optional()
        self.fields.append(self.EndOfSet)
        self.EdgeRpt = TEDS_Field(35,"EdgeRpt","Edge-to-report attribute",uint8,1)
        self.EdgeRpt.set_value_enum(self.EDGE_TO_REPORT)
        self.EdgeRpt.set_value(self.EDGE_TO_REPORT.NOT_APPLICABLE)
        self.EdgeRpt.is_optional()
        self.fields.append(self.EdgeRpt)
        self.ActHalt = TEDS_Field(36,"ActHalt","Actuator-halt attribute",uint8,1)
        self.ActHalt.set_value_enum(self.ACTUATOR_HALT_OPERATIONS)
        self.ActHalt.set_value(self.ACTUATOR_HALT_OPERATIONS.NOT_APPLICABLE)
        self.ActHalt.is_optional()
        self.fields.append(self.ActHalt)
        # Sensitivity
        self.Directon = TEDS_Field(37,"Directon","Sensitivity direction",uint8,1)
        self.Directon.set_value_enum(self.SENSITIVITY_DIRECTION)
        self.Directon.set_value(self.SENSITIVITY_DIRECTION.NOT_APPLICABLE)
        self.Directon.is_optional()
        self.fields.append(self.Directon)
        self.DAngles = TEDS_Field(38,"DAngles","Direction angles Two",float32,8)
        self.DAngles.set_value([0.0,0.0])
        self.DAngles.is_optional()
        self.fields.append(self.DAngles)
        # Options
        self.ESOption = TEDS_Field(39,"ESOption","Event sensor options",uint8,1)
        self.ESOption.set_value_enum(self.EVENT_SENSOR_OPTIONS)
        self.ESOption.set_value(self.EVENT_SENSOR_OPTIONS.NOT_APPLICABLE)
        self.ESOption.is_optional()
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

# ba = TransducerChannel_TEDS_Data_Block()
# print([ "0x%02x" % b for b in ba.to_bytes()])

#PhyUnits = TEDS_Field(12,"PhyUnits","Physical Units",UNITS_TEDS_Data_Block,11)
#PhyUnits.set_value(UNITS_TEDS_Data_Block())
#print([ "0x%02x" % b for b in PhyUnits.get_bytes()])
# [ lst[x:x+4] for x in range(0,len(lst),4)]