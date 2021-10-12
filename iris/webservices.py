import json
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from iris.codelogic import check_iris, optimization
from .models import UploadImage
from .serialziers import ImageSerializer


class ImageViewSet(ListAPIView):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = UploadImage.objects.create(image=file)
        image_relative = str(image.image)
        person, mindistance, eye = check_iris.compare_all_iris(image_relative)
        return HttpResponse(
            json.dumps({
                'min': str(mindistance),
                'person': person,
                'eye': eye,
                "route": str(image_relative)
            }), status=200)

class ImageViewSet2(ListAPIView):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = UploadImage.objects.create(image=file)
        image_relative = str(image.image)
        person, mindistance, eye = check_iris.optimized_compare_all_iris(image_relative)
        return HttpResponse(
            json.dumps({
                'min': str(mindistance),
                'person': person,
                'eye': eye,
                "route": str(image_relative)
            }), status=200)
