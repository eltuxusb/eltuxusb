# -*- coding: utf-8 -*-
# Those methods read, write and convert data from / to the device

import usb.core
import usb.util
import sys
import datetime
import time
#import el_devices_settings *
from el_devices_settings import el_settings, el_buffer

class el1_buffer:
    "Device configuration buffer"
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
        self.raw_buffer = []


class el_test:
    def __init__(self):
        self.rrr = 0


class el1_math:
    "Convert different units from or to the device"
    def __init__(self):
        self.fake = 0
    
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

    # Convert alarm to a decimal value
    def alarm_convert(self, value, unit):
        self.value_converted = 0

        if unit == 0:
            self.value_converted = (value * 2) + 80

        if unit == 1:
            self.value_converted = value + 40

        return int(self.value_converted)

    # Convert humidity alarm to a decimal value
    def humidity_alarm_convert(self, value):
        self.value_converted = 0

        self.value_converted = (value * 2)

        return int(self.value_converted)

    # convert the two flag bit into a "binary string"
    def base2tostr(self, base2):
        bin_32 = str(bin(base2)[2:])
        
        #print "base2tostr", base2 ###DEBUG

        while len(bin_32) < 8:
            bin_32 = "0" + bin_32
        return bin_32

    # convert base 256 serial number to base 10
    def sn_convert(self, sn):
        base10sn = self.base256to10(sn)
        base10sn = str(base10sn)
        
        while len(base10sn) < 9:
            base10sn = "0" + base10sn

        return base10sn

    # convert base 256 numbers to base 10
    def base256to10(self, base256):
        puissance = len(base256) -1
        base10 = 0

        for i in base256[::-1]:
            base10 += i * pow(256, puissance)
            puissance -= 1
        return base10

    # convert base 10 numbers to base 256
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

    # check if illegal characters were put in the recording name
    def illegal_char(self, name):
        found = 0
        illegal_char = ["%", "&", "*", ",", ".", "/", ":", "<", ">", "?", "|", "(", ")"]
        illegal_char_found = "illegal char found in name: "

        for entry in illegal_char:
            if name.find(entry) != -1:
                illegal_char_found += entry
                found = 1
        if found == 1:
            return illegal_char_found
        else:
            return False               

