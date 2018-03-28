# -*- coding: utf-8 -*-
import MySQLdb
import time
import json
import os
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.stdin.encoding
print sys.stdout.encoding

def command(cmd):
	print cmd
	lines = os.popen(cmd).readlines()
	return ''.join(lines)

def get_mysql_conn(host, db, user, passwd):
	conn = None
	cursor = None
	try:
		conn = MySQLdb.connect(host=host, db=db, user=user, passwd=passwd, charset='utf8')
		print '[mysql]: mysql -u%s -h%s -p%s -D%s' % (user, host, passwd, db)
		cursor = conn.cursor()
	except Exception, e:
		print e
		conn = None
		cursor = None
	return conn, cursor

def close_mysal_conn(conn, cursor):
	if cursor:
		cursor.close()
	if conn:
		conn.close()
	conn = None
	cursor = None

def insert_ignore_topic(conn, cursor, date, story_id, title, cover, ga_prefix):
	sql = 'insert ignore into zhihu_topic set dt=%s,story_id=%s,title=%s,cover=%s,sort=%s'
	print date, story_id, title, cover, ga_prefix
	# cursor.execute(sql, (date, story_id, title, cover, ga_prefix, ))
	# conn.commit()

def get_latest_stories():
	res = command("curl --connect-timeout 10 -H 'Authorization: Bearer kx/28n6XTEWCV47tGELiCg' 'https://news-at.zhihu.com/api/7/stories/latest?client=0'")
	# print res
	json_obj = json.loads(res)
	date = json_obj.get('date')
	stories = json_obj.get('stories')
	res = []
	for story in stories:
		images = story.get('images')
		cover = images[0]
		story_id = story.get('id')
		ga_prefix = story.get('ga_prefix')
		title = story.get('title')
		res.append((date, story_id, title, cover, ga_prefix))
	return res

def main():
	story_data = get_latest_stories()
	conn, cursor = get_mysql_conn('localhost', 'zhuhaibus', 'root', '')
	for story in story_data:
		(date, story_id, title, cover, ga_prefix) = story
		insert_ignore_topic(conn, cursor, date, story_id, title, cover, ga_prefix)
	close_mysal_conn(conn, cursor)

if __name__ == '__main__':
	main()
