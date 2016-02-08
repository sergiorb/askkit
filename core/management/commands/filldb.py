#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import socket
import struct

from users.models import *
from questions.models import *

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from optparse import make_option

def gen_ip():
	return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))	


def gen_string(text_long=10, verbose=False):
	letters = ('a','b','c','d','e','f','g','h','i','j','k',
		'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
		'A','B','C','D','E','F','G','H','I','J','K',
		'L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
		'0','1','2','3','4','5','6','7','8','9',)
	string = ''

	for x in range(0, text_long):
		string += letters[random.randint(0, len(letters)-1)]

	return string

def gen_random_number(min_num=0, max_num=3):
		return random.randint(min_num, max_num)

def gen_users(num=5, verbose=False):

	user_list = []

	print "Generating "+str(num)+" users..."
	for x in range(0,num):
		try:
			user = User(username=gen_string())
			user.save()
			profile = Profile(user=user)
			profile.save()
			user_list.append(user)
			if verbose:
				print "Nº: "+str(x)+" OK."
		except Exception as e:
			print "Nº: "+str(x)+" fails."
			print e
	print "Done¡"
	return user_list


def gen_question(user_list, num=10, verbose=False):

	def get_random_user():
		return user_list[random.randint(0, len(user_list)-1)]


	question_list = []

	print "Generating "+str(num)+" question..."
	for x in range(0,num):
		try:
			question = Question(context=gen_string(text_long=300), question=gen_string(text_long=15), fromIp=gen_ip(), data_require_vote=False)

			if gen_random_number(max_num=4) != 1:
				question.context_on_home = False
			"""
			if gen_random_number() != 1:
				#question.asker = Profile.objects.get(user=get_random_user())
				question.asker = Profile.objects.get(user=None)			
			"""
			question.save()
			question_list.append(question)
			if verbose:
				print "Nº: "+str(x)+" OK."
		except Exception as e:
			print "Nº: "+str(x)+" fails."
			print e
		

	print "Done¡"

	return question_list


def gen_reply(question_list, num=25, verbose=False):

	def get_random_question():
		return question_list[random.randint(0, len(question_list)-1)]

	reply_list = []

	print "Generating "+str(num)+" replies..."
	for x in range(0,num):
		try:
			reply = Reply(question=get_random_question(), replyText=gen_string(text_long=gen_random_number(min_num=8, max_num=50)))
			reply.save()
			reply_list.append(reply)
			if verbose:
				print "Nº: "+str(x)+" OK."
		except Exception as e:
			print "Nº: "+str(x)+" fails."
			print e

	print "Done¡"

	return reply_list


def gen_comments(user_list, question_list, num=50, verbose=False):

	def get_random_user():
		return user_list[random.randint(0, len(user_list)-1)]

	def get_random_question():
		return question_list[random.randint(0, len(question_list)-1)]

	comment_list = []

	print "Generating "+str(num)+" comments..."
	for x in range(0, num):
		try:
			comment = Comment(commenter=Profile.objects.get(user=get_random_user()), question=get_random_question(), text=gen_string(text_long=150))
			comment.save()
			comment_list.append(comment)
			if verbose:
				print "Nº: "+str(x)+" OK."
		except Exception as e:
			print "Nº: "+str(x)+" fails."
			print e

	print "Done¡"

	return comment_list


def gen_votes(user_list, replies_list, num=50, verbose=False):

	def get_random_user():
		return user_list[random.randint(0, len(user_list)-1)]

	def get_random_reply():
		return replies_list[random.randint(0, len(replies_list)-1)]

	votes_list = []

	print "Generating "+str(num)+" votes..."
	for x in range(0, num):
		try:
			reply = get_random_reply()
			question = Question.objects.get(replies=reply)
			vote = ReplyVotedBy(reply=reply, fromIp=gen_ip(), question=question )
			if gen_random_number(max_num=5) != 1:
				vote.voter = Profile.objects.get(user=get_random_user())
			vote.save()
			votes_list.append(vote)
			reply.hits += 1
			question.votes += 1
			reply.save()
			question.save()
			if verbose:
				print "Nº: "+str(x)+" OK."
		except Exception as e:
			print "Nº: "+str(x)+" fails."
			print e

	print "Done¡"

	return votes_list

class Command(BaseCommand):

    def handle(self, *args, **options):

		users = gen_users(num=20, verbose=True)

		#users = User.objects.all()

		#questions = gen_question(user_list=None, num=1500000, verbose=True)

		questions = gen_question(user_list=users, num=150, verbose=True)

		replies = gen_reply(question_list=questions, num=500, verbose=True)

		votes = gen_votes(user_list=users, replies_list=replies, num=2000, verbose=True)

		comments = gen_comments(user_list=users, question_list=questions, num=900, verbose=True)
		