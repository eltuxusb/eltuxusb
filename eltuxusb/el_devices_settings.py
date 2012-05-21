# -*- coding: utf-8 -*-
# Here we set the diffrent values for the different devices

import usb.core
import usb.util

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
                "elusb4_1": 256,
                "elusb4_2": 256,
                "elusblite": 256,
                "elusbco": 256,
                "elusbtc": 256,
                "elusbco300": 256,
                "elusb2lcd": 256,
                "elusb2plus": 256}

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
                "13": "elusb2plus"}

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
                "elusb2plus": "EL-USB-2+"}

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
                "elusb2plus": 64}

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
                "elusb2plus": "not defined yet"}

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
    def __init__(self):
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

    def get_original_buffer(self):
        return self.actual_buffer

    def get_modified_buffer(self):
        self.get_new_buffer()
        return self.new_buffer

    # End of public functions
    ######

    def setup(self):
        #print ""
        #print self.actual_buffer
        #print ""

        # The first 32 bytes are the same for every devices
        self.device_model = self.actual_buffer[0]
        self.cmd_type = self.actual_buffer[1]
        self.name = [self.actual_buffer[2], self.actual_buffer[3], self.actual_buffer[4], self.actual_buffer[5], self.actual_buffer[6], self.actual_buffer[7], self.actual_buffer[8], self.actual_buffer[9], self.actual_buffer[10], self.actual_buffer[11], self.actual_buffer[12], self.actual_buffer[13], self.actual_buffer[14], self.actual_buffer[15], self.actual_buffer[16], self.actual_buffer[17]]
        self.hour = self.actual_buffer[18]
        self.minutes = self.actual_buffer[19]
        self.seconds = self.actual_buffer[20]
        self.day = self.actual_buffer[21]
        self.month = self.actual_buffer[22]
        self.year = self.actual_buffer[23]
        self.start_offset = [self.actual_buffer[24], self.actual_buffer[25], self.actual_buffer[26], self.actual_buffer[27]]
        self.sample_rate = [self.actual_buffer[28], self.actual_buffer[29]]
        self.sample_count = [self.actual_buffer[30], self.actual_buffer[31]]
        self.flag_bits = [self.actual_buffer[32], self.actual_buffer[33]]
        self.sn = [self.actual_buffer[52], self.actual_buffer[53], self.actual_buffer[54], self.actual_buffer[55]]
        self.calib_m = [self.actual_buffer[36], self.actual_buffer[37], self.actual_buffer[38], self.actual_buffer[39]]
        self.calib_c = [self.actual_buffer[40], self.actual_buffer[41], self.actual_buffer[42], self.actual_buffer[43]]
        self.version = [self.actual_buffer[48], self.actual_buffer[49],self.actual_buffer[50], self.actual_buffer[51]]

        if self.model == "elusb1_16" or self.model == "elusb1_17" or self.model == "elusb2" or self.model == "elusb2lcd" or self.model == "elusb2plus":

            self.hal = self.actual_buffer[34]
            self.lal = self.actual_buffer[35]
            self.factory_use = [self.actual_buffer[44], self.actual_buffer[45]]
            self.unit = self.actual_buffer[46]
            self.flag_bits2 = self.actual_buffer[47]
            self.hal_ch2 = self.actual_buffer[56]
            self.lal_ch2 = self.actual_buffer[57]
            self.roll_count = self.actual_buffer[58]
            self.res1 = self.actual_buffer[59]
            self.res2 = self.actual_buffer[60]


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
        self.new_buffer += self.start_offset
        self.new_buffer += self.sample_rate
        self.new_buffer += self.sample_count
        self.new_buffer += self.flag_bits

        if self.model == "elusb1_16" or self.model == "elusb1_17" or self.model == "elusb2" or self.model == "elusb2lcd" or self.model == "elusb2plus":

            self.new_buffer.append(self.hal)
            self.new_buffer.append(self.lal)
            self.new_buffer += self.calib_m
            self.new_buffer += self.calib_c
            self.new_buffer += self.factory_use
            self.new_buffer.append(self.unit)
            self.new_buffer.append(self.flag_bits2)
            self.new_buffer += self.version
            self.new_buffer += self.sn
            self.new_buffer.append(self.hal_ch2)
            self.new_buffer.append(self.lal_ch2)
            self.new_buffer.append(self.roll_count)
            self.new_buffer.append(self.res1)
            self.new_buffer.append(self.res2)

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
