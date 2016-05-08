#!/usr/bin/env python
from subreddit_info import invalid_file
import gtk
import os
import urllib2

"""
Custom Error UI
"""

class ErrorUI(object):
	def __init__(self, error):
		#window
		self.root = gtk.Window()
		self.root.set_title("An error has occured")
		self.root.set_icon_from_file(os.getcwd() + "/reddit_icon.png")
		self.root.set_size_request(400, 180)
		self.root.set_resizable(False)
		self.root.set_position(gtk.WIN_POS_MOUSE)
		self.root.set_keep_above(True)
		self.root.connect("delete-event", lambda e1, e2: gtk.main_quit())

		self.fixed_layout = gtk.Fixed()

		#error icon
		error_icon = gtk.Image()
		error_icon.set_size_request(150, 150)
		error_icon.set_from_file(os.getcwd() + "/reddit_error_icon.png")
		self.fixed_layout.put(error_icon, 5, 0)

		#calls certain ErrorUI
		if error == "no_connection":
			self.no_connection()

		elif error == "invalid_subred":
			self.invalid_subred()

		self.root.add(self.fixed_layout)
		self.root.show_all()
		gtk.main()

	def no_connection(self):
		#UI for no connection error
		error_msg = gtk.Label("Can't connect to Reddit, please\ncheck your connection and\ntry again.")
		self.fixed_layout.put(error_msg, 170, 50)

		#buttons for no connection error
		self.try_again_butn = gtk.Button("Try Again")
		self.try_again_butn.set_size_request(100, 30)
		self.try_again_butn.connect("clicked", self.no_connection_try_again)
		self.fixed_layout.put(self.try_again_butn, 170, 130)

		exit_butn = gtk.Button("Exit")
		exit_butn.set_size_request(100, 30)
		exit_butn.connect("clicked", lambda e1: gtk.main_quit())
		self.fixed_layout.put(exit_butn, 270, 130)

	def invalid_subred(self):
		#UI for invalid subreddit error
		invalid_file()
		error_msg = gtk.Label("Subreddit and post type have\nbeen reset, please restart\nQuickReddit.")
		self.fixed_layout.put(error_msg, 170, 50)

		#buttons for invalid subreddit error
		exit_butn = gtk.Button("Exit")
		exit_butn.set_size_request(100, 30)
		exit_butn.connect("clicked", lambda e1: gtk.main_quit())
		self.fixed_layout.put(exit_butn, 170, 130)

	def check_connection(self):
		#checks for a valid internet connection
		try:
			connect = urllib2.urlopen("http://reddit.com")
			return True

		except urllib2.URLError:
			return False

	def no_connection_try_again(self, widget):
		if self.check_connection():
			self.root.destroy()

		else:
			#change fg and bg colour
			label = self.try_again_butn.get_child()
			label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFF"))

			self.try_again_butn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#D03E3E"))