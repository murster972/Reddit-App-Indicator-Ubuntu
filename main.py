#!/usr/bin/env python
import os
import appindicator
import gtk

def main():
	app_ind = appindicator.Indicator("QuickReddit", "indicator", appindicator.CATEGORY_APPLICATION_STATUS)
	app_ind.set_status(appindicator.STATUS_ACTIVE)
	app_ind_icon = os.getcwd() + "/reddit_icon.png"
	app_ind.set_attention_icon(app_ind_icon)
	app_ind.set_icon(app_ind_icon)

if __name__ == '__main__':
	main()