#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
#import pymysql.cursors
from pyramid.view import view_config
import json

#!-- Methods

def nlp_talk(t_title, data):
    data = data.encode('utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', 9990))
    #print s.recv(1024)
    #for data in ['lisi', 'zhangsan', 'wangwu']:
    #data=""
    if data:
        s.send(str(data))
        t_data = data
        data = False
        qdata = s.recv(8192)
    s.send('exit')
    s.close()
    '''
    # Connect to the database
    db_conn = pymysql.connect(host='localhost',
                                 user='root',
                                 password='toor',
                                 db='quizprep',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with db_conn.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `topics` (`name`, `content`) VALUES (%s, %s)"
            cursor.execute(sql, (t_title, t_data))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db_conn.commit()
        with db_conn.cursor() as cursor:
            sql = "INSERT INTO `trivia` (`topic_name`,`question`,`answer`) VALUES (%s, %s, %s)"
            qdict = json.loads(qdata)
            for element in qdict:
                cursor.execute(sql, (t_title,element,qdict[element]))
        db_conn.commit()
    finally:
        db_conn.close()
    '''
    
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
    return {'out_text': ret_data}

@view_config(route_name='pebbletopics', renderer='json')
def pebble_json(request):
    return {'pebbletopics':['Hello!','Lincoln', 'Washington', 'Obama']}
