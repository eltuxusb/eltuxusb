# -*- coding: utf-8 -*-

# This module contains classes to manage EL1USB device
# This class reads the content of the EL-USB-1 thermometer 
# Romain Aviolat 2010
# Some GPL related stuffs should come there...one day

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
	
#	def setup(self, tab):
#		#print tab
#		self.model = tab[0]
#		self.cmd_typ = tab[1]
#		self.name = []
#		self.name.append(tab[2])
#		self.name.append(tab[3])
#		self.name.append(tab[4])
#		self.name.append(tab[5])
#		self.name.append(tab[6])
#		self.name.append(tab[7])
#		self.name.append(tab[8])
#		self.name.append(tab[9])
#		self.name.append(tab[10])
#		self.name.append(tab[11])
#		self.name.append(tab[12])
#		self.name.append(tab[13])
#		self.name.append(tab[14])
#		self.name.append(tab[15])
#		self.name.append(tab[16])
#		self.name.append(tab[17])
#		self.hour = tab[18]
#		self.minute = tab[19]
#		self.seconds = tab[20]
#		self.day = tab[21]
#		self.month = tab[22]
#		self.year = tab[23]
#		self.start_offset = []
#		self.start_offset.append(tab[24])
#		self.start_offset.append(tab[25])
#		self.start_offset.append(tab[26])
#		self.start_offset.append(tab[27])
#		self.sample_rate = []
#		self.sample_rate.append(tab[28])
#		self.sample_rate.append(tab[29])
#		self.sample_count = []
#		self.sample_count.append(tab[30])
#		self.sample_count.append(tab[31]) 
#		self.flag_bit = []
#		self.flag_bit.append(tab[32])
#		self.flag_bit.append(tab[33])
#		self.hal = tab[34]
#		self.lal = tab[35]
#		self.calib_m = []
#		self.calib_m.append(tab[36])
#		self.calib_m.append(tab[37])
#		self.calib_m.append(tab[38])
#		self.calib_m.append(tab[39])
#		self.calib_c = []
#		self.calib_c.append(tab[40])
#		self.calib_c.append(tab[41])
#		self.calib_c.append(tab[42])
#		self.calib_c.append(tab[43])
#		self.factory_use = []
#		self.factory_use.append(tab[44])		
#		self.factory_use.append(tab[45])
#		self.unit = tab[46]
#		self.flag_bit2 = tab[47]
#		self.version = []
#		self.version.append(tab[48])
#		self.version.append(tab[49])
#		self.version.append(tab[50])
#		self.version.append(tab[51])
#		self.sn = []
#		self.sn.append(tab[52])
#		self.sn.append(tab[53])
#		self.sn.append(tab[54])
#		self.sn.append(tab[55])
#		self.hal_ch2 = tab[56]
#		self.lal_ch2 = tab[57]
#		self.roll_count = tab[58]
#		self.res1 = tab[59]
#		self.res2 = tab[60]


#	def get_buffer(self):
#		
#		self.raw_buffer = []
#		
#		# byte 0 we read the device model and return it to the new_buffer
#		self.raw_buffer.append(self.model)
#
#		# byte 1 we set opperation command (should be 0 for reading) warning with this one...)
#		self.raw_buffer.append(self.cmd_typ)
#		
#		# Chain name
#		i=0
#		for elt in self.name:
#			self.raw_buffer.append(self.name[i])
#			i += 1
#
#		# Hour
#		self.raw_buffer.append(self.hour)
#
#		# Minutes
#		self.raw_buffer.append(self.minute)
#
#		# Seconds
#		self.raw_buffer.append(self.seconds)
#
#		# Day
#		self.raw_buffer.append(self.day)
#
#		# Month
#		self.raw_buffer.append(self.month)	
#
#		# Year
#		self.raw_buffer.append(self.year)	
#
#		# Chain start_offset
#		i=0
#		for elt in self.start_offset:
#			self.raw_buffer.append(self.start_offset[i])
#			i += 1
#
#		# Chain sample_rate
#		i=0
#		for elt in self.sample_rate:
#			self.raw_buffer.append(self.sample_rate[i])
#			i += 1
#
#		# Chain sample_count
#		i=0
#		for elt in self.sample_count:
#			self.raw_buffer.append(self.sample_count[i])
#			i += 1
#
#		# Chain flag_bit
#		i=0
#		for elt in self.flag_bit:
#			self.raw_buffer.append(self.flag_bit[i])
#			i += 1
#
#		# High alarm level
#		self.raw_buffer.append(self.hal)
#
#		# Low alarm level
#		self.raw_buffer.append(self.lal)
#
#		# Chain calib_m
#		i=0
#		for elt in self.calib_m:
#			self.raw_buffer.append(self.calib_m[i])
#			i += 1
#
#		# Chain calib_c
#		i=0
#		for elt in self.calib_c:
#			self.raw_buffer.append(self.calib_c[i])
#			i += 1
#
#		# Chain factory_use
#		i=0
#		for elt in self.factory_use:
#			self.raw_buffer.append(self.factory_use[i])
#			i += 1
#
#		# Unit
#		self.raw_buffer.append(self.unit)
#
#		# flag_bit2
#		self.raw_buffer.append(self.flag_bit2)
#
#		# Chain version
#		i=0
#		for elt in self.version:
#			self.raw_buffer.append(self.version[i])
#			i += 1
#
#		# Chain sn
#		i=0
#		for elt in self.sn:
#			self.raw_buffer.append(self.sn[i])
#			i += 1
#
#		# High alarm level ch2
#		self.raw_buffer.append(self.hal_ch2)
#
#
#		# Low alarm level ch2
#		self.raw_buffer.append(self.lal_ch2)
#
#		# roll_count
#		self.raw_buffer.append(self.roll_count)
#
#		# res1
#		self.raw_buffer.append(self.res1)
#
#		# res2
#		self.raw_buffer.append(self.res2)
#
#
#		while len(self.raw_buffer) != 64:
#			self.raw_buffer.append(0)
#
#		return self.raw_buffer
#		
#	


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
	
	# convert the two flag bit into a "binary string" 
	def base2tostr(self, base2):
		bin_32 = str(bin(base2)[2:])

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
		
			print "actual_buffer: ", self.read_config 

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

			print "actual_buffer: ", self.read_config 

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
			print "I wrote nothing"
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
			print "I wrote this shit"
			return True
		
	# This method reads the device status
	def status_read(self):

		self.status = self.read_config[32:34]
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

		print self.device_nb_packets

		# read the recordings (size depends of the device)	
		for i in range(self.device_nb_packets):
			self.read_block.extend(self.address.read(0x82, 0x1000, 0, 1000))

		#print self.read_block[0:1000]

		return True



	
