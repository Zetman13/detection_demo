from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.conf import settings

import json
import os
import uuid

from .detection import detect_image


class IndexView(TemplateView):
    template_name = 'detection/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_images'] = [
            'test_image_1',
            'test_image_2',
            'test_image_3',
            'test_image_4',
        ]
        return context


class DetectPreloadedView(View):
    def post(self, request):
        data = json.loads(request.body)
        img_name = data['img_name']
        detect_image(img_name=img_name)
        return JsonResponse(data={'result': 'success'})


class DetectUploadedView(View):
    def post(self, request):
        img_file = request.FILES['0']
        img_filename = str(uuid.uuid4().hex)
        img_path = os.path.join(settings.BASE_DIR, f"static/detection_demo/raw_images/{img_filename}.png")
        with open(img_path, "wb+") as destination:
            for chunk in img_file.chunks():
                destination.write(chunk)

        detect_image(img_name=img_filename)
        return JsonResponse(data={"result": "success", "img_name": img_filename})
