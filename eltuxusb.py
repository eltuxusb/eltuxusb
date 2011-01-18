#! /usr/bin/env python
# -*- coding: utf-8 -*-

#This is the main file to launch the program

from el_device import *
from el_input import *
from el_parse import *
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import datetime
import time
from time import localtime
import os

pathname = os.path.dirname(sys.argv[0])        
full_path = os.path.abspath(pathname) 
os.chdir(full_path)

class eltuxusb:
    def __init__(self):
	self.dev1 = el1_device()
	self.parse = el1_parse()
	self.file = ""
	self.name_recording = ""
	self.model = ""
        self.widgets = gtk.glade.XML('eltuxusb.glade',"window1")
        events = { 'on_download_button_clicked': self.download,
                   'delete': self.delete,  
                   'on_checkbutton1_toggled': self.delay_recording,  
                   'on_checkbutton2_toggled': self.high_temp_alarm,
                   'on_checkbutton3_toggled': self.low_temp_alarm,
                   'on_checkbutton6_toggled': self.high_hum_alarm,
                   'on_checkbutton8_toggled': self.low_hum_alarm,
                   'on_new_button_clicked': self.new_recording,
                   'on_stop_button_clicked': self.stop_recording,	
                   'on_apply_button_clicked': self.start_recording,
                   'on_radiobutton1_toggled': self.switch_unit,
				   'on_refresh_button_clicked': self.refresh }
        self.widgets.signal_autoconnect(events)

    def delete(self, source=None, event=None):
	gtk.main_quit()

    def switch_unit(self, source=None, event=None):

		if self.widgets.get_widget('radiobutton1').get_active():
			self.widgets.get_widget('label9').set_text("high temp. alarm: (°C)")
			self.widgets.get_widget('label8').set_text("high temp. alarm: (°C)")
		else:
			self.widgets.get_widget('label9').set_text("high temp. alarm: (°F)")
			self.widgets.get_widget('label8').set_text("high temp. alarm: (°F)")

    def download(self, source=None, event=None):

	#self.dialog = "sgezg"
        # Setup the filechooserdialog
        chooser = gtk.FileChooserDialog(("please, choose an output file"),
            None,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE,
                        gtk.RESPONSE_OK))

        # Run the dialog
        response = chooser.run()

        if response == gtk.RESPONSE_OK:
            self.result = chooser.get_filename()

        else:
            chooser.destroy()
            return

        chooser.destroy()

	if self.dev1.init() == False:
		self.widgets.get_widget('label2').set_text(self.dev1.get_last_err())
		self.widgets.get_widget("found").hide()
		self.widgets.get_widget("not_found").show()

	else:
		if self.dev1.download() == False:
			self.widgets.get_widget('label2').set_text(self.dev1.get_last_err()) 
			##DEBUG##
			# print "afiche status", self.dev1.get_status()
			##DEBUG##

		else:
			self.parse.data_translate(self.dev1.get_data(), self.dev1.get_config(), self.dev1.get_status(), self.result, self.model)
			##DEBUG##
			# print "afiche status", self.dev1.get_status()
			##DEBUG##
			self.widgets.get_widget('label2').set_text('Downloaded and stopped')
			self.widgets.get_widget('stop_button').set_sensitive(False)	


    def refresh(self, source=None, event=None):
	if self.dev1.init() == False:
		self.widgets.get_widget('label2').set_text(self.dev1.get_last_err())
		self.widgets.get_widget('label15').set_text("")
		self.widgets.get_widget("found").hide()	
		self.widgets.get_widget("not_found").show()
		self.widgets.get_widget('stop_button').set_sensitive(False)	
		self.widgets.get_widget('download_button').set_sensitive(False)
		self.widgets.get_widget('new_button').set_sensitive(False)
		self.widgets.get_widget('entry1').set_text("")
		self.widgets.get_widget('vbox3').hide()


	else:
		status = "state: "
		self.model = self.dev1.device_model
		flag_bits = self.dev1.get_status()
		config  = self.dev1.get_config()
		full_name = self.dev1.device_full_name

		self.sample_count = el1_math().base256to10(config[30:32])

		if self.sample_count == 0:
			self.widgets.get_widget('download_button').set_sensitive(False)	
			status += "zero records, "
		else:
			self.widgets.get_widget('download_button').set_sensitive(True)	

		if flag_bits[8] == "1":
			status += "delayed start or logging, "
			self.widgets.get_widget('stop_button').set_sensitive(True)	
		else:
			status += "stopped, "
			self.widgets.get_widget('stop_button').set_sensitive(False)	

		if flag_bits[9] == "1":
			status += "data NOT downloaded"
		else:
			status += "data ALREADY downloaded"

		if flag_bits[10] == "1":
			status += ", during the last acquisition battery level dropped to a low level but logging continued"

		if flag_bits[11] == "1":
			status += ", during the last acquisition battery level dropped to a critical level and logging stopped"

		self.widgets.get_widget('label2').set_text(status)
		self.widgets.get_widget('label15').set_text(full_name)

		self.widgets.get_widget("found").show()
		self.widgets.get_widget("not_found").hide()
		#self.widgets.get_widget('stop_button').set_sensitive(True)	
	
		self.widgets.get_widget('new_button').set_sensitive(True)	
		self.name_recording = self.parse.name_translate(self.dev1.get_config())

		self.widgets.get_widget('entry1').set_text(self.name_recording)
	
		self.widgets.get_widget('checkbutton4').set_sensitive(False)
		self.widgets.get_widget('checkbutton5').set_sensitive(False)
		self.widgets.get_widget('checkbutton7').set_sensitive(False)
		self.widgets.get_widget('checkbutton9').set_sensitive(False)

		if self.model == "elusb2":
			self.widgets.get_widget("hbox13").show()
			self.widgets.get_widget("hbox14").show()
			self.widgets.get_widget("hbox15").show()
			self.widgets.get_widget("hbox16").show()
		else:					
			self.widgets.get_widget("hbox13").hide()
			self.widgets.get_widget("hbox14").hide()
			self.widgets.get_widget("hbox15").hide()
			self.widgets.get_widget("hbox16").hide()

	return True


    def delay_recording(self, source=None, event=None):
		self.hour = time.localtime()[3]
		self.minute = time.localtime()[4]


		if self.widgets.get_widget('checkbutton1').get_active() == True:
			self.widgets.get_widget('calendar1').set_sensitive(True)	
			self.widgets.get_widget('spin_button_hour').set_sensitive(True)
			self.widgets.get_widget('spin_button_min').set_sensitive(True)
			self.widgets.get_widget('spin_button_hour').set_value(self.hour)
			self.widgets.get_widget('spin_button_min').set_value(self.minute + 2)

		else:
			self.widgets.get_widget('calendar1').set_sensitive(False)
			self.widgets.get_widget('spin_button_hour').set_sensitive(False)
			self.widgets.get_widget('spin_button_min').set_sensitive(False)


    def new_recording(self, source=None, event=None):
	self.widgets.get_widget('vbox3').show()
	self.widgets.get_widget('combobox1').set_active(2)


    def stop_recording(self, source=None, event=None):
	self.status = self.dev1.stop_recording()
	self.widgets.get_widget('label2').set_text(self.status)


    def high_temp_alarm(self, source=None, event=None):
	if self.widgets.get_widget('checkbutton2').get_active() == True:
		self.widgets.get_widget('spin_button_high_alarm').set_sensitive(True)
		self.widgets.get_widget('checkbutton4').set_sensitive(True)
	else:
		self.widgets.get_widget('spin_button_high_alarm').set_sensitive(False)
		self.widgets.get_widget('checkbutton4').set_sensitive(False)

    def low_temp_alarm(self, source=None, event=None):	
	if self.widgets.get_widget('checkbutton3').get_active() == True:
		self.widgets.get_widget('spin_button_low_alarm').set_sensitive(True)
		self.widgets.get_widget('checkbutton5').set_sensitive(True)
	else:
		self.widgets.get_widget('spin_button_low_alarm').set_sensitive(False)
		self.widgets.get_widget('checkbutton5').set_sensitive(False)

    def high_hum_alarm(self, source=None, event=None):
	if self.widgets.get_widget('checkbutton6').get_active() == True:
		self.widgets.get_widget('spin_button_high_h_alarm').set_sensitive(True)
		self.widgets.get_widget('checkbutton7').set_sensitive(True)
	else:
		self.widgets.get_widget('spin_button_high_h_alarm').set_sensitive(False)
		self.widgets.get_widget('checkbutton7').set_sensitive(False)

    def low_hum_alarm(self, source=None, event=None):	
	if self.widgets.get_widget('checkbutton8').get_active() == True:
		self.widgets.get_widget('spin_button_low_h_alarm').set_sensitive(True)
		self.widgets.get_widget('checkbutton9').set_sensitive(True)
	else:
		self.widgets.get_widget('spin_button_low_h_alarm').set_sensitive(False)
		self.widgets.get_widget('checkbutton9').set_sensitive(False)



    ### We read the values entred by the user and write them to the device
    def start_recording(self, source=None, event=None):
	self.recording_name = ""
	self.high_alarm = 0
	self.high_alarm_latch = "0"
	self.high_humidity_alarm = 0
	self.high_humidity_alarm_latch = "0"
	self.low_alarm = 0
	self.low_alarm_latch = "0"
	self.low_humidity_alarm = 0
	self.low_humidity_alarm_latch = "0"
	self.flag_bit_32 = ""
	self.flag_bit_33 = ""
	self.widgets.get_widget('label12').set_text("")
	self.sample_rate = 0
	self.high_alarm_value = 0
	self.low_alarm_value = 0
	self.high_humidity_alarm_value = 0
	self.low_humidity_alarm_value = 0
	self.unit = 0
	self.start_sec = 0
	self.status = 0
	self.text_to_seconds = {
	    		         "10 sec": 10,
	                         "30 sec": 30,
	                         "1 min": 60,
	                         "30 min": 1800,
	                         "1 hour": 3600,
	                         "10 hours": 36000,
	                         "18 hours": 64800 }

	# We read the name value, and check if there's no illegal char in it, then we convert it to ascii string
	self.recording_name = self.widgets.get_widget('entry1').get_text()

	illegal_char = ["%", "&", "*", ",", ".", "/", ":", "<", ">", "?", "|", "(", ")"]
	illegal_char_found = "illegal char found in name: "

	for entry in illegal_char:
		if self.recording_name.find(entry) != -1:
			illegal_char_found += entry
			self.widgets.get_widget('label12').set_text(illegal_char_found)
			self.status = 1

	self.converted_name = el1_input().convert_name(self.recording_name)

	# We read the sample rate value and convert it from base 10 to 256
	self.sample_rate = self.widgets.get_widget('combobox1').get_active_text()
	self.converted_sample_rate = el1_math().base10to256(self.text_to_seconds.get(self.sample_rate), 2)

	# We check if the recording is delayed or not and set the start time/date value
	if self.widgets.get_widget('checkbutton1').get_active() == True:
		self.start_day = self.widgets.get_widget('calendar1').get_date()[2]
		self.start_month = self.widgets.get_widget('calendar1').get_date()[1]+1
		self.start_year = int(str(self.widgets.get_widget('calendar1').get_date()[0])[2:4])
		self.start_hour = self.widgets.get_widget('spin_button_hour').get_value_as_int()
		self.start_min = self.widgets.get_widget('spin_button_min').get_value_as_int()
		self.time_start = int(time.mktime([self.start_year, self.start_month, self.start_day, self.start_hour, self.start_min, self.start_sec, 0, 0, time.localtime()[8]]))
		self.time_sys = int(time.time())
		self.offset_seconds = self.time_start - self.time_sys

	# If not delayed we use the curent date and time 
	else:
		self.start_day = time.localtime()[2]	
		self.start_month = time.localtime()[1]
		self.start_year = int(str(time.localtime()[0])[2:4])
		self.start_hour = time.localtime()[3]
		self.start_min = time.localtime()[4]
		self.start_sec = time.localtime()[5]
		self.offset_seconds = 0

	if self.offset_seconds < 0:
		self.widgets.get_widget('label12').set_text("Start date is in the past")
		self.status = 1

	# We convert the offset seconds into a readable format for the device
	self.offset_seconds_converted = el1_math().base10to256(self.offset_seconds, 4)
	
	# Check the unit selected (Celsuis=0 or Fahrenheit=1)
	if self.widgets.get_widget('radiobutton1').get_active():
		self.unit = 0
	else:
		self.unit = 1

	# Check if high alarm is enabled (and alarm latch)
	if self.widgets.get_widget('checkbutton2').get_active() == True:
		self.high_alarm = "1"
		self.high_alarm_value = self.widgets.get_widget('spin_button_high_alarm').get_value() 
		self.high_alarm_value_converted = el1_math().alarm_convert(self.high_alarm_value, self.unit)

		if self.widgets.get_widget('checkbutton4').get_active() == True:
			self.high_alarm_latch = "1"	

	else:
		self.high_alarm = "0"
		self.high_alarm_latch = "0"
		self.high_alarm_value_converted = 0

	# Check if low alarm is enabled (and alarm latch)
	if self.widgets.get_widget('checkbutton3').get_active() == True:
		self.low_alarm = "1"
		self.low_alarm_value = self.widgets.get_widget('spin_button_low_alarm').get_value()
		self.low_alarm_value_converted = el1_math().alarm_convert(self.low_alarm_value, self.unit)


		if self.widgets.get_widget('checkbutton5').get_active() == True:
			self.low_alarm_latch = "1"	

	else:
		self.low_alarm = "0"
		self.low_alarm_value_converted = 0

	if self.model == "elusb2":
		# Check if high humidity alarm is enabled (and alarm latch)
		if self.widgets.get_widget('checkbutton6').get_active() == True:
			self.high_humidity_alarm = "1"
			self.high_humidity_alarm_value = self.widgets.get_widget('spin_button_high_h_alarm').get_value() 
			self.high_humidity_alarm_value_converted = el1_math().humidity_alarm_convert(self.high_humidity_alarm_value)

			if self.widgets.get_widget('checkbutton7').get_active() == True:
				self.high_humidity_alarm_latch = "1"	

		else:
			self.high_humidity_alarm = "0"
			self.high_humidity_alarm_latch = "0"
			self.high_humidity_alarm_value_converted = 0

		# Check if low humidity alarm is enabled (and alarm latch)
		if self.widgets.get_widget('checkbutton8').get_active() == True:
			self.low_humidity_alarm = "1"
			self.low_humidity_alarm_value = self.widgets.get_widget('spin_button_low_h_alarm').get_value() 
			self.low_humidity_alarm_value_converted = el1_math().humidity_alarm_convert(self.low_humidity_alarm_value)

			if self.widgets.get_widget('checkbutton9').get_active() == True:
				self.low_humidity_alarm_latch = "1"	

		else:
			self.low_humidity_alarm = "0"
			self.low_humidity_alarm_latch = "0"
			self.low_humidity_alarm_value_converted = 0

		self.flag_bit_32 += self.low_humidity_alarm_latch + self.high_humidity_alarm_latch + self.low_humidity_alarm + self.high_humidity_alarm + self.low_alarm_latch + self.high_alarm_latch + self.low_alarm + self.high_alarm

	else:
		self.flag_bit_32 += "0000" + self.low_alarm_latch + self.high_alarm_latch + self.low_alarm + self.high_alarm

	self.flag_bit_33 += "00000011"

	#print "TEMP"
	#print "high temp alarm", self.high_alarm, self.high_alarm_value_converted
	#print "high temp alarm latch", self.high_alarm_latch
	#print "low temp alarm", self.low_alarm, self.low_alarm_value_converted
	#print "low temp alarm latch", self.low_alarm_latch
	#print ""
	#print "HUM"
	#print "high hum alarm", self.high_humidity_alarm, self.high_humidity_alarm_value_converted
	#print "high hum alarm latch", self.high_humidity_alarm_latch
	#print "low hum alarm", self.low_humidity_alarm, self.low_humidity_alarm_value_converted
	#print "low hum alarm latch", self.low_humidity_alarm_latch




	# If eveything's ok ve set the different values to the new buffer
	if self.status == 0:

		self.dev1.new_buffer.set_cmd_type(0)
		self.dev1.new_buffer.set_flag_bits([int(self.flag_bit_32, 2), int(self.flag_bit_33, 2)])
		self.dev1.new_buffer.set_name(self.converted_name)
		self.dev1.new_buffer.set_sample_rate(self.converted_sample_rate)
		self.dev1.new_buffer.set_start_offset(self.offset_seconds_converted)
		self.dev1.new_buffer.set_unit(self.unit)
		self.dev1.new_buffer.set_hour(self.start_hour)
		self.dev1.new_buffer.set_minutes(self.start_min)
		self.dev1.new_buffer.set_seconds(0)
		self.dev1.new_buffer.set_day(self.start_day)
		self.dev1.new_buffer.set_month(self.start_month)
		self.dev1.new_buffer.set_year(self.start_year)
		self.dev1.new_buffer.set_hal(self.high_alarm_value_converted)
		self.dev1.new_buffer.set_lal(self.low_alarm_value_converted)

		self.dev1.new_buffer.set_sample_count([0, 0])

		if self.model == "elusb2":
			self.dev1.new_buffer.set_hal_ch2(self.high_humidity_alarm_value_converted)
			self.dev1.new_buffer.set_lal_ch2(self.low_humidity_alarm_value_converted)

		#self.dev1.new_buffer.set_sn([111, 111, 111, 111])

		old_buffer = self.dev1.new_buffer.get_original_buffer()
		new_buffer = self.dev1.new_buffer.get_modified_buffer()

	

		#print "old buffer: ", old_buffer
		#print ""
		#print "new buffer: ", new_buffer		
		
		# old method to create buffer# self.buffer_new_record = self.dev1.rd_buffer.get_buffer()

		if self.dev1.config_write(new_buffer) == True:
			self.widgets.get_widget('label12').set_text("Ready, please remove device")
		else:
			self.widgets.get_widget('label12').set_text("Something bad happened")		

if __name__ == '__main__':
    app = eltuxusb().refresh()
    gtk.main()

