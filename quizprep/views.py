#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from pyramid.view import view_config

#!-- Methods

#def nlp_talk(data):
def nlp_talk():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', 9990))
    #print s.recv(1024)
    #for data in ['lisi', 'zhangsan', 'wangwu']:
    data="""
George Washington (February 22, 1732 [O.S. February 11, 1731][Note 1][Note 2] – December 14, 1799) was the first President of the United States (1789–97), the Commander-in-Chief of the Continental Army during the American Revolutionary War, and one of the Founding Fathers of the United States. He presided over the convention that drafted the current United States Constitution and during his lifetime was called the "father of his country".[4]

Widely admired for his strong leadership qualities, Washington was unanimously elected President in the first two national elections. He oversaw the creation of a strong, well-financed national government that maintained neutrality in the French Revolutionary Wars, suppressed the Whiskey Rebellion, and won acceptance among Americans of all types.[5] Washington's incumbency established many precedents, still in use today, such as the cabinet system, the inaugural address, and the title Mr. President.[6][7] His retirement from office after two terms established a tradition that lasted until 1940, when Franklin Delano Roosevelt won an unprecedented third term.

Born into the provincial gentry of Colonial Virginia, his family were wealthy planters who owned tobacco plantations and slaves which he inherited; he owned hundreds of slaves throughout his lifetime, but his views on slavery evolved. In his youth he became a senior British officer in the colonial militia during the first stages of the French and Indian War. In 1775, the Second Continental Congress commissioned Washington as commander-in-chief of the Continental Army in the American Revolution. In that command, Washington forced the British out of Boston in 1776, but was defeated and nearly captured later that year when he lost New York City. After crossing the Delaware River in the middle of winter, he defeated the British in two battles, retook New Jersey and restored momentum to the Patriot cause. This is known as the Battle of Trenton.
"""
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
        #ret_data = nlp_talk(in_text)
        ret_data = nlp_talk()
    return {'out_text': ret_data}


