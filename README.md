# svdFingerPrint
Proyecto metodos numéricos 2021

Para ejecutar este proyecto es necesario contar con una instalación de docker.

Sino tiene docker instalado:

windows: Dirijase a https://www.docker.com/get-started para proceder a descargar docker desktop

Distribuciones de linux: https://docs.docker.com/engine/install/

El puerto 8020 debe estar disponible para cargar la aplicación.

Clone el repositorio:

```
git clone https://github.com/edgarceron/svdIris
```
Es necesario tener una herramienta de control de repositorios para realizar esta acción
Para hacerlo desde windows descargue: [Git bash](https://git-scm.com/downloads) 

Desde la terminal ejecute:

```
docker build --no-cache -t svdiris .
docker-compose up -d
docker exec -it svdiris-svdiris-1 python svdIris/manage.py migrate
docker exec -it svdiris-svdiris-1 python svdIris/manage.py import_iris /opt/app/datairis/MMU-Iris-Database
```

Desde el navegador dirijase a [http://localhost:8020/iris/check_iris](http://localhost:8020/iris/check_iris)

Seleccione un archivo formato bmp que tenga como dimesiones  (320, 240).

De click en subir archivo. El programa respondera entre 2 y 3 minutos con la verificación de la identidad.
Despues de la primera ejecución obtendra respuestas menos de 30 segundos. 