class el1_device:
    "Search, read, write to the device"
    def __init__(self, debug, recover_mode):
        self.debug = debug
        self.recover_mode = recover_mode
        self.device_model = ""
        self.device_full_name = ""
        self.last_error = ""
        self.address = 0
        self.read_config = 0
        self.str_items = []
        self.int_items = []
        # ANCIEN BUFFER self.rd_buffer = el1_buffer()

        self.new_buffer = el_buffer(self.debug)
        self.settings = el_settings()

        self.read_block = []
        self.flag_bits = ""

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

        #print "FlagBits", self.flag_bits ###DEBUG
        
        return self.flag_bits


    ### Internal needed functions
    # Search if the device is connected or not
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

        if self.debug:
            print "#DEBUG# DEVICE IDENT: %s" % self.read_config[0]
            print "#DEBUG# DEVICE MODEL: %s" % self.device_model
            print "#DEBUG# DEVICE NAME : %s" % self.device_full_name

    # Download datas
    def download(self):

        if self.status_read() != True:
            print "status error"
            return False

        else:
            if self.recordings_read() != True:
                return False
            else:
                return True

    # Clear flag bits, (download state / alarms)
    def clear_flag_bits(self):

        self.new_buffer.set_flag_bits([0,0])

        stop_buffer = self.new_buffer.get_modified_buffer()

        if self.debug:
            print "#DEBUG# STOP BUFFER: %s" % stop_buffer

        else:
            if self.config_write(stop_buffer) != True:
                return False

    # Stop the recording and keep the curent alarm/alarm latch and download state
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
            
            if self.debug:
                print "#DEBUG# stop buffer  : %s" % stop_buffer
                self.status = "#DEBUG# not stopped and NOT downloaded"

            else:
                self.config_write(stop_buffer)
                self.status = "stopped"

        return self.status

    # Read recovery config file from an external file
    def read_file(self, path):
     
        self.config_file = open(path)
        self.error = 0

        with self.config_file as f:
            self.str_items = f.readline().strip().split(', ')

        for i in self.str_items:
           if int(i) > 255 or int(i) < 0:
               self.error = 1
           self.int_items.append(int(i))
   
        if self.error != 0:
            return False

        else:
            if len(self.int_items) != 128 and len(self.int_items) != 256:
                return False
            else:
                return True   

    # Restore original backup of the device buffer (The backup_buffer was taken from my device (elusb1), in case I broke something)
    def restore_backup(self):

        if self.device_search() == False :
            return False

        if self.config_read() == False:
            return False

        if self.config_write(self.backup_buffer2) != True:
            return False
        else:
            print "OK"

    # Reads the device configuration
    def config_read(self):

        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

        # requesting device configuration
        msg = [0x00, 0xFF, 0xFF]
        print msg
        sent_bytes = self.address.write(0x02, msg, 100)
        # reading device configuration
        read_device = self.address.read(0x82, 0x03, 1000)

        if read_device[2] == 1:
            self.size = 257
        else:
            self.size = read_device[1] + 1

        self.read_config = self.address.read(0x82, self.size, 1000)

        if len(self.read_config) == 0:
            self.last_error = "error reading device configuration"
            return False
        else:
            self.read_config = self.read_config.tolist()
            self.new_buffer.set_buffer(self.read_config)
            
            if self.debug:
                print "#DEBUG# BUFFER SIZE: %s" % len(self.read_config)
                print "#DEBUG# ORIGINAL BUFFER: %s" % self.read_config

        usb.util.release_interface(self.address, 0x00)   

    # Write the configuration to the device
    def config_write(self, config_buffer):

        if self.recover_mode == False:
            if self.new_buffer.verify_buffer() == False:
                self.status = "Buffer error"
                return False

        # initialise device
        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

        # requesting device configuration
        msg = [0x01, 0x40, 0x00 ]
        sent_bytes = self.address.write(0x02, msg, 100)
        sent_bytes = self.address.write(0x02, config_buffer, 100)

        # reading device configuration
        read_device = self.address.read(0x82, 0x03, 1000)

        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x04)
        return True

    # Reads the device status (recording, stopped, ...)
    def status_read(self):

        self.status = self.read_config[32:34]

        #print "self.status", self.status##DEBUG
        
        self.fb = el1_math()
        self.flag_bits = ""
        for i in self.status:
            self.flag_bits += self.fb.base2tostr(i)[::-1]
        return True

    # Read the device recordings
    def recordings_read(self):

        # initialise device
        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

        # requesting device configuration
        msg = [0x00, 0xFF, 0xFF]
        sent_bytes = self.address.write(0x02, msg, 100)

        # reading device configuration
        read_device = self.address.read(0x82, 0x03, 1000)
        read_config = self.address.read(0x82, 0x1000, 1000)

        # initialise device
        self.address.ctrl_transfer(bmRequestType=0x40, bRequest=0x02, wValue=0x02)

        # request device configuration
        msg = [0x03, 0xFF, 0xFF]
        sent_bytes = self.address.write(0x02, msg, 100)

        # read device configuration
        read_device = self.address.read(0x82, 0x03, 1000)

        self.device_nb_packets = self.settings.get_device_nb_packets(self.device_model)

        #print self.device_nb_packets

        # read the recordings (size depends of the device)
        for i in range(self.device_nb_packets):
            self.read_block.extend(self.address.read(0x82, 0x1000, 1000))

        if self.debug:
            print "#DEBUG# NB RECORDS: %s" % len(self.read_block)
            print "#DEBUG# RECORDED DATAS: %s" % self.read_block[0:1000]

        usb.util.release_interface(self.address, 0x00)   
        
        return True


