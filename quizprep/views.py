from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/quizprep.pt')
def my_view(request):
    return {'project': 'QuizPrep'}

@view_config(route_name='learn', renderer='templates/learn.pt')
def learn_view(request):
    return {'Question': 'Answer'}
