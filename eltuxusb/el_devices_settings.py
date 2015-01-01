# -*- coding: utf-8 -*-
# Here we set the different values for the different devices

class el_settings:
    "Here we return the settings of the different devices"
    def __init__(self):

        self.model = "elusb1_17"

        # Return the size (in bytes) of the configuration buffer
        self.config_message_size = {
                "elusb1_16": 64,
                "elusb1_17": 64,
                "elusb2": 128,
                "elusb3_1": 256,
                "elusb3_2": 256,
                "elusb3_256": 2,
                "elusb4_1": 256,
                "elusb4_2": 256,
                "elusblite": 256,
                "elusbco": 256,
                "elusbtc": 256,
                "elusbco300": 256,
                "elusb2lcd": 128,
                "elusb2plus": 256,
                "elusb1pro": 256}

        # Return the device model from the first byte of the config message (1 -> D)
        self.device_model = {
                "1": "elusb1_16",
                "2": "elusb1_17",
                "3": "elusb2",
                "4": "elusb3_1",
                "5": "elusb4_1",
                "6": "elusb3_2",
                "7": "elusb4_2",
                "8": "elusblite",
                "9": "elusbco",
                "10": "elusbtc",
                "11": "elusbco300",
                "12": "elusb2lcd",
                "13": "elusb2plus",
                "14": "elusb1pro"}

        # Return the full name (commercial) of the device
        self.device_full_name = {
                "elusb1_16": "EL-USB-1 Temperature Logger (v.64b)",
                "elusb1_17": "EL-USB-1 Temperature Logger (v.512b)",
                "elusb2": "EL-USB-2 Humidity and Temperature Logger",
                "elusb3_1": "EL-USB-3 Voltage Logger",
                "elusb4_1": "EL-USB-4 Current Logger",
                "elusb3_2": "EL-USB-3 Voltage Logger",
                "elusb4_2": "EL-USB-4 Current Logger",
                "elusblite": "EL-USB-LITE Temperature Logger",
                "elusbco": "EL-USB-CO Carbon Monoxide Logger",
                "elusbtc": "EL-USB-TC Thermocouple Temperature Logger",
                "elusbco300": "EL-USB-CO300 Low Range Carbon Monoxide Logger",
                "elusb2lcd": "EL-USB-2-LCD",
                "elusb2plus": "EL-USB-2+",
                "elusb1pro": "EL-USB-1-PRO"}

        # Define the number of packets we should read from the device when downloading the recordings
        self.device_nb_packets = {
                "elusb1_16": 256,
                "elusb1_17": 32,
                "elusb2": 64,
                "elusb3_1": 127,
                "elusb4_1": 127,
                "elusb3_2": 127,
                "elusb4_2": 127,
                "elusblite": 10,
                "elusbco": 127,
                "elusbtc": 127,
                "elusbco300": 127,
                "elusb2lcd": 64,
                "elusb2plus": 64,
                "elusb1pro": 127}

        # Define which conversion diagram should be used for the recorded datas (some devices use the same conversion diagram)
        self.data_conversion_diagram = {
                "elusb1_16": "elusb1_convert",
                "elusb1_17": "elusb1_convert",
                "elusb2": "elusb2_convert",
                "elusb3_1": "not defined yet",
                "elusb4_1": "not defined yet",
                "elusb3_2": "not defined yet",
                "elusb4_2": "not defined yet",
                "elusblite": "not defined yet",
                "elusbco": "not defined yet",
                "elusbtc": "not defined yet",
                "elusbco300": "not defined yet",
                "elusb2lcd": "elusb2_convert",
                "elusb2plus": "not defined yet",
                "elusb1pro": "elusb1_convert"}

    ######
    # Public functions

    def get_config_message_size(self, model):
        return self.config_message_size.get(model)

    def get_device_model(self, value):
        return self.device_model.get(value)

    def get_device_full_name(self, value):
        return self.device_full_name.get(value)

    def get_device_nb_packets(self, value):
        return self.device_nb_packets.get(value)

    def get_data_conversion_diagram(self, value):
        return self.data_conversion_diagram.get(value)

    # End of public functions
    ######

    # Return the device model from the config message
    #def config_message(self, ):
    #       #hexadecimal values, sent in little endian mode
    #       self.config_message = {
    #               "024000": ("elusb1_16", "elusb1_17"),
    #               "021280": ("elusb2", "elusb2lcd", "elusb2plus"),
    #               "022560": ("elusb3_1", "elusb3_2", "elusb4_1", "elusb4_2", "elusblite", "elusbco", "elusbtc", "elusbco300")}
    #       return self.config_message.get(model)

