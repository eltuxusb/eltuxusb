# -*- coding: utf-8 -*-
# This module contains classes to manage EL1USB device
# This class reads the content of the EL-USB-1 thermometer 

import sys
import datetime
import time

class el1_input:
	"Doc ..."
	def __init__(self):
		self.fake = 0
						
	def request(self, text, base_value, min_value, max_value):
		print text,
		while base_value < min_value or base_value > max_value:
			base_value = input()	
			if base_value < min_value:
				print "value too low, should be between", min_value, "and", max_value	
			if base_value > max_value:
				print "value too high, should be between", min_value, "and", max_value
	
		return base_value
		
		
	def convert_name(self, name):

		new_buffer = []		
	
		for char in name:
			new_buffer.append(ord(char))
	
		count = len(name)
		while count != 16:
	
			new_buffer.append(0)
			count += 1
		return new_buffer
		
	
