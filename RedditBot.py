#!/usr/bin/env python
import praw

"""
Reddit bot, gets posts from Reddit using praw
"""

class RedditBot(object):
	def __init__(self, subred, post_type, check_subred=False):
		self.subred = subred
		self.post_type = post_type
		self.check_subred = check_subred
		self.reddit = praw.Reddit(user_agent="QuickReddit")
		self.get_posts()

	def get_posts(self):
		try:
			#gets posts from current subreddit, either new, hot or top
			if self.post_type == "new":
				posts = self.reddit.get_subreddit(self.subred).get_new(limit=15)

			elif self.post_type == "hot":
				posts = self.reddit.get_subreddit(self.subred).get_hot(limit=15)

			elif self.post_type == "top":
				posts = self.reddit.get_subreddit(self.subred).get_top(limit=15)

			else:
				posts = self.reddit.get_subreddit(self.subred).get_hot(limit=15)

			#lists contain information about the posts
			titles = []
			links = []
			scores = []

			for i in posts:
				#gets info for posts
				titles.append(i.title)
				links.append(i.short_link)
				scores.append(i.score)

			if self.check_subred:
				return len(titles) == 15

			else:
				current_posts = [titles, links, scores]
				return current_posts

		except Exception:
			return False