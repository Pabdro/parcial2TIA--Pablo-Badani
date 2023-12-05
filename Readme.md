# Parcial 2 Topicos en IA - Prediccion noticias ELDEBER
### Pablo Alejandro Badani Zambrana - 55789

# Prediccion noticias ELDEBER - Descripcion: 
La aplicacion presente de noticias ELDEBER se especializa en saber que tan buena o mala es la noticia, que puede ayudar a la gente sensible o que solo busca noticias bonitas.

# Prediccion noticias ELDEBER - Funcionalidad:
Para poder utilizarla se debe hacer correr el archivo app.py, despues se tiene que ir al link proporcionado para irnos a la interfaz de fastAPI donde tendremos que poner la ruta "/docs" para poder ingresar a los diferentes endpoint:
- /status .- Para ver informacion general de la aplicacion y modelo.
- /sentiment .- Para subir el link.
- /analysis .- Para mostrar diferentes caracteristicas de los alumnos como la deteccion de ojos, boca y nariz.
- /reports .- Nos crea un registro .csv de los alumnos que fueron detectados donde nos mostrará el nombre respectivo del que se le sacó la foto, fecha y hora, entre otros datos, cabe destacar que solo se puede usar despues de haber utilizado el /annotate 

# Prediccion noticias ELDEBER - Problemas:
No se pudo fusionar los endpoints /annotate y /faces para una deteccion mas completa por lo que estan aparte para evitar bugs y por ultimo el modelo entrenado tiene problemas al detectar a Dylan confundiendolo con Gabriel posiblemente por falta de datos.