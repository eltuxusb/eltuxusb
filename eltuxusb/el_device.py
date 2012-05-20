# -*- coding: utf-8 -*-
# This module contains classes to manage EL1USB device
# This class reads the content of the EL-USB-1 thermometer

import usb.core
import usb.util
import sys
import datetime
import time
from el_devices_settings import *

class el1_buffer:
    "Doc ..."
    def __init__(self):
        self.model = 1
        self.cmd_typ = 0
        self.name = ["rec1"]
        self.hour = time.localtime()[3]
        self.minute = time.localtime()[4]
        self.seconds = time.localtime()[5]
        self.day = time.localtime()[2]
        self.month = time.localtime()[1]
        self.year = time.localtime()[0]
        self.start_offset = 0
        self.sample_rate = 60
        self.sample_count = 0
        self.flag_bit = 0
        self.hal = 0
        self.lal = 0
        self.calib_m = 0 # Don't write !
        self.calib_c = 0# Don't write !
        self.factory_use = 0  # Don't write !
        self.unit = 0
        self.flag_bit2 = 0
        self.version = 0 # Don't write !
        self.sn = 0  # Don't write !
        self.hal_ch2 = 0
        self.lal_ch2 = 0
        self.roll_count = 0
        self.res1 = 0
        self.res2 = 0
        # Buffer brut (tableau)
        self.raw_buffer = []


class el1_math:
    "Doc..."
    def __init__(self):
        self.fake = 0

    def alarm_convert(self, value, unit):
        self.value_converted = 0

        if unit == 0:
            self.value_converted = (value * 2) + 80

        if unit == 1:
            self.value_converted = value + 40

        return int(self.value_converted)

    def humidity_alarm_convert(self, value):
        self.value_converted = 0

        self.value_converted = (value * 2)

        return int(self.value_converted)

    # convert the two flag bit into a "binary string"
    def base2tostr(self, base2):
        bin_32 = str(bin(base2)[2:])

        ##DEBUG##
        #print "base2tostr", base2
        ##DEBUG##

        while len(bin_32) < 8:
            bin_32 = "0" + bin_32


        return bin_32

    # This function convert base 256 numbers to base 10
    def base256to10(self, base256):
        puissance = len(base256) -1
        base10 = 0

        for i in base256[::-1]:
            base10 += i * pow(256, puissance)
            puissance -= 1
        return base10

    def base10to256(self, base10, nb_bits):

        puissance = 1
        base256 = []
        base10_tmp = base10

        while (base10_tmp / 256) >= 1:
            puissance += 1
            base10_tmp = int(base10_tmp / 256)

        for i in range(puissance)[::-1]:

            base256.append(int(base10 / pow(256, i)))
            base10 = base10 % pow(256, i)

        while len(base256) != nb_bits:

            base256.insert(0, 0)

        return base256[::-1]


