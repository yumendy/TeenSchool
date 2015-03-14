from django.shortcuts import render, render_to_response
from models import *
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.urlresolvers import reverse


import datetime

# Create your views here.
def default(request):
	if request.user.is_authenticated():
		user = request.user
	else:
		user = None
	content = {
		'user' : user,
	}
	return render_to_response('default.html',content)

def login(request):
	next = request.GET.get('next','/')
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	state = ''
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username = username, password = password)
		if user:
			if user.is_active:
				auth.login(request,user)
				return HttpResponseRedirect(next)
			else:
				state = 'not_active'
		else:
			state = 'auth_error'
	content = {
		'state' : state,
	}
	return render_to_response('login.html', content, context_instance = RequestContext(request))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

@login_required
def addCourse(request):
	state = ''
	if request.POST:
		name = request.POST.get('name','')
		time = request.POST.get('time','')
		if name and time:
			format = "%Y-%m-%dT%H:%M:%S"
			course = Project(
				name = name,
				startTime = time,
				signinTime = time,
				signoutTime = datetime.datetime.strptime(time,format) + datetime.timedelta(hours = 2),
				)
			course.save()
			state = 'success'
		else:
			state = 'error'
	content = {
		'state' : state,
	}
	return render_to_response('addCourse.html', content, context_instance = RequestContext(request))

@login_required
def courseList(request):
	tbd_list = Project.objects.filter(startTime__gte = datetime.date.today())
	content = {
		'tbd_list' : tbd_list,
	}
	return render_to_response('courselist.html', content)

@login_required
def QRCode(request):
	courseId = request.GET.get('courseId','')
	typ = request.GET.get('typ','')
	if courseId and typ:
		try:
			course = Project.objects.get(pk = courseId)
		except:
			return HttpResponseRedirect('courselist/')
		else:
			if typ == '1':
				course.signinTime = datetime.datetime.now()
			elif typ == '2':
				course.signoutTime = datetime.datetime.now()
			course.save()
			url = 'http://' + request.META['HTTP_HOST'] + reverse('sign') + '?courseId=' + courseId +'%26typ=' + typ
			content = {
				'course' : course,
				'url' :url,
			}
			return render_to_response('QRCode.html', content)
	else:
		return HttpResponseRedirect('/courselist/')

def sign(request):
	state = ''
	content = {}
	courseId = request.GET.get('courseId','')
	typ = request.GET.get('typ','')
	try:
		course = Project.objects.get(pk = courseId)
	except:
		state = 'code_error'
	else:
		content['course'] = course
	if request.POST:
		num = request.POST.get('num','')
		name = request.POST.get('name','')
		ip = request.META['REMOTE_ADDR']
		records = Record.objects.filter(project = course)
		if (typ == '1') or (typ == '2'):
			records = records.filter(typ = int(typ))
			if records.filter(signIp = ip):
				state = 'device_error'
			elif records.filter(num = num) or records.filter(name = name):
				state = 'repetition_error'
			else:
				condition1 = (typ == '1') and ((datetime.datetime.now() - course.signinTime.replace(tzinfo=None) > datetime.timedelta(minutes = 15)) or (datetime.datetime.now() < course.signinTime.replace(tzinfo=None)))
				condition2 = (typ == '2') and ((datetime.datetime.now() - course.signoutTime.replace(tzinfo=None) > datetime.timedelta(minutes = 15)) or (datetime.datetime.now() < course.signoutTime.replace(tzinfo=None)))
				if condition1 or condition2:
					state = 'time_out'
				else:	
					record = Record(
						name = name,
						num = num,
						typ = int(typ),
						signIp = ip,
						project = course,
						signTime = datetime.datetime.now(),
						)
					record.save()
					state = 'success'
		else:
			state = 'code_error'
	content['state'] = state
	return render_to_response('sign.html', content, context_instance = RequestContext(request))

@login_required
def recordList(request):
	courseId = request.GET.get('courseId','')
	try:
		course = Project.objects.get(id = courseId)
	except:
		return HttpResponseRedirect('/courselist/')
	else:
		records = Record.objects.filter(project = course)
		startRecord = records.filter(typ = '1')
		endRecord = records.filter(typ = '2')
		content = {
			'course' : course,
			'startRecord' : startRecord,
			'endRecord' : endRecord,
		}
		return render_to_response('recordList.html', content)

@login_required
def finishList(request):
	courses = Project.objects.annotate(num_records = Count('record'))
	# finish_list = courses.filter(startTime__lt = datetime.date.today())
	finish_list = courses
	content = {
		'finish_list' : finish_list,
	}
	return render_to_response('finishList.html', content)