#!/usr/bin/env python

"""
Reads and writes Subreddit info and also corrects an invalid 'subreddit.txt'
"""

def subreddit_info(error=False):
	#gets subreddit info and resets if error is true
	if error:
		invadlid_file()

	try:
		#open subreddit file
		cur_subred_file = open("subreddit.txt", "r").readlines()
		subreddit_info = []

		#gets subreddit info from file
		for i in cur_subred_file:
			for j in i.split():
				if j != "subreddit:" and j != "post" and j != "type:":
					subreddit_info.append(j)

		#checks if subreddit info contains subreddit and post type
		if len(subreddit_info) != 2:
			subreddit_info = invadlid_file()

		return subreddit_info

	except Exception:
		invalid_file()

def invalid_file():
	#resets current subreddit and post type
	cur_subred_file = open("subreddit.txt", "w")
	cur_subred_file.write("subreddit: all\npost type: new")
	cur_subred_file.close()
	return ["all", "new"]

def new_subreddit_info(subred, pos_type):
	#sets new subreddit info
	cur_subred_file = open("subreddit.txt", "w")
	cur_subred_file.write("subreddit: %s\npost type: %s" % (subred, pos_type))
	cur_subred_file.close()