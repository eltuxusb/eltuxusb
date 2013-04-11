# -*- coding: utf-8 -*-
# Command-line interface

import datetime, time, os

#from el_device import init, get_config, get_last_err, get_data, get_status, stop_recordings # <- need to clean, dirty
from el_device import * # <- need to clean, dirty
from el_input import *  # <- need to clean, dirty
from el_parse import *  # <- need to clean, dirty

class el_cmd:
    def __init__(self, path, debug, recover_mode):
        self.debug = debug
        self.recover_mode = recover_mode
        self.path = path
        self.parse = el1_parse()

    def download(self):
        self.model = ""
        self.full_name = ""
        self.config = ""

        self.dev1 = el1_device(self.debug, self.recover_mode)

        if self.dev1.init() == False:
            print (self.dev1.get_last_err())

        else:
            self.config  = self.dev1.get_config()
            self.model = self.dev1.device_model
            self.full_name = self.dev1.device_full_name
            self.sample_count = el1_math().base256to10(self.config[30:32])

            print "Found: %s\nDownloading data to: %s" % (self.full_name, self.path) 

            if self.dev1.download():
                print "Finished: downloaded %s recordings" % self.sample_count
                self.parse.data_translate(self.dev1.get_data(), self.dev1.get_config(), self.dev1.get_status(), self.path, self.model)

                self.status = self.dev1.stop_recording()
                print self.status

    def recover(self):
        self.dev1 = el1_device(self.debug, self.recover_mode)

        if os.path.exists(self.path):
            

            self.dev1.init()

            if self.dev1.read_file(self.path):
                print "File successfully imported"
        
        else:
            #THIS CHECK SHOULD ME MADE INSIDE THE DEF READ_FILE
            print "File does not exists"

        #self.dev1.restore_backup()

