# -*- coding: utf-8 -*-

# This module contains classes to manage EL1USB device
# This class reads the content of the EL-USB-1 thermometer 
# Romain Aviolat 2010
# Some GPL related stuffs should come there...one day

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
		
### OLD function
#	def input_name(self):
#		print "enter the name of the recording:",
#	
#		nom_test = ""
#	
#		while nom_test != "ok":
#	
#			nom = raw_input()
#			char = ""
#			# Illegal character list, the / is not listed...
#			liste = ["%", "&", "*", ",", ".", "/", ":", "<", ">", "?", "|", "(", ")"]
#	
#			if len(nom) > 15:
#				print "name's too long 15 char max,"
#	
#			else:			
#				for entry in liste:
#					if nom.find(entry) != -1:
#						print "Illegal char found"
#						char = "found"
#				if char != "found":
#					nom_test = "ok"
#			
#		for char in nom:
#			new_buffer.append(ord(char))
#	
#		count = len(nom)
#		while count != 16:
#	
#			new_buffer.append(0)
#			count += 1
			


		
	