class el1_device:
    "Doc ..."
    def __init__(self):
        self.debug_actual_buffer = 0  # Debug output 1 = ON
        self.debug_stopped_buffer = 0 # Debug output 1 = ON
        self.debug_recorded_data = 0  # Debug output 1 = ON
        self.device_model = ""
        self.device_full_name = ""
        self.last_error = ""
        self.address = 0
        self.read_config = 0
        # ANCIEN BUFFER self.rd_buffer = el1_buffer()

        self.new_buffer = el_buffer()
        self.settings = el_settings()

        self.read_block = []
        self.flag_bits = ""
        self.backup_buffer = [2, 0, 98, 117, 114, 101, 97, 117, 102, 105, 108, 105, 112, 101, 0, 0, 0, 0, 16, 8, 41, 14, 1, 10, 0, 0, 0, 0, 60, 0, 1, 0, 4, 0, 140, 80, 0, 0, 0, 63, 0, 0, 32, 194, 0, 0, 0, 0, 118, 50, 46, 48, 121, 243, 152, 0, 0, 0, 0, 0, 0, 0, 0, 0]



    ### "Public" usable functions
    def get_last_err(self):
        return self.last_error

    def print_last_err(self):
        print self.get_last_error()

    def get_data(self):
        return self.read_block

    def get_config(self):
        return self.read_config

    def get_status(self):
        #self.init()
        self.status_read()

        ##DEBUG##
        #print "FlagBits", self.flag_bits
        ##DEBUG##

        return self.flag_bits


    ### Internal needed functions

    # This function search if the device is connected or not
    def device_search(self):
        self.address = usb.core.find(idVendor=0x10c4, idProduct=0x0002)

        if self.address is None:
            self.last_error = "device not found"
            return False

    # Initialize the device
    def init(self):
        if self.device_search() == False :
            return False

        if self.config_read() == False:
            return False

        self.identify_device()

    # Identify the device from the first byte of the configuration buffer
    def identify_device(self):
        self.device_model = self.settings.get_device_model(str(self.read_config[0]))
        self.device_full_name = self.settings.get_device_full_name(self.device_model)
        self.new_buffer.set_model(self.device_model)

        #print "\ntemp. debug (device ident)    : %s" % self.read_config[0]    #CLEAN_ME
        #print "temp. debug (device model)    : %s" % self.device_model      #CLEAN_ME
        #print "temp. debug (device full name): %s \n" % self.device_full_name  #CLEAN_ME

    # Download datas and stop device
    def download(self):

        if self.status_read() != True:
            print "status error"
            return False

        else:
            if self.recordings_read() != True:
                return False


            self.new_buffer.set_flag_bits([0,0])


            stop_buffer = self.new_buffer.get_modified_buffer()

            if self.debug_actual_buffer == 1:
                print "actual_buffer: ", self.read_config

            if self.debug_stopped_buffer == 1:
                print "stopped buffer: ", stop_buffer

            if self.config_write(stop_buffer) != True:
                return False


    # Just stop the recording anbd keep the curent alarm/alarm latch and download state
    def stop_recording(self):

        flag_bits = self.get_status()

        self.flag_bit_32 = flag_bits[0:8][::-1]
        self.flag_bit_33 = "00000010"

        if flag_bits[8] == "0":
            self.status = "device is already stopped"

        else:

            self.config_read()

            self.new_buffer.set_flag_bits([int(self.flag_bit_32, 2), int(self.flag_bit_33, 2)])
            stop_buffer = self.new_buffer.get_modified_buffer()

            self.config_write(stop_buffer)

            if self.debug_actual_buffer == 1:
                print "actual_buffer: ", self.read_config

            if self.debug_stopped_buffer == 1:
                print "stopped buffer: ", stop_buffer

            self.status = "stopped but NOT downloaded"

        return self.status

    # restore original backup of the device buffer
    def restore_backup(self):
        if self.device_search() == False :
            return False

        if self.config_read() == False:
            return False

        if self.config_write(self.backup_buffer) != True:
            return False


    # Reads config
    def config_read(self):

        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

        # requesting device configuration
        msg = [0x00, 0xFF, 0xFF]
        sent_bytes = self.address.write(0x02, msg, 0, 100)

        # reading device configuration
        read_device = self.address.read(0x82, 0x03, 0, 1000)
        self.size = read_device[1] + 1
        self.read_config = self.address.read(0x82, self.size, 0, 1000)
        #print self.read_config
        if len(self.read_config) == 0:
            self.last_error = "error reading device configuration"
            return False
        else:
            self.read_config = self.read_config.tolist()
            self.new_buffer.set_buffer(self.read_config)

    # This function write the configuration to the device
    def config_write(self, config_buffer):

        if self.new_buffer.verify_buffer() == False:
            self.status = "Buffer error"
            return False

        else:
            #dev = device_search(vendorid)
            # initialise device
            self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

            # requesting device configuration
            msg = [0x01, 0x40, 0x00 ]
            sent_bytes = self.address.write(0x02, msg, 0, 100)
            sent_bytes = self.address.write(0x02, config_buffer, 0, 100)

            # reading device configuration
            read_device = self.address.read(0x82, 0x03, 0, 1000)

            self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x04)
            return True

    # This method reads the device status
    def status_read(self):

        self.status = self.read_config[32:34]

        ##DEBUG##
        #print "self.status", self.status
        ##DEBUG##

        self.fb = el1_math()
        self.flag_bits = ""
        for i in self.status:
            self.flag_bits += self.fb.base2tostr(i)[::-1]
        return True


    def recordings_read(self):

        # initialise device
        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

        # requesting device configuration
        msg = [0x00, 0xFF, 0xFF]
        sent_bytes = self.address.write(0x02, msg, 0, 100)

        # reading device configuration
        read_device = self.address.read(0x82, 0x03, 0, 1000)
        read_config = self.address.read(0x82, 0x1000, 0, 1000)

        # initialise device
        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

        # request device configuration
        msg = [0x03, 0xFF, 0xFF]
        sent_bytes = self.address.write(0x02, msg, 0, 100)

        # read device configuration
        read_device = self.address.read(0x82, 0x03, 0, 1000)

        self.device_nb_packets = self.settings.get_device_nb_packets(self.device_model)

        #print self.device_nb_packets

        # read the recordings (size depends of the device)
        for i in range(self.device_nb_packets):
            self.read_block.extend(self.address.read(0x82, 0x1000, 0, 1000))

        if self.debug_recorded_data == 1:
            print self.read_block[0:1000]

        return True
