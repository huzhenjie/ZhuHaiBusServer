# -*- coding: utf-8 -*-
import MySQLdb
import time
import datetime
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

def insert_ignore_topic(conn, cursor, date, story_id, title, cover, ts, detail):
	sql = 'select count(1) as total from news where origin_id=%s and title=%s'
	cursor.execute(sql, (story_id, title, ))
	exists = cursor.fetchone()[0] > 0
	if exists:
		return
	sql = "insert ignore into news set dt=%s, pt='知乎日报', origin_id=%s, title=%s, cover=%s, news_ts=%s, detail=%s"
	cursor.execute(sql, (date, story_id, title, cover, ts, detail, ))
	conn.commit()

def topic_exist(conn, cursor, story_id, title):
	sql = 'select count(1) as total from news where origin_id=%s and title=%s'
	cursor.execute(sql, (story_id, title, ))
	return cursor.fetchone()[0] > 0

def get_detail(story_id):
	res = command("curl --connect-timeout 10 'https://news-at.zhihu.com/api/7/story/%s'" % story_id)
	json_obj = json.loads(res)
	body = json_obj.get('body')
	cover = json_obj.get('image')
	return (body, cover)

def get_stories(conn, cursor, stories_list=[], dt=None):
	if not stories_list:
		stories_list = []
	cmd = "curl --connect-timeout 10 -H 'Authorization: Bearer kx/28n6XTEWCV47tGELiCg' 'https://news-at.zhihu.com/api/7/stories/latest?client=0'"
	if dt:
		cmd = "curl --connect-timeout 10 -H 'Authorization: Bearer kx/28n6XTEWCV47tGELiCg' 'https://news-at.zhihu.com/api/7/stories/before/" + dt + "?client=0'"
	res = command(cmd)
	json_obj = json.loads(res)
	date = json_obj.get('date')
	news_ts = '%.0f000' % (time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple()))
	stories = json_obj.get('stories')
	for story in stories:
		images = story.get('images')
		thumbnail = images[0]
		story_id = story.get('id')
		title = story.get('title')
		if topic_exist(conn, cursor, story_id, title):
			continue
		ga_prefix = story.get('ga_prefix')
		(body, cover) = get_detail(story_id)
		stories_list.append((date, story_id, title, cover, news_ts, body))
	day_7_ago = int(time.strftime('%Y%m%d', time.localtime(time.time()-3600*24*7)))
	if len(stories_list) > 100 or day_7_ago > int(date):
		return stories_list
	return get_stories(conn, cursor, stories_list, date)

def main():
	conn, cursor = get_mysql_conn('localhost', 'zhuhaibus', 'root', '')
	story_data = get_stories(conn, cursor)
	story_data.reverse()
	for story in story_data:
		(date, story_id, title, cover, news_ts, body) = story
		insert_ignore_topic(conn, cursor, date, story_id, title, cover, news_ts, body)
	close_mysal_conn(conn, cursor)

if __name__ == '__main__':
	main()
