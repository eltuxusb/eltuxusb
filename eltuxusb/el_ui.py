# -*- coding: utf-8 -*-
# Functions related to the user interface

import datetime, time, gobject, os
from gi.repository import Gtk

#pygtk.require("2.0")

from el_device import * # <- need to clean, dirty
from el_input import *  # <- need to clean, dirty
from el_parse import *  # <- need to clean, dirty
from el_plot import *  # <- need to clean, dirty
#from el_devices_settings import * # <- need to clean, dirty

# Auto-determine the location of the Glade file.
my_directory = os.path.dirname(os.path.realpath(__file__))
glade_file = os.path.join(my_directory, 'eltuxusb.glade')

class eltuxusb:
    def __init__(self, debug):
        self.debug = debug
        if self.debug:
            self.dev1 = el1_device(debug=True)
        else:
            self.dev1 = el1_device(debug=False)
        self.parse = el1_parse()
        self.file = ""
        self.name_recording = ""
        self.model = ""
        self.widgets = Gtk.Builder()
        self.widgets.add_from_file(glade_file)
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
                   'on_about_button_clicked': self.about_windows,
                   'on_graph_button_clicked': self.generate_graph,
                   'on_refresh_button_clicked': self.refresh }
        self.widgets.connect_signals(events)

    def delete(self, source=None, event=None):
        Gtk.main_quit()

    def switch_unit(self, source=None, event=None):

        if self.widgets.get_object('radiobutton1').get_active():
            self.widgets.get_object('label9').set_text("high temp. alarm: (°C)")
            self.widgets.get_object('label8').set_text("high temp. alarm: (°C)")
        else:
            self.widgets.get_object('label9').set_text("high temp. alarm: (°F)")
            self.widgets.get_object('label8').set_text("high temp. alarm: (°F)")

    def about_windows(self, source=None, event=None):
        self.about = Gtk.AboutDialog()
        #self.about.set_position(Gtk.WIN_POS_CENTER)
        self.about.set_name("ELTuxUSB")
        self.about.set_program_name("ELTuxUSB")
        self.about.set_website("https://github.com/eltuxusb")
        self.about.set_website_label("https://github.com/eltuxusb")
        self.about.set_copyright(u'Copyright \u00A9 2009-2012 Romain Aviolat')
        self.about.set_version("0.4")
        self.about.set_authors(["Romain Aviolat", "David Strauss"])

        self.about.run()
        self.about.destroy()

    def generate_graph(self, source=None, event=None):
        # Setup the filechooserdialog
        chooser = Gtk.FileChooserDialog(("select a previously saved recording"),
            Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = chooser.run()
        
        if response == Gtk.ResponseType.OK:
            self.result = chooser.get_filename()
            graph = plot()
            graph.parse_file(self.result)
            graph.render_plot()

        chooser.destroy()

    def download(self, source=None, event=None):
        # Setup the filechooserdialog
        chooser = Gtk.FileChooserDialog(("please, choose an output file"),
            None,
            Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = chooser.run()

        if response == Gtk.ResponseType.OK:
            self.result = chooser.get_filename()
            
        chooser.destroy()

        if self.dev1.init() == False:
            self.widgets.get_object('label2').set_text(self.dev1.get_last_err())
            self.widgets.get_object("found").hide()
            self.widgets.get_object("not_found").show()

        else:
            if self.dev1.download() == False:
                self.widgets.get_object('label2').set_text(self.dev1.get_last_err())

            else:
                if self.dev1.clear_flag_bits() == False:
                    self.widgets.get_object('label2').set_text(self.dev1.get_last_err())
                else:
                    self.parse.data_translate(self.dev1.get_data(), self.dev1.get_config(), self.dev1.get_status(), self.result, self.model)
                    if self.debug:
                        self.widgets.get_object('label2').set_text('Downloaded but not stopped')                
                    else:
                        self.widgets.get_object('label2').set_text('Downloaded and stopped')
                        self.widgets.get_object('stop_button').set_sensitive(False)


    def refresh(self, source=None, event=None):
        if self.dev1.init() == False:
            self.widgets.get_object('label2').set_text(self.dev1.get_last_err())
            self.widgets.get_object('label15').set_text("")
            self.widgets.get_object("found").hide()
            self.widgets.get_object("not_found").show()
            self.widgets.get_object('stop_button').set_sensitive(False)
            self.widgets.get_object('download_button').set_sensitive(False)
            self.widgets.get_object('new_button').set_sensitive(False)
            self.widgets.get_object('entry1').set_text("")
            self.widgets.get_object('vbox3').hide()

            if self.debug:
                print "#DEBUG# DEVICE NOT FOUND"
        else:
            self.status_msg = "state: "
            self.model = self.dev1.device_model
            flag_bits = self.dev1.get_status()
            config  = self.dev1.get_config()
            self.full_name = self.dev1.device_full_name

            self.math = el1_math()

            self.sample_count = self.math.base256to10(config[30:32])

            if self.sample_count == 0:
                self.widgets.get_object('download_button').set_sensitive(False)
                self.status_msg += "zero records, "
            else:
                self.widgets.get_object('download_button').set_sensitive(True)

            self.display_recordings = str(self.sample_count) + " recordings"
            self.widgets.get_object('label21').set_text(self.display_recordings)
            self.widgets.get_object('label21').show()
            self.widgets.get_object('recordings').show()


            if self.model != "elusb2" and self.model != "elusb1_17":
                self.widgets.get_object('download_button').set_sensitive(False)
                self.widgets.get_object('stop_button').set_sensitive(False)
                self.widgets.get_object('new_button').set_sensitive(False)
                self.widgets.get_object('label15').set_text(self.full_name)
                self.widgets.get_object('label2').set_text("DEVICE NOT SUPPORTED YET")

            else:

                if flag_bits[8] == "1":
                    self.status_msg += "delayed start or logging, "
                    self.widgets.get_object('stop_button').set_sensitive(True)
                else:
                    self.status_msg += "stopped, "
                    self.widgets.get_object('stop_button').set_sensitive(False)

                if flag_bits[9] == "1":
                    self.status_msg += "data NOT downloaded"
                else:
                    self.status_msg += "data ALREADY downloaded"

                if flag_bits[10] == "1":
                    self.status_msg += ", during the last acquisition battery level dropped to a low level but logging continued"

                if flag_bits[11] == "1":
                    self.status_msg += ", during the last acquisition battery level dropped to a critical level and logging stopped"

                self.widgets.get_object('label2').set_text(self.status_msg)
                self.widgets.get_object('label15').set_text(self.full_name)

                self.widgets.get_object("found").show()
                self.widgets.get_object("not_found").hide()
                #self.widgets.get_object('stop_button').set_sensitive(True)

                self.widgets.get_object('new_button').set_sensitive(True)
                self.name_recording = self.math.name_translate(self.dev1.get_config()[2:18])

                self.widgets.get_object('entry1').set_text(self.name_recording)

                self.widgets.get_object('checkbutton4').set_sensitive(False)
                self.widgets.get_object('checkbutton5').set_sensitive(False)
                self.widgets.get_object('checkbutton7').set_sensitive(False)
                self.widgets.get_object('checkbutton9').set_sensitive(False)

                if self.model == "elusb2" or self.model == "elusb2lcd":
                    self.widgets.get_object("hbox13").show()
                    self.widgets.get_object("hbox14").show()
                    self.widgets.get_object("hbox15").show()
                    self.widgets.get_object("hbox16").show()
                else:
                    self.widgets.get_object("hbox13").hide()
                    self.widgets.get_object("hbox14").hide()
                    self.widgets.get_object("hbox15").hide()
                    self.widgets.get_object("hbox16").hide()

            if self.debug:

                self.widgets.get_object('label1').set_text("eltuxusb device manager (DEBUG MODE)")
                print "#DEBUG# DEVICE STATE: %s" % self.status_msg  
                print "#DEBUG# RECORDING COUNT: %d" % self.sample_count

        return True

    def delay_recording(self, source=None, event=None):
        self.hour = time.localtime()[3]
        self.minute = time.localtime()[4]


        if self.widgets.get_object('checkbutton1').get_active() == True:
            self.widgets.get_object('calendar1').show()
            self.widgets.get_object('calendar1').set_sensitive(True)
            self.widgets.get_object('spin_button_hour').set_sensitive(True)
            self.widgets.get_object('spin_button_hour').set_value(self.hour)
            self.widgets.get_object('spin_button_hour').set_range(0, 23)
            self.widgets.get_object('spin_button_min').set_sensitive(True)
            self.widgets.get_object('spin_button_min').set_value(self.minute + 2)
            self.widgets.get_object('spin_button_min').set_range(0, 59)

        else:
            self.widgets.get_object('calendar1').hide()
            self.widgets.get_object('calendar1').set_sensitive(False)
            self.widgets.get_object('spin_button_hour').set_sensitive(False)
            self.widgets.get_object('spin_button_min').set_sensitive(False)


    def new_recording(self, source=None, event=None):
        self.widgets.get_object('vbox3').show()
        self.widgets.get_object('calendar1').hide()

    def stop_recording(self, source=None, event=None):
        self.status_msg = self.dev1.stop_recording()
        self.widgets.get_object('label2').set_text(self.status_msg)


    def high_temp_alarm(self, source=None, event=None):
        if self.widgets.get_object('checkbutton2').get_active() == True:
            self.widgets.get_object('spin_button_high_alarm').set_sensitive(True)
            self.widgets.get_object('spin_button_high_alarm').set_range(-39.5, 87.5)
            self.widgets.get_object('spin_button_high_alarm').set_increments(0.5, 10)
            self.widgets.get_object('checkbutton4').set_sensitive(True)
        else:
            self.widgets.get_object('spin_button_high_alarm').set_sensitive(False)
            self.widgets.get_object('checkbutton4').set_sensitive(False)

    def low_temp_alarm(self, source=None, event=None):
        if self.widgets.get_object('checkbutton3').get_active() == True:
            self.widgets.get_object('spin_button_low_alarm').set_sensitive(True)
            self.widgets.get_object('spin_button_low_alarm').set_range(-39.5, 87.5)
            self.widgets.get_object('spin_button_low_alarm').set_increments(0.5, 10)
            self.widgets.get_object('checkbutton5').set_sensitive(True)
        else:
            self.widgets.get_object('spin_button_low_alarm').set_sensitive(False)
            self.widgets.get_object('checkbutton5').set_sensitive(False)

    def high_hum_alarm(self, source=None, event=None):
        if self.widgets.get_object('checkbutton6').get_active() == True:
            self.widgets.get_object('spin_button_high_h_alarm').set_sensitive(True)
            self.widgets.get_object('spin_button_high_h_alarm').set_range(0, 100)
            self.widgets.get_object('spin_button_high_h_alarm').set_increments(1, 10)
            self.widgets.get_object('checkbutton7').set_sensitive(True)
        else:
            self.widgets.get_object('spin_button_high_h_alarm').set_sensitive(False)
            self.widgets.get_object('checkbutton7').set_sensitive(False)

    def low_hum_alarm(self, source=None, event=None):
        if self.widgets.get_object('checkbutton8').get_active() == True:
            self.widgets.get_object('spin_button_low_h_alarm').set_sensitive(True)
            self.widgets.get_object('spin_button_low_h_alarm').set_range(0, 100)
            self.widgets.get_object('spin_button_low_h_alarm').set_increments(1, 10)
            self.widgets.get_object('checkbutton9').set_sensitive(True)
        else:
            self.widgets.get_object('spin_button_low_h_alarm').set_sensitive(False)
            self.widgets.get_object('checkbutton9').set_sensitive(False)

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
        self.widgets.get_object('label12').set_text("")
        self.sample_rate = 0
        self.high_alarm_value = 0
        self.low_alarm_value = 0
        self.high_humidity_alarm_value = 0
        self.low_humidity_alarm_value = 0
        self.unit = 0
        self.start_sec = 0
        self.status = 0

        # Read the entered recording name, and check if there's no illegal char in it, then we convert it to ascii string
        self.recording_name = self.widgets.get_object('entry1').get_text()
        self.illegal_char = self.math.illegal_char(self.recording_name)

        if self.illegal_char:
            self.status = 1
            self.widgets.get_object('label12').set_text(self.illegal_char)
                
        self.converted_name = el1_input().convert_name(self.recording_name)

        # Read the selected sample rate (from the combobox) 
        self.combobox_item = self.widgets.get_object('combobox1').get_active()
        self.sample_rate = self.widgets.get_object('combobox1').get_model()[self.combobox_item][1]
           
        # And convert it from base 10 to 256
        self.converted_sample_rate = self.math.base10to256(self.sample_rate, 2)

        # We check if the recording is delayed or not and set the start time/date value
        if self.widgets.get_object('checkbutton1').get_active() == True:
            self.start_day = int(self.widgets.get_object('calendar1').get_date()[2])
            self.start_month = int(self.widgets.get_object('calendar1').get_date()[1]+1)
            self.start_year = int(str(self.widgets.get_object('calendar1').get_date()[0])[2:4])
            self.start_hour = self.widgets.get_object('spin_button_hour').get_value_as_int()
            self.start_min = self.widgets.get_object('spin_button_min').get_value_as_int()
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
            self.widgets.get_object('label12').set_text("Start date is in the past")
            self.status = 1

        # We convert the offset seconds into a readable format for the device
        self.offset_seconds_converted = self.math.base10to256(self.offset_seconds, 4)

        # Check the unit selected (Celsuis=0 or Fahrenheit=1)
        if self.widgets.get_object('radiobutton1').get_active():
            self.unit = 0
        else:
            self.unit = 1

        # Check if high alarm is enabled (and alarm latch)
        if self.widgets.get_object('checkbutton2').get_active() == True:
            self.high_alarm = "1"
            self.high_alarm_value = self.widgets.get_object('spin_button_high_alarm').get_value_as_int()
            self.high_alarm_value_converted = self.math.alarm_convert(self.high_alarm_value, self.unit)

            if self.widgets.get_object('checkbutton4').get_active() == True:
                self.high_alarm_latch = "1"

        else:
            self.high_alarm = "0"
            self.high_alarm_latch = "0"
            self.high_alarm_value_converted = 0

        # Check if low alarm is enabled (and alarm latch)
        if self.widgets.get_object('checkbutton3').get_active() == True:
            self.low_alarm = "1"
            self.low_alarm_value = self.widgets.get_object('spin_button_low_alarm').get_value_as_int()
            self.low_alarm_value_converted = self.math.alarm_convert(self.low_alarm_value, self.unit)


            if self.widgets.get_object('checkbutton5').get_active() == True:
                self.low_alarm_latch = "1"

        else:
            self.low_alarm = "0"
            self.low_alarm_value_converted = 0

        if self.model == "elusb2" or self.model == "elusb2lcd":
            # Check if high humidity alarm is enabled (and alarm latch)
            if self.widgets.get_object('checkbutton6').get_active() == True:
                self.high_humidity_alarm = "1"
                self.high_humidity_alarm_value = self.widgets.get_object('spin_button_high_h_alarm').get_value_as_int()
                self.high_humidity_alarm_value_converted = self.math.humidity_alarm_convert(self.high_humidity_alarm_value)

                if self.widgets.get_object('checkbutton7').get_active() == True:
                    self.high_humidity_alarm_latch = "1"

            else:
                self.high_humidity_alarm = "0"
                self.high_humidity_alarm_latch = "0"
                self.high_humidity_alarm_value_converted = 0

            # Check if low humidity alarm is enabled (and alarm latch)
            if self.widgets.get_object('checkbutton8').get_active() == True:
                self.low_humidity_alarm = "1"
                self.low_humidity_alarm_value = self.widgets.get_object('spin_button_low_h_alarm').get_value_as_int()
                self.low_humidity_alarm_value_converted = self.math.humidity_alarm_convert(self.low_humidity_alarm_value)

                if self.widgets.get_object('checkbutton9').get_active() == True:
                    self.low_humidity_alarm_latch = "1"

            else:
                self.low_humidity_alarm = "0"
                self.low_humidity_alarm_latch = "0"
                self.low_humidity_alarm_value_converted = 0

            self.flag_bit_32 += self.low_humidity_alarm_latch + self.high_humidity_alarm_latch + self.low_humidity_alarm + self.high_humidity_alarm + self.low_alarm_latch + self.high_alarm_latch + self.low_alarm + self.high_alarm

        else:
            self.flag_bit_32 += "0000" + self.low_alarm_latch + self.high_alarm_latch + self.low_alarm + self.high_alarm

        self.flag_bit_33 += "00000011"

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

            if self.model == "elusb2" or self.model == "elusb2lcd":
                self.dev1.new_buffer.set_hal_ch2(self.high_humidity_alarm_value_converted)
                self.dev1.new_buffer.set_lal_ch2(self.low_humidity_alarm_value_converted)

            #self.dev1.new_buffer.set_sn([111, 111, 111, 111]) ### TESTING PURPOSE

            old_buffer = self.dev1.new_buffer.get_original_buffer()
            new_buffer = self.dev1.new_buffer.get_modified_buffer()
            
            if self.debug:
                self.widgets.get_object('label12').set_text("Debug mode, nothing sent to the device, see console")
                print "#DEBUG# NEW CONFIG  : %s" % new_buffer          
            
            else:

                if self.dev1.config_write(new_buffer) == True:
                    self.widgets.get_object('label12').set_text("Ready, please remove device")
                else:
                    self.widgets.get_object('label12').set_text("Something bad happened")

