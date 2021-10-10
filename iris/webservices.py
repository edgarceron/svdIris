import json
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from users.codelogic import check_fingerprint
from .models import UploadImage
from .serialziers import ImageSerializer


class ImageViewSet(ListAPIView):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = UploadImage.objects.create(image=file)
        image_relative = str(image.image)
        result = check_fingerprint.check_all_fingerprints(image_relative)
        return HttpResponse(
            json.dumps({
                **result,
                "route": str(image_relative)
            }), status=200)
