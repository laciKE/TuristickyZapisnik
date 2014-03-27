from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import messages

def index(request):
	context = RequestContext(request)
	return render_to_response('base.html',{}, context)

def home(request):
	context = RequestContext(request)
	messages.info(request, 'Test info message, click to hide.')
	messages.success(request, 'Test success message, click to hide.')
	messages.error(request, 'Test error message, click to hide.')


	return render_to_response('home/home.html', {}, context)
