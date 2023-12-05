# Parcial 2 Topicos en IA - Prediccion noticias ELDEBER 📰🗞️
### Pablo Alejandro Badani Zambrana - 55789

# Prediccion noticias ELDEBER - Descripcion: 

La aplicacion presente de noticias ELDEBER se especializa en saber que tan buena o mala es la noticia, que puede ayudar a la gente sensible o que solo busca noticias bonitas.

# Prediccion noticias ELDEBER 💭 - Funcionalidad:

Para poder utilizar localmente se debe hacer correr en la terminal el comando "docker-compose up", despues se tiene que ir al link proporcionado para irnos a la interfaz de fastAPI donde tendremos que poner la ruta "/docs" para poder ingresar a los diferentes endpoints, tambien se puede utilizar el siguiente link:
- https://parcial2tia--pablo-badani-zdvvhg27qq-uc.a.run.app/docs

# Endpoints
- /status .- Para ver informacion general de la aplicacion y modelo.
- /sentiment .- Para subir el link de la noticia y hacer su prediccion si la noticia es positiva, negativo o simplemente neutral.
- /analysis .- Para subir el link donde tendremos mas informacion donde tendremos diferentes caracteristicas como el tiempo de ejecucion, POS tagging, NER, Embedding y el rango de calificacion de cada palabra posible obtenida de la noticia.
- /reports .- Nos crea un registro .csv de informacion relevante de las noticias que fueron detectados donde nos mostrará el titulo del articulo, prediccion, fecha y hora, entre otros datos, cabe destacar que solo se puede usar despues de haber utilizado el /sentiment.

# Prediccion noticias ELDEBER 🥸 - Problemas:
No se pudo crear el endpoint /analysis_v2 y de que los links solo son compatibles con ELDEBER