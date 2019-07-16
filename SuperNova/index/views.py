# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
import os
#main
def index_views(request):
    return render(request, 'index.html')

# def upload_image(request,shell=True):
# 	obj = request.FILES.get('inputfile')
# 	filename=obj.name
# 	print(filename)
# 	file_path = os.path.join("static/upload", filename)
# 	f = open(file_path, 'wb')
# 	for chunk in obj.chunks():
# 		f.write(chunk)
# 	f.close()
# 	File.objects.create(file_name=filename,file_size=obj.size,file=file_path)
# 	return HttpResponseRedirect('/show')   
def upload_image(request,shell=True):
	obj = request.FILES.get('inputfile')
	filename=obj.name
	print(filename)
	file_path = os.path.join("static/upload", filename)
	f = open(file_path, 'wb')
	for chunk in obj.chunks():
		f.write(chunk)
	f.close()
	File.objects.create(file_name=filename,file_size=obj.size,file=file_path)
	return HttpResponseRedirect('/show')  
def show_image(request):
    files=File.objects.all().order_by('create_time').last()
    return render(request,'show.html',locals())

def dete1(request):
	import demo
	files=File.objects.all().order_by('create_time').last()
	a=files.file_name
	demo.test(a)
	return HttpResponseRedirect('/result')
def result(request):
	return render(request,'result.html')
def about_views(request):
	return render(request,'about.html')
def project_views(request):
	return render(request,'projects.html')
def single_views(request):
	return render(request,'singlepost.html')
def contact_views(request):
	return render(request,'contact.html')