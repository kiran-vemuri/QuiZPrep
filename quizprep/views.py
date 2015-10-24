#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from pyramid.view import view_config

#!-- Methods

def nlp_talk(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', 9990))
    #print s.recv(1024)
    #for data in ['lisi', 'zhangsan', 'wangwu']:
    #data=""
    if data:
        s.send(str(data))
        data = False
        qdata = s.recv(8192)
    s.send('exit')
    s.close()
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
        ret_data = nlp_talk(in_text)
    return {'out_text': ret_data}


