

def set_session_var(request, **kwargs):
	for key, value in kwargs.items():
		if key == 'exam':
			request.session['exam'] = value
		if key == 'page':
			request.session['page'] = value
		
	
