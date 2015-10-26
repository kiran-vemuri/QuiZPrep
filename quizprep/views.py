#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pymysql.cursors
from pyramid.view import view_config
import json
import random

#!-- Methods

def db_connect():
    db_conn = pymysql.connect(host='localhost',
                                 user='root',
                                 password='toor',
                                 db='quizprep',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return db_conn

def nlp_talk(t_title, data):
    data = data.encode('utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', 9990))
    #data=""
    if data:
        s.send(str(data))
        t_data = data
        data = False
        qdata = s.recv(8192)
        qdata = qdata.encode('utf-8')
    s.send('exit')
    s.close()
    
    # Connect to the database
    db_conn = db_connect()
    try:
        with db_conn.cursor() as cursor:
            sql = "select distinct(`name`) from `topics`"
            cursor.execute(sql,())
            topic_res = cursor.fetchall()
        
        elem_pres = False
        for element in topic_res: 
            if t_title in element.values():
                elem_pres = True
        if elem_pres:
            with db_conn.cursor() as cursor:
                sql = "UPDATE topics SET `content`=%s,`questions`=%s WHERE `name`=%s"
                cursor.execute(sql,(t_data, qdata, t_title))
                db_conn.commit()
        else:
            with db_conn.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `topics` (`name`, `content`,`questions`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (t_title, t_data, qdata))
        
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db_conn.commit()
    finally:
        db_conn.close()
    
    return qdata




#!-- Views


@view_config(route_name='home', renderer='templates/quizprep.pt')
def my_view(request):
    return {'project': 'QuizPrep'}

@view_config(route_name='learn', renderer='templates/learn.pt')
def learn_view(request):
    return {'Question': 'Answer'}

@view_config(route_name='qparser', renderer='templates/trivia.pt')
def qparser(request):
    if request.method == "POST":
        in_text = request.params['in_text']
        topic_title = request.params['topic_title']
        ret_data = nlp_talk(topic_title,in_text)
    ret_data = json.loads(ret_data)
    final_dict = []
    for element in ret_data.keys():
        final_dict.append({'question':element, 'answer': ret_data[element]})
    return {'out_text': final_dict,'topic':topic_title}

@view_config(route_name='usertopics', renderer="templates/collections.pt")
def user_topics(request):
    db_conn = db_connect()
    try:
        with db_conn.cursor() as cursor:
            sql = "select distinct(`name`) from `topics`"
            cursor.execute(sql,())
            topic_res = cursor.fetchall()
        topic_list = []
        for element in topic_res:
            for value in element.values():
                topic_list.append(value)
    finally:
        db_conn.close()
    return {'usertopics':topic_list}

@view_config(route_name='usertrivia',renderer = 'templates/trivia.pt')
def user_trivia(request):
    topic_title = request.matchdict['topic']
    if topic_title != 'random':
        # Connect to the database
        db_conn = db_connect()
        try:
            with db_conn.cursor() as cursor:
                sql = "select `questions` from `topics` WHERE `name`=%s"
                cursor.execute(sql,(topic_title))
                topic_res = cursor.fetchone()
        finally:
            db_conn.close()
        topic_res = json.loads(topic_res['questions'])
        final_dict = []
        for element in topic_res.keys():
            final_dict.append({'question':element, 'answer': topic_res[element]})
    '''
    elif topic_title == 'random':
        db_conn = db_connect()
        try:
            with db_conn.cursor() as cursor:
                sql = "select `questions` from `topics`"
                cursor.execute(sql,(topic_title))
                topic_res = cursor.fetchall()
        finally:
            db_conn.close()
        qdict = []
        for element in topic_res:
            for value in element.values():
                qdict = qdict+list(json.loads(value))
        qdict = dict(qdict)
        final_dict = []
        for i in xrange(1,10):
            outkey = random.choice(q_dict.keys())
            final_dict.append({'question': outkey,'answer':qdict[outkey]})

    '''
    return {'out_text': final_dict,'topic':topic_title}





@view_config(route_name='pebbletopics', renderer='json')
def pebble_json(request):
    # Connect to the database
    db_conn = db_connect()
    try:
        with db_conn.cursor() as cursor:
            sql = "select distinct(`name`) from `topics`"
            cursor.execute(sql,())
            topic_res = cursor.fetchall()
        topic_list = []
        for element in topic_res:
            for value in element.values():
                topic_list.append(value)
    finally:
        db_conn.close()
    return {'pebbletopics':topic_list}

@view_config(route_name='pebbletrivia', renderer='json')
def pebble_trivia_json(request):
    topic_title = request.matchdict['topic']
     # Connect to the database
    db_conn = db_connect()
    try:
        with db_conn.cursor() as cursor:
            sql = "select `questions` from `topics` WHERE `name`=%s"
            cursor.execute(sql,(topic_title))
            topic_res = cursor.fetchone()
    finally:
        db_conn.close()
    
    q_dict = topic_res['questions']

    q_dict = json.loads(q_dict)
    outkey = random.choice(q_dict.keys())

    return {'question': outkey, 'answer':q_dict[outkey]}

@view_config(route_name='contact', renderer='templates/contact.pt')
def contact_json(request):
    return {'hello':'world'}
