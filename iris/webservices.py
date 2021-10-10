import json
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from iris.codelogic import check_iris
from .models import UploadImage
from .serialziers import ImageSerializer


class ImageViewSet(ListAPIView):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = UploadImage.objects.create(image=file)
        image_relative = str(image.image)
        min, person = check_iris.compare_all_iris(image_relative)
        return HttpResponse(
            json.dumps({
                'min': min,
                'min': person,
                "route": str(image_relative)
            }), status=200)