class el_buffer:
    "Here we define the buffer config for the diffrent devices"
    def __init__(self, debug):
        self.debug = debug
        self.model = ""
        self.name = ""
        self.hour = ""
        self.flag_bits = ""
        self.actual_buffer = []
        self.conig_size = ""
        self.new_buffer = "not yet set"

    ######
    # Public functions

    def set_model(self, model):
        self.model = model
        self.config_size = el_settings().get_config_message_size(self.model)
        self.setup()

    def set_buffer(self, actual_buffer):
        self.actual_buffer = actual_buffer

    def set_cmd_type(self, cmd_type_value):
        self.cmd_type = cmd_type_value

    def set_name(self, name_value):
        self.name = name_value

    def set_hour(self, hour_value):
        self.hour = hour_value

    def set_minutes(self, minutes_value):
        self.minutes = minutes_value

    def set_seconds(self, seconds_value):
        self.seconds = seconds_value

    def set_day(self, day_value):
        self.day = day_value

    def set_month(self, month_value):
        self.month = month_value

    def set_year(self, year_value):
        self.year = year_value

    def set_start_offset(self, start_offset_value):
        self.start_offset = start_offset_value

    def set_sample_rate(self, sample_rate_value):
        self.sample_rate = sample_rate_value

    def set_hal_ch2(self, hal_ch2_value):
        self.hal_ch2 = hal_ch2_value

    def set_lal_ch2(self, lal_ch2_value):
        self.lal_ch2 = lal_ch2_value

    def set_hal(self, hal_value):
        self.hal = hal_value

    def set_lal(self, lal_value):
        self.lal = lal_value

    def set_unit(self, unit_value):
        self.unit = unit_value

    def set_flag_bits(self, flag_bits_value):
        self.flag_bits = flag_bits_value

    def set_start_hour(self, start_hour_value):
        self.hour = start_hour_value

    def set_sample_count(self, sample_count_value):
        self.sample_count = sample_count_value

    def set_sn(self, sn):
        self.sn = sn

    def get_calib_m(self):
        return self.calib_m

    def get_calib_c(self):
        return self.calib_c

    def get_display_unit_text(self):
        return self.display_unit_text

    def get_calibration_input1_text(self):
        return self.calibration_input1_text

    def get_calibration_output1_text(self):
        return self.calibration_output1_text

    def get_calibration_input2_text(self):
        return self.calibration_input2_text

    def get_calibration_output2_text(self):
        return self.calibration_output2_text

    def get_scaling_factor(self):
        return self.scaling_factor

    def get_high_alarm_level_text(self):
        return self.high_alarm_level_text

    def get_low_alarm_level_text(self):
        return self.low_alarm_level_text

    def get_original_buffer(self):
        return self.actual_buffer

    def get_modified_buffer(self):
        self.get_new_buffer()
        return self.new_buffer

    # End of public functions
    ######

    def setup(self):
        
        from el_device import el1_math
        self.math = el1_math()

        # The first 32 bytes are the same for every devices
        self.device_model = self.actual_buffer[0]
        self.cmd_type = self.actual_buffer[1]
        self.name = self.actual_buffer[2:18]
        self.hour = self.actual_buffer[18]
        self.minutes = self.actual_buffer[19]
        self.seconds = self.actual_buffer[20]
        self.day = self.actual_buffer[21]
        self.month = self.actual_buffer[22]
        self.year = self.actual_buffer[23]
        self.start_offset = self.actual_buffer[24:28]
        self.sample_rate = self.actual_buffer[28:30]
        self.sample_count = self.actual_buffer[30:32]
        self.flag_bits = self.actual_buffer[32:34]
        self.sn = self.actual_buffer[52:56]
        self.calib_m = self.actual_buffer[36:40]
        self.calib_c = self.actual_buffer[40:44]
        self.version = self.actual_buffer[48:52]

        if self.model == "elusb1_16" or self.model == "elusb1_17" or self.model == "elusb2" or self.model == "elusb2lcd" or self.model == "elusb2plus" or self.model == "elusb3_2" or self.model == "elusb1pro":

            if self.model == "elusb3_2":
                self.hal = self.actual_buffer[34:36]
                self.lal = self.actual_buffer[56:58]

            else:
                self.hal = self.actual_buffer[34]
                self.lal = self.actual_buffer[35]
                self.hal_ch2 = self.actual_buffer[56]
                self.lal_ch2 = self.actual_buffer[57]

            self.factory_use = self.actual_buffer[44:46]
            self.unit = self.actual_buffer[46]
            self.flag_bits2 = self.actual_buffer[47]
            self.roll_count = self.actual_buffer[58]
            self.res1 = self.actual_buffer[59]
            self.maximum_samples = self.actual_buffer[60:62]
            self.res2 = self.actual_buffer[62:64]

            # CONVERTED BASE VALUE (CNV)
            self.cnv_sn = self.math.sn_convert(self.sn)
            self.cnv_calib_m = self.math.base256to10(self.calib_m)
            self.cnv_calib_c = self.math.base256to10(self.calib_c)

        if self.model == "elusb3_2":
            # RAW VALUES
            self.display_unit_text = self.actual_buffer[64:76]
            self.calibration_input1_text = self.actual_buffer[76:84]
            self.calibration_output1_text = self.actual_buffer[84:92]
            self.calibration_input2_text = self.actual_buffer[92:100]                        
            self.calibration_output2_text = self.actual_buffer[100:108]
            self.scaling_factor = self.actual_buffer[108:112]
            self.high_alarm_level_text = self.actual_buffer[112:120]
            self.low_alarm_level_text = self.actual_buffer[120:128]
            self.default_range_description_text = self.actual_buffer[128:142]
            self.default_input_unit_text = self.actual_buffer[142:154]
            self.default_display_unit = self.actual_buffer[154:166]
            self.default_calibration_input1_text = self.actual_buffer[166:174]
            self.default_calibration_output1_text = self.actual_buffer[174:182]
            self.default_calibration_input2_text = self.actual_buffer[182:190]
            self.default_calibration_output2_text = self.actual_buffer[190:198]
            self.default_high_alarm_level_text = self.actual_buffer[198:206]
            self.default_low_alarm_level_text = self.actual_buffer[206:214]

            # CONVERTED VALUE (CNV)
            self.cnv_display_unit_text = self.math.name_translate(self.display_unit_text)
            self.cnv_calibration_input1_text = self.math.name_translate(self.calibration_input1_text)
            self.cnv_calibration_output1_text = self.math.name_translate(self.calibration_output1_text)
            self.cnv_calibration_input2_text = self.math.name_translate(self.calibration_input2_text)
            self.cnv_calibration_output2_text = self.math.name_translate(self.calibration_output2_text)
            self.cnv_scaling_factor = self.math.base256to10(self.scaling_factor)
            self.cnv_high_alarm_level_text = self.math.name_translate(self.high_alarm_level_text)
            self.cnv_low_alarm_level_text = self.math.name_translate(self.low_alarm_level_text)
            self.cnv_default_range_description_text = self.math.name_translate(self.default_range_description_text)
            self.cnv_default_input_unit_text = self.math.name_translate(self.default_input_unit_text)
            self.cnv_default_display_unit = self.math.name_translate(self.default_display_unit)
            self.cnv_default_calibration_input1_text = self.math.name_translate(self.default_calibration_input1_text)
            self.cnv_default_calibration_output1_text = self.math.name_translate(self.default_calibration_output1_text)
            self.cnv_default_calibration_input2_text = self.math.name_translate(self.default_calibration_input2_text)
            self.cnv_default_calibration_output2_text = self.math.name_translate(self.default_calibration_output2_text)
            self.cnv_default_high_alarm_level_text = self.math.name_translate(self.default_high_alarm_level_text)
            self.cnv_default_low_alarm_level_text = self.math.name_translate(self.default_low_alarm_level_text)

        if self.debug:
            print "\n#DEBUG# ###################"
            print "#DEBUG# RAW DEVICE SETTINGS"
            print "#DEBUG# DEVICE MODEL: %s" % self.device_model
            print "#DEBUG# COMMAND TYPE: %s" % self.cmd_type
            print "#DEBUG# RECORD NAME : %s" % self.name
            print "#DEBUG# START HOUR  : %s" % self.hour
            print "#DEBUG# START MINUTE: %s" % self.minutes
            print "#DEBUG# START SECOND: %s" % self.seconds
            print "#DEBUG# CALIB M VALUE: %s" % self.calib_m
            print "#DEBUG# CALIB C VALUE: %s" % self.calib_c
            print "#DEBUG# SERIAL NUMBER: %s" % self.sn

            self.sn = self.actual_buffer[52:56]

            if self.model == "elusb3_2":
                print "#DEBUG# DISPLAY UNIT TEXT: %s" % self.display_unit_text
                print "#DEBUG# CALIBRATION INPUT1 TEXT: %s" % self.calibration_input1_text
                print "#DEBUG# CALIBRATION OUTPUT1 TEXT: %s" % self.calibration_output1_text
                print "#DEBUG# CALIBRATION INPUT2 TEXT: %s" % self.calibration_input2_text
                print "#DEBUG# CALIBRATION OUTPUT2 TEXT: %s" % self.calibration_output2_text
                print "#DEBUG# SCALING FACTOR: %s" % self.scaling_factor
                print "#DEBUG# HIGH ALARM LEVEL TEXT: %s" % self.high_alarm_level_text
                print "#DEBUG# LOW ALARM LEVEL TEXT: %s" % self.low_alarm_level_text
                print "#DEBUG# DEFAULT RANGE DECRIPTION TEXT: %s" % self.default_range_description_text
                print "#DEBUG# DEFAULT INPUT UNIT TEXT: %s" % self.default_input_unit_text
                print "#DEBUG# DEFAULT DISPLAY UNIT: %s" % self.default_display_unit
                print "#DEBUG# DEFAULT CALIBRATION INPUT1 TEXT: %s" % self.default_calibration_input1_text
                print "#DEBUG# DEFAULT CALIBRATION OUTPUT1 TEXT: %s" % self.default_calibration_output1_text
                print "#DEBUG# DEFAULT CALIBRATION INPUT2 TEXT: %s" % self.default_calibration_input2_text
                print "#DEBUG# DEFAULT CALIBRATION OUTPUT2 TEXT: %s" % self.default_calibration_output2_text
                print "#DEBUG# DEFAULT HIGH ALARM LEVEL TEXT: %s" % self.default_high_alarm_level_text
                print "#DEBUG# DEFAULT LOW ALARM LEVEL TEXT: %s" % self.default_low_alarm_level_text
 
            print "\n#DEBUG# ###################"
            print "#DEBUG# CONVERTED DEVICE SETTINGS"
            print "#DEBUG# SERIAL NUMBER: %s" % self.cnv_sn
            print "#DEBUG# CALIBRATION M VALUE: %s" % self.cnv_calib_m
            print "#DEBUG# CALIBRATION C VALUE: %s" % self.cnv_calib_c

            if self.model == "elusb3_2":
                print "#DEBUG# DISPLAY UNIT TEXT: %s" % self.cnv_display_unit_text
                print "#DEBUG# CALIBRATION INPUT1 TEXT: %s" % self.cnv_calibration_input1_text
                print "#DEBUG# CALIBRATION OUTPUT1 TEXT: %s" % self.cnv_calibration_output1_text     
                print "#DEBUG# CALIBRATION INPUT2 TEXT: %s" % self.cnv_calibration_input2_text
                print "#DEBUG# CALIBRATION OUTPUT2 TEXT: %s" % self.cnv_calibration_output2_text
                print "#DEBUG# SCALING FACTOR: %f" % self.cnv_scaling_factor
                print "#DEBUG# HIGH ALARM LEVEL TEXT: %s" % self.cnv_high_alarm_level_text
                print "#DEBUG# LOW ALARM LEVEL TEXT: %s" % self.cnv_low_alarm_level_text
                print "#DEBUG# DEFAULT RANGE DESCRIPTION TEXT: %s" % self.cnv_default_range_description_text
                print "#DEBUG# DEFAULT INPUT UNIT TEXT: %s" % self.cnv_default_input_unit_text
                print "#DEBUG# DEFAULT DISPLAY UNIT: %s" % self.cnv_default_display_unit
                print "#DEBUG# DEFAULT CALIBRATION INPUT1 TEXT: %s" % self.cnv_default_calibration_input1_text
                print "#DEBUG# DEFAULT CALIBRATION OUTPUT1 TEXT: %s" % self.cnv_default_calibration_output1_text
                print "#DEBUG# DEFAULT CALIBRATION INPUT2 TEXT: %s" % self.cnv_default_calibration_input2_text
                print "#DEBUG# DEFAULT CALIBRATION OUTPUT2 TEXT: %s" % self.cnv_default_calibration_output2_text
                print "#DEBUG# DEFAULT HIGH ALARM LEVEL TEXT: %s" % self.cnv_default_high_alarm_level_text
                print "#DEBUG# DEFAULT LOW ALARM LEVEL TEXT: %s" % self.cnv_default_low_alarm_level_text



    def get_new_buffer(self):
    
        self.new_buffer = []
        self.new_buffer.append(self.device_model)
        self.new_buffer.append(self.cmd_type)
        self.new_buffer += self.name
        self.new_buffer.append(self.hour)
        self.new_buffer.append(self.minutes)
        self.new_buffer.append(self.seconds)
        self.new_buffer.append(self.day)
        self.new_buffer.append(self.month)
        self.new_buffer.append(self.year)

        self.new_buffer = self.new_buffer + self.start_offset \
                                          + self.sample_rate \
                                          + self.sample_count \
                                          + self.flag_bits

        if self.model == "elusb1_16" or self.model == "elusb1_17" or self.model == "elusb2" or self.model == "elusb2lcd" or self.model == "elusb2plus" or self.model == "elusb3_2" or self.model == "elusb1pro":


            if self.model == "elusb3_2":
                self.new_buffer += self.hal

            else:
                self.new_buffer.append(self.hal)
                self.new_buffer.append(self.lal)

            self.new_buffer += self.calib_m
            self.new_buffer += self.calib_c
            self.new_buffer += self.factory_use
            self.new_buffer.append(self.unit)
            self.new_buffer.append(self.flag_bits2)
            self.new_buffer += self.version
            self.new_buffer += self.sn

            if self.model == "elusb3_2":            
                self.new_buffer += self.lal
        
            else:
                self.new_buffer.append(self.hal_ch2)
                self.new_buffer.append(self.lal_ch2)

            self.new_buffer.append(self.roll_count)
            self.new_buffer.append(self.res1)
            self.new_buffer += self.maximum_samples
            self.new_buffer += self.res2

            if self.model == "elusb3_2":            
                #PUT EL3_2 RELATED SETTINGS HERE
                self.new_buffer = self.new_buffer + self.display_unit_text \
                                                  + self.calibration_input1_text \
                                                  + self.calibration_output1_text \
                                                  + self.calibration_input2_text \
                                                  + self.calibration_output2_text \
                                                  + self.scaling_factor \
                                                  + self.high_alarm_level_text \
                                                  + self.low_alarm_level_text \
                                                  + self.default_range_description_text \
                                                  + self.default_input_unit_text \
                                                  + self.default_display_unit \
                                                  + self.default_calibration_input1_text \
                                                  + self.default_calibration_output1_text \
                                                  + self.default_calibration_input2_text \
                                                  + self.default_calibration_output2_text \
                                                  + self.default_high_alarm_level_text \
                                                  + self.default_low_alarm_level_text 


            while len(self.new_buffer) != self.config_size:
                self.new_buffer.append(0)
            return self.new_buffer

    # We check that the sensitive data's hasn't been corrupted (serial number, calibration values, model, ...)
    def verify_buffer(self):

        old_type = self.actual_buffer[0]
        old_calibration_m_value = self.actual_buffer[36:40]
        old_calibration_c_value = self.actual_buffer[40:44]
        old_serial_number = self.actual_buffer[52:56]
        old_version = self.actual_buffer[48:52]

        new_type = self.new_buffer[0]
        new_calibration_m_value = self.new_buffer[36:40]
        new_calibration_c_value = self.new_buffer[40:44]
        new_serial_number = self.new_buffer[52:56]
        new_version = self.new_buffer[48:52]

        if old_type != new_type or old_calibration_m_value != new_calibration_m_value or old_calibration_c_value != new_calibration_c_value or old_serial_number != new_serial_number or old_version != new_version:
            return False
        else:
            return True
