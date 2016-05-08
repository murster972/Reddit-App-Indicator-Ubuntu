#!/usr/bin/env python
from subreddit_info import *
from ErrorUI import ErrorUI
from RedditBot import RedditBot
import gtk
import appindicator
import os
import sys
import webbrowser
import urllib2

"""
A Reddit Application Indicator for Ubuntu
"""

class QuickReddit(object):
	def __init__(self):
		#setup application indicator
		app_ind = appindicator.Indicator("QuickReddit", "indicator", appindicator.CATEGORY_APPLICATION_STATUS)
		app_ind.set_status(appindicator.STATUS_ACTIVE)
		app_ind_icon = os.getcwd() + "/reddit_icon.png"
		app_ind.set_attention_icon(app_ind_icon)
		#app_ind.set_icon(app_ind_icon)

		#current subreddit and post type
		subred_info = subreddit_info()

		if len(subred_info) == 2:
			self.cur_subred = subred_info[0]
			self.post_type = subred_info[1]

		else:
			ErrorUI("invalid_subred")
			sys.exit()

		#stops error at startup when clearing current posts
		self.startup = True

		#menu items
		#permanent items
		self.perm_items = [x for x in range(5)]
		perm_item_names = ["Refresh", "Change Subreddit...", "Exit...", "Subreddit: ", "Posts Type: "]
		
		#items to hold posts
		self.post_items = [x for x in range(15)]

		#application indicator menu
		self.app_ind_menu = gtk.Menu()

		#perm items 4: Subreddit name and 5: Post Type
		self.perm_items[3] = gtk.MenuItem(perm_item_names[3])
		self.perm_items[3].set_sensitive(False)
		self.perm_items[3].show()

		self.perm_items[4] = gtk.MenuItem(perm_item_names[4])
		self.perm_items[4].connect("activate", self.set_post_type)
		self.perm_items[4].show()

		self.app_ind_menu.append(self.perm_items[3])
		self.app_ind_menu.append(self.perm_items[4])

		#perm items 1 - 3, refresh, change subreddit and sys.exit
		for i in range(3):
			self.perm_items[i] = gtk.MenuItem(perm_item_names[i])
			item_funct = perm_item_names[i]
			self.perm_items[i].connect("activate", self.menu_active, item_funct)
			self.perm_items[i].show()
			self.app_ind_menu.append(self.perm_items[i])

		#item seperator between perm. items and post items
		item_seper = gtk.SeparatorMenuItem()
		item_seper.show()
		self.app_ind_menu.append(item_seper)

		self.check_connection()
		self.new_posts()

		app_ind.set_menu(self.app_ind_menu)
		gtk.main()

	def menu_active(self, widget, data):
		#checks connection then calls approriate function function when menu item is clicked
		self.check_connection()

		if data == "Refresh":
			self.new_posts()

		elif data == "Change Subreddit...":
			self.ChangeSubredditUI()

		else:
			gtk.main_quit()

	def new_posts(self):
		#handles new posts
		self.set_subreddit_info()
		self.get_new_posts()
		self.clear_posts()
		self.refresh_posts()

	def set_subreddit_info(self):
		#set current subreddit info
		self.perm_items[3].get_child().set_text("/r/" + self.cur_subred)
		self.perm_items[4].get_child().set_text("Post Type: " + self.post_type)

	def set_post_type(self, widget):
		#sets current posts type
		self.check_connection()

		if self.post_type == "new":
			self.post_type = "hot"

		elif self.post_type == "hot":
			self.post_type = "top"

		elif self.post_type == "top":
			self.post_type = "new"

		else:
			ErrorUI("invalid_subred")
			sys.exit()

		self.new_posts()
		new_subreddit_info(self.cur_subred, self.post_type)

	def get_new_posts(self):
		#gets new posts
		r_bot = RedditBot(self.cur_subred, self.post_type)
		posts = r_bot.get_posts()

		#invalid subreddit or post type
		if not posts:
			ErrorUI("invalid_subred")
			sys.exit()

		else:
			#sorts post info into lists
			self.titles = posts[0]
			self.links = posts[1]
			self.scores = posts[2]

	def clear_posts(self):
		#clears current posts
		for i in self.post_items:
			if not self.startup:
				i.hide()

	def refresh_posts(self):
		#updates posts
		self.startup  = False

		for i in range(15):
			post_title = self.titles[i]

			#ensures length of title is no longer than 60
			if len(post_title) > 60:
				post_title = post_title[:57] + "..."

			#updates posts item with new post
			post_title = "[%s] %s" % (self.scores[i], post_title)
			self.post_items[i] = gtk.MenuItem(post_title)
			self.post_items[i].connect("activate", self.open_post, self.links[i])
			self.post_items[i].show()
			self.app_ind_menu.append(self.post_items[i])

	def open_post(self, widget, data):
		#opens post
		webbrowser.open(data)

	def ChangeSubredditUI(self):
		#UI for changing subreddit
		#creates window
		self.root = gtk.Window()
		self.root.set_title("Change Subreddit")
		self.root.set_icon_from_file(os.getcwd() + "/reddit_icon.png")
		self.root.set_size_request(350, 80)
		self.root.set_resizable(False)
		self.root.set_position(gtk.WIN_POS_MOUSE)
		self.root.set_keep_above(True)
		self.root.connect("delete-event", lambda e1, e2: self.root.destroy())

		self.new_subreddit = ""

		#layout management
		fixed_layout = gtk.Fixed()

		#creates input and adds to UI
		self.subred_input = gtk.Entry()
		self.subred_input.set_size_request(330, 25)
		self.subred_input.connect("key-release-event", self.new_subred_entered)
		self.subred_input.connect("key-press-event", lambda e1, e2: self.check_new_subred(e2) if e2.keyval == 65293 else False)
		fixed_layout.put(self.subred_input, 10, 10)

		#creates button and adds to UI
		self.new_subred_button = gtk.Button("Change")
		self.new_subred_button.set_size_request(150, 30)
		self.new_subred_button.connect("clicked", self.check_new_subred)
		fixed_layout.put(self.new_subred_button, 100, 40)

		self.root.add(fixed_layout)
		self.root.show_all()

	def new_subred_entered(self, widget, event):
		self.new_subreddit = widget.get_text()

	def check_new_subred(self, widget):
		#checks if new subreddit entered is valid
		r_bot = RedditBot(self.new_subreddit, self.post_type, True)
		check_subred = r_bot.get_posts()

		#changes new_subred_button font color to white
		label = self.new_subred_button.get_child()
		label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFF"))

		#if new subreddit is valid, updates subreddit info closes window and loads new posts
		if check_subred:
			new_subreddit_info(self.new_subreddit, self.post_type)
			self.cur_subred = self.new_subreddit
			self.root.destroy()
			self.new_posts()

		#if new_subreddit is not valid, changes new_subred_button to red
		else:
			self.new_subred_button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#D03E3E"))

	def check_connection(self):
		#checks for a valid internet connection
		try:
			connect = urllib2.urlopen("http://reddit.com")

		except urllib2.URLError:
			ErrorUI("no_connection")
			sys.exit()

if __name__ == '__main__':
	QuickReddit()