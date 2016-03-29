# -*- coding: utf-8 -*-
# python
import requests
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
from django.db.models import Q
# app
from musics.models import Music

class Musics(APIView):

    def get(self, request, format=None):
        try:
            page = int(self.request.GET['page'])
        except:
            page = 0
        startpage = page*10
        queryObj = Q()
        try:
            language = str(request.GET['language'])
            queryObj = queryObj & Q(language=language)
        except:
            pass
        try:
            style = request.GET['style']
            queryObj = queryObj & Q(style=style)
        except:
            pass
        try:
            theme = request.GET['theme']
            queryObj = queryObj & Q(theme=theme)
        except:
            pass
        try:
            order = request.GET['order']
        except:
            order = 0
        orderItem = ('time' if (order==0) else 'collects')
        musics = Music.objects.filter(queryObj).order_by(orderItem)[startpage:10]
        results = []
        for music in musics:
            result = {'id':music.id, 'name':music.name, 'language':music.language,
                    'style':music.style, 'theme':music.theme, 'collects':music.collects,
                    'album':music.album, 'singer':music.singer,
                    'comments':music.comments, 'time':music.time}
            results.append(result)
        response = Response(results)
        response["X-Total-Count"] = musics = Music.objects.filter(queryObj).count()
        response["Access-Control-Expose-Headers"] = "X-Total-Count"
        return response
