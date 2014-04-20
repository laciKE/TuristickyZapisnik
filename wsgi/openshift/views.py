from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import messages

def home(request):
	context = RequestContext(request)

	return render_to_response('home/home.html', {}, context)
