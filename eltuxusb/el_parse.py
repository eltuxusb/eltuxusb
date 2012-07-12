# -*- coding: utf-8 -*-
# Here we convert the recorded data to human reading characters


import datetime
import math
from el_device import *

class el1_parse:
    "This class contains everything for converting the recorded data into a file with human reading characters, the format of the files are the same as the ELWINUSB software"
    def __init__(self):
        self.translated_data = ""
        self.file_header = ""
        self.serial = ""
        self.file_dest = ""
        self.raw_data = []
        self.high_alarm_status = 0
        self.low_alarm_status = 0
        self.high_hum_alarm_status = 0
        self.low_hum_alarm_status = 0
        self.dest_file = ""
        self.unit = 0
        self.first_rec_time = 0
        self.intervale_rec = 0
        self.name = ""
        self.text_celsius = ",Celsius(°C)"
        self.text_fahrenheit = ",Fahrenheit(°F)"
        self.text_high_alarm = ",High Alarm"
        self.text_low_alarm = ",Low Alarm"
        self.text_high_hum_alarm = ",High Alarm rh"
        self.text_low_hum_alarm = ",Low Alarm rh"
        self.text_serial_number = ",Serial Number"
        self.text_humidity = ",Humidity(%rh)"
        self.text_dew_point_c = ",dew point(°C)"
        self.text_dew_point_f = ",dew point(°F)"
        self.text_time = ",Time"


    # Extract the name of the recording from the config buffer
    def name_translate(self, raw_config):
        self.name = ""

        self.name_byte = raw_config

        for i in self.name_byte:

            if i == 0:
                break
            else:
                self.name += (chr(i))
        return self.name

    # This formula calculate the Dew point with temperature and relative humidity
    def dew_point(self, temperature, relative_humidity):
        T = temperature
        RH = relative_humidity
        LogEW = (0.66077+(7.5*T/ (237.3+T))+(math.log10(RH)-2))
        Dp = ((0.66077-LogEW)*237.3) / (LogEW-8.16077)
        return round(Dp, 1)

    # Extract the temperature in Celsius or Fahrenheit from the config buffer
    def temp_convert(self, raw_temp):

        if self.unit == 0:
            temperature = float(raw_temp - 80) / 2
            return temperature
        else:
            temperature = float(raw_temp - 40)
            return temperature

    # Extract the high alarm value in Celsius or Fahrenheit from the config buffer
    def high_alarm_convert(self, raw_high_alarm):

        if self.unit == 0:
            high_alarm_value = float(raw_high_alarm - 80) / 2
            return high_alarm_value

        else:
            high_alarm_value = float(raw_high_alarm - 40)
            return high_alarm_value

    # Extract the low alarm value in Celsius or Fahrenheit from the config buffer
    def low_alarm_convert(self, raw_low_alarm):

        if self.unit == 0:
            low_alarm_value = float(raw_low_alarm - 80) / 2
            return low_alarm_value
        else:
            low_alarm_value = float(raw_low_alarm - 40)
            return low_alarm_value

    # Extract the humidity alarm value from the config buffer
    def humidity_alarm_convert(self, raw_humidity_alarm):

        humidity_alarm_value = float(raw_humidity_alarm) / 2

        return humidity_alarm_value

    # Convert the recorded data from the ELUSB2 device to the "standard" output format (same as the ELWINUSB software)
    def elusb2_convert(self):

        self.file_dest = open(self.dest_file, 'w')
        self.file_header += self.name + ",Time"
        separator = ","

        if self.unit == 0:
            self.file_header += self.text_celsius
        else:
            self.file_header += self.text_fahrenheit

        if self.high_alarm_status == "1":
            self.file_header += self.text_high_alarm

        if self.low_alarm_status == "1":
            self.file_header += self.text_low_alarm

        self.file_header += self.text_humidity

        if self.high_hum_alarm_status == "1":
            self.file_header += self.text_high_hum_alarm

        if self.low_hum_alarm_status == "1":
            self.file_header += self.text_low_hum_alarm


        if self.unit == 0:
            self.file_header += self.text_dew_point_c
        else:
            self.file_header += self.text_dew_point_f

        self.file_header += self.text_serial_number
        self.file_dest.write(self.file_header+"\n")

        line_position = 1
        value = self.raw_data[0]
        raw_data_number = 1
        count = 0

        while value != 255:
            date = str(self.first_rec_time.strftime("%d/%m/%Y %H:%M:%S"))
            if count == 0:
                pair = [value]
                count = 1

            else:
                pair.append(value)
                count = 0
                converted_temp = self.temp_convert(pair[0])
                converted_hum = float(pair[1]) / 2
                dew_point = self.dew_point(converted_temp, converted_hum)
                converted_high_alarm = self.high_alarm_convert(self.raw_high_alarm)
                converted_low_alarm = self.low_alarm_convert(self.raw_low_alarm)
                converted_high_hum_alarm = self.humidity_alarm_convert(self.raw_high_hum_alarm)
                converted_low_hum_alarm = self.humidity_alarm_convert(self.raw_low_hum_alarm)

                line_content = str(line_position) + separator + date + separator + str(converted_temp)

                if self.high_alarm_status == "1":
                    line_content += separator + str(converted_high_alarm)

                if self.low_alarm_status == "1":
                    line_content += separator + str(converted_low_alarm)

                line_content += separator + str(converted_hum)

                if self.high_hum_alarm_status == "1":
                    line_content += separator + str(converted_high_hum_alarm)

                if self.low_hum_alarm_status == "1":
                    line_content += separator + str(converted_low_hum_alarm)

                line_content += separator + str(dew_point)

                if line_position == 1:
                    line_content += separator + str(self.serial)

                line_content += "\n"

                self.first_rec_time = self.first_rec_time + datetime.timedelta(0,self.intervale_rec)
                
                self.file_dest.write(line_content),
                line_position += 1

            value = self.raw_data[raw_data_number]
            raw_data_number += 1
        self.file_dest.close()

    # Convert the recorded data from the ELUSB1 device to the "standard" output format (same as the ELWINUSB software)
    def elusb1_convert(self):

        self.file_dest = open(self.dest_file, 'w')
        self.file_header += self.name + ",Time"
        separator = ","

        if self.unit == 0:
            self.file_header += self.text_celsius
        else:
            self.file_header += self.text_fahrenheit

        if self.high_alarm_status == "1":
            self.file_header += self.text_high_alarm

        if self.low_alarm_status == "1":
            self.file_header += self.text_low_alarm

        self.file_header += self.text_serial_number
        self.file_dest.write(self.file_header+"\n")

        line_position = 1
        value = self.raw_data[0]
        raw_data_number = 1

        while value != 255:
            date = str(self.first_rec_time.strftime("%d/%m/%Y %H:%M:%S"))

            converted_temp = self.temp_convert(value)

            converted_high_alarm = self.high_alarm_convert(self.raw_high_alarm)
            converted_low_alarm = self.low_alarm_convert(self.raw_low_alarm)

            line_content = str(line_position) + separator + date + separator + str(converted_temp)

            if self.high_alarm_status == "1":
                line_content += separator + str(converted_high_alarm)

            if self.low_alarm_status == "1":
                line_content += separator + str(converted_low_alarm)

            if line_position == 1:
                line_content += separator + str(self.serial)

            line_content += "\n"

            self.first_rec_time = self.first_rec_time + datetime.timedelta(0,self.intervale_rec)

            self.file_dest.write(line_content),
            line_position += 1
            value = self.raw_data[raw_data_number]
            raw_data_number += 1

        self.file_dest.close()

    # Extract the needed values to convert the recorded data (date, date offset, time between recordings, name of the recording, alarms, ...)
    def data_translate(self, recordings, config, status, destination_file, model):
        self.model = model
        self.unit = config[46]
        self.raw_high_alarm = config[34]
        self.raw_low_alarm = config[35]
        self.raw_high_hum_alarm = config[56]
        self.raw_low_hum_alarm = config[57]
        self.raw_data = recordings
        self.dest_file = destination_file
        self.name = self.name_translate(config)
        self.serial = (config[55] * 16777216) + (config[54] * 65536) + (config[53] * 256) + (config[52])
        self.offset_start = (config[27] * 16777216) + (config[26] * 65536) + (config[25] * 256) + (config[24])
        self.first_rec_time = datetime.datetime(2000+config[23], config[22], config[21], config[18], config[19], config[20]) + datetime.timedelta(0,self.offset_start)
        self.intervale_rec = (config[29] * 256) + config[28]
        self.high_alarm_status = status[0]
        self.low_alarm_status = status[1]
        self.high_hum_alarm_status = status[4]
        self.low_hum_alarm_status = status[5]

        if model == "elusb1_16":
            self.elusb1_convert()

        if model == "elusb1_17":
            self.elusb1_convert()

        if model == "elusb2" or model == "elusb2lcd":
            self.elusb2_convert()

###
### This part of commented code is for my internal testing... Will be removed
###
#status = [0, 0] # high and low alarm states
#config = [2, 0, 98, 117, 114, 101, 97, 117, 102, 105, 108, 105, 112, 101, 0, 0, 0, 0, 16, 8, 41, 14, 1, 10, 0, 0, 0, 0, 60, 0, 74, 0, 0, 0, 140, 80, 0, 0, 0, 63, 0, 0, 32, 194, 0, 0, 0, 0, 118, 50, 46, 48, 121, 243, 152, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#buffer_el1 = [136, 136, 135, 135, 135, 135, 134, 134, 134, 134, 255, 133, 133, 133]
#buffer_el2 = [124, 96, 125, 97, 126, 98, 127, 97, 125, 97, 125, 97, 125, 97, 125, 97, 125, 98, 125, 97, 255, 97, 125, 97]
#destination_file = "/tmp/test"
#recordings = buffer_el1
#model = "elusb1_16"

#el1_parse().data_translate(recordings, config, status, destination_file, model)
