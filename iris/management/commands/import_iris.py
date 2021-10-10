import os
from django.core.management.base import BaseCommand
from users.models import Irises, Config
from users.codelogic import utils
from django.conf import settings


def check_iris(name):
    try:
        Irises.objects.get(name=name)
        return False
    except Irises.DoesNotExist:
        return True

class Command(BaseCommand):
    help = 'Carga los iris desde la carpeta especificada'

    def add_arguments(self, parser):
        parser.add_argument('ruta', type=str, help='Ruta de la carpeta')

    def handle(self, *args, **kwargs):
        ruta = kwargs['ruta']
        list_subfolders = [ f.path for f in os.scandir(ruta) if f.is_dir()]
        for subfolder in list_subfolders:
            dirname = os.path.basename(subfolder)
            if Command.check_iris(dirname):
                iris = Irises()
                iris.name = dirname
                left_path = os.path.join(subfolder, 'left')
                right_path = os.path.join(subfolder, 'right')
                left_files = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(left_path, f))]
                right_files = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(right_path, f))]

                array_images_left = []
                for i in range(len(left_files)):
                    image = utils.get_array_image(settings.MEDIA_ROOT, left_files[i]).tolist()
                    array_images_left.append(image)
                
                iris.left = array_images_left

                array_images_right = []
                for i in range(len(right_files)):
                    image = utils.get_array_image(settings.MEDIA_ROOT, right_files[i]).tolist()
                    array_images_right.append(image)
                
                iris.right = array_images_right
                iris.save()
                print("Created Iris {}".format(dirname))


                
                

    