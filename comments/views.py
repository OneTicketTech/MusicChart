# -*- coding: utf-8 -*-
# python
import requests
import time
import datetime
#django-rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# django
from django.http import HttpResponse, HttpResponse
# app
from comments.models import Comment
from musics.models import Music
from setlists.models import Setlist
from utils.views import get_comment


# GET /musics/comments/{musicId}
# 获取某音乐的评论
# POST /musics/comments/{musicId}
# 评论音乐
class CommentMusic(APIView):

    def get(self,request,**kwargs):
        try:
            musicId = int(self.kwargs['musicId'])
        except:
            return HttpResponse(status=400)
        try:
            page = int(self.request.GET['page'])
        except:
            page = 0
        try:
            Music.objects.get(id=musicId)
        except:
            return HttpResponse(status=404)
        try:
            results = get_comment(musicId,0,page)
        except:
            return HttpResponse(status=404)
        return Response(results)

    @authentication_classes((TokenAuthentication,SessionAuthentication, BasicAuthentication))
    @permission_classes((IsAuthenticated,))
    def post(self,request,**kwargs):
        try:
            musicId = int(self.kwargs['musicId'])
        except:
            return HttpResponse(status=400)
        userId = self.request.user.id
        try:
            Music.objects.get(id=musicId)
        except:
            return HttpResponse(status=404)
        try:
            comment = request.data['comment']
        except:
            return HttpResponse(status=400)
        now = datetime.datetime.now()
        c = Comment.objects.create(user_id=userId,music_id=musicId,comment=comment,time=now)
        results = get_comment(musicId,0,0)
        return Response(results)


# GET /setlists/comments/{setlistId}
# 获取某歌单的评论
# POST /setlists/comments/{setlistId}
# 评论歌单
class CommentSetlist(APIView):

    def get(self,request,**kwargs):
        try:
            setlistId = int(self.kwargs['setlistId'])
        except:
            return HttpResponse(status=400)
        try:
            page = int(self.request.GET['page'])
        except:
            page = 0
        try:
            Setlist.objects.get(id=setlistId)
        except:
            return HttpResponse(status=404)
        try:
            results = get_comment(0,setlistId,page)
        except:
            return HttpResponse(status=404)
        return Response(results)

    @authentication_classes((TokenAuthentication,SessionAuthentication, BasicAuthentication))
    @permission_classes((IsAuthenticated,))
    def post(self,request,**kwargs):
        try:
            setlistId = int(self.kwargs['setlistId'])
        except:
            return HttpResponse(status=400)
        userId = self.request.user.id
        try:
            Setlist.objects.get(id=setlistId)
        except:
            return HttpResponse(status=404)
        try:
            comment = request.data['comment']
        except:
            return HttpResponse(status=400)
        now = datetime.datetime.now()
        c = Comment.objects.create(user_id=userId,setlist_id=setlistId,comment=comment,time=now)
        results = get_comment(0,setlistId,0)
        return Response(results)
