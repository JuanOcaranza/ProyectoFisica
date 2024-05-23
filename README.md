 # Proyecto Física
 En este proyecto analizamos videos del ejercicio curl de bicep y utilizamos lo aprendido en física para determinar la cantidad de calorías consumidas.
 
 ## Instalación
 - Clonar o descargar proyecto
 - Utilizar pip para instalar las librerías mencionadas en [requirements.txt](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/requirements.txt)

 ## Ejecución
 Hay dos opciones ejecutar [main.py](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/main.py) o ejecutar [main_no_track.py](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/main_no_track.py):

 - Con [main.py](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/main.py) se realiza el trackeo y luego se muestran los gráficos y el consumo de calorías, realizar el trackeo lleva tiempo, especialmente si no se dispone de tarjeta gráfica.
 - Para una ejecución rápida se recomienda utilizar [main_no_track.py](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/main_no_track.py), en este caso en vez de tracker se utilizan los valores de trackeo almacenados en la carpeta [keypoints](https://github.com/JuanOcaranza/ProyectoFisica/tree/main/keypoints) para esto debe estar almacenado el arhivo correspondiente al video, si no está se puede calcular y almacenar ejecutando [save_keypoints.py](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/save_keypoints.py).

Si no se desea calcular las calorías sino ver cómo se realiza el trackeo se puede ejecutar [tracker.py](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/tracker.py).

En todos los casos el nombre del video está hardcodeado.

## Controles de video
- **q**: cerrar.
- **p**: pausar/reanudar.
- **a**: retroceder un frame.
- **d**: avanzar un frame.
- **r**: reiniciar.

## Gráficos
Se puede acceder a los gráficos sin necesidad de ejecutar nada abriendo el archivo correspondiente al video en la carpeta [graphs](https://github.com/JuanOcaranza/ProyectoFisica/tree/main/graphs).

## Documentación
Para enter cómo funciona se puede ver los notebooks:
- [adapter_notebook.ipynb](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/adapter_notebook.ipynb)
- [data_notebook.ipynb](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/data_notebook.ipynb)
- [forces_notebook.ipynb](https://github.com/JuanOcaranza/ProyectoFisica/blob/main/forces_notebook.ipynb)
