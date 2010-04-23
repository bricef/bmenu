#!/usr/bin/env python

import re, gtk, os, sys, subprocess, time, datetime

#PIPE_TIMEOUT=5
LABEL_MARKUP="<span color=\"#000000\"><b>%s</b></span>"

def make_exec(entry):
	try:
		command = entry["command"]
	except KeyError:
		print "[FATAL ERROR]: an 'exec' command has nothing to execute!"
		exit()
	
	try:
		item = gtk.MenuItem(entry["label"])
	except KeyError:
		print "[WARNING]: an 'exec' statement has no label, using command as label"
		item = gtk.MenuItem(command)
		
	item.connect("activate", _generate_callback(command))
	return item
	
def make_separator(entry):
	item=gtk.SeparatorMenuItem()
	return item

def make_submenu(entry, entries):
	print entries
	item=gtk.MenuItem("submenu")
	item.set_submenu(makeMenu(entries))
	item.toggle_size_allocate(12)
	return item

def make_label(entry):
	item = gtk.MenuItem(entry["label"])
	item.set_sensitive(False)
	label = item.get_children()[0]
	label.set_markup(LABEL_MARKUP%entry["label"])
	return item
	

def make_DYNAMIC_pipemenu(entry):
	command = entry["command"]
	item = gtk.MenuItem(entry["label"])
	menu=gtk.Menu()
	
	item.set_submenu(menu)
	item.connect("activate", dynamic_menu(), menu, entry["command"])
	
	return item

def dynamic_menu():
	def fn(widget, menu, command):
		#print menu
		#print command
		for item in menu.get_children():
			menu.remove(item)
		
		sub = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		(sout,serr) = sub.communicate()
		menu = makeMenu(parse_menu(sout))
		menu.show_all()
		widget.set_submenu(menu)
	return fn

def make_SIMPLE_pipemenu(entry):
	command = entry["command"]
	sub = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	(sout,serr) = sub.communicate()
	menu = makeMenu(parse_menu(sout))
	item = gtk.MenuItem(entry["label"])
	item.set_submenu(menu)
	return item


def _generate_callback(command):
	def callback(menuitem):
		os.system(command+" &")
		exit()
	return callback

def makeMenu(entries):
	menu = gtk.Menu()
	while entries:
		entry=entries.pop(0)
		#print entry
		if entry["type"] == "exec":
			menu.append(make_exec(entry))
		elif entry["type"] == "separator":
			menu.append(make_separator(entry))
		elif entry["type"] == "submenu":
			item = gtk.MenuItem(entry["label"])
			item.set_submenu(makeMenu(entries))
			menu.append(item)
		elif entry["type"] == "/submenu":
			return menu
		elif entry["type"] == "label":
			menu.append(make_label(entry))
		elif entry["type"] == "pipe-menu":
			menu.append(make_DYNAMIC_pipemenu(entry))
	menu.connect("deactivate", gtk.main_quit)
	return menu

def check_entry(entry):
	#all pipe-menus and submenues must be named:
	if entry["type"] == "submenu" or entry["type"] == "pipe-menu":
		try:
			assert len(entry["label"]) > 0
		except (AssertionError, KeyError):
			print("[FATAL]: All submenu and pipe-menu entries must be named.")
			exit()
	#all pipe-menus must have a command
	if entry["type"] == "pipe-menu":
		try:
			assert len(entry["command"]) > 0
		except (AssertionError, KeyError):
			print("[FATAL]: All pipe-menus must have a command to execute")
			exit()
	#all label entries must have a label!
	if entry["type"] == "label":
		try:
			assert len(entry["label"]) > 0
		except (AssertionError, KeyError):
			print("[FATAL]: All labels must have a label field!")
			exit()

def parse_menu(file):
	lines=file.split("\n")
	entries=[]
	for line in lines:
		entry={}
		line = line.strip()
		RE_instruction=re.compile("\[(.*?)\]")
		RE_name=re.compile("\((.*?)\)")
		RE_command=re.compile("\{(.*)\}")
		
		type_result = RE_instruction.match(line)
		if type_result:
			type = type_result.group(1)
			line = line[len(type_result.group(0)):].strip()
			entry["type"]=type
			name_result = RE_name.match(line)
			if name_result:
				name = name_result.group(1)
				line = line[len(name_result.group(0)):].strip()
				entry["label"]=name
			
			command_result=RE_command.search(line)
			if command_result:
				command = command_result.group(1)
				entry["command"]=command
			
		if entry:
			check_entry(entry)
			entries.append(entry)
	return entries
		 
			
if __name__=="__main__":
	f=open(sys.argv[1],"r")
	menu_txt = f.read()
	entries = parse_menu(menu_txt)
	menu = makeMenu(entries)
	menu.show_all()
	menu.popup(None, None, None, 0, 0)
	gtk.main()
