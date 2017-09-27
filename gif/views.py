# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from moviepy.editor import *
from pytube import YouTube

from YoutubeToGIF import settings

@method_decorator(csrf_exempt, name='dispatch')
class ConvertGIF(View):
    def get(self, request):
        return render(request, 'gif/gif.html')

    def post(self, request):
        videoURL = request.POST.get('url')
        start = request.POST.get('start')
        end = request.POST.get('end')
        if videoURL is not None and start is not None and end is not None:
            try:
                if (int(end) - int(start)) > 10:
                    return HttpResponse(status=400)
            except:
                return HttpResponse(status=400)
            try:
                yt = YouTube(videoURL)
                print('ConverGIF - get video')
                yt.set_filename('video')
                print('ConverGIF - set filename')
                yt.filter('mp4')[-1].download('{}/youtube_video/'.format(settings.MEDIA_ROOT))
                print('ConverGIF - download')
            except:
                return HttpResponse(status=404)
            try:
                video = VideoFileClip('{}/youtube_video/video.mp4'.format(settings.MEDIA_ROOT)).subclip(int(start), int(end))
                video.write_videofile('{}/youtube_gif/gif.gif'.format(settings.MEDIA_ROOT), fps=25, codec='gif')
                os.remove('{}/youtube_video/video.mp4'.format(settings.MEDIA_ROOT))
            except:
                return HttpResponse(status=416)
        else:
            return HttpResponse(status=400)
        gifURL = '{}/youtube_gif/gif.gif'.format(settings.MEDIA_ROOT)
        return JsonResponse({'url': gifURL})