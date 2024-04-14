### Plantilla inicial de proyecto

El proyecto se trata de un juego de trivia de películas, y consta de:

---Una interfaz web, con sus rutas desarrolladas en "server.py". Cuenta con una página inicial "home.html", donde el usuario puede completar con sus datos en casilleros y así acceder a jugar la trivia de películas, a un listado de las posibles películas o a ver sus resultados históricos. 

-Si se decide jugar trivia se le redirecciona a "trivia.html" donde se inicia el juego, que consta de una frase al azar (sin repeticiones) y 3 opciones distintas de películas, de las cuales se debe seleccionar una y enviar ese resultado. "respuestas.html" contiene información sobre el juego: si se acertó o no, la calificación final, y la posibilidad de seguir jugando o de volver al inicio mediante un botón.

-Si se decide observar resultados históricos, "resultados.html" mostrará el nombre de usuario, calificación, fecha y hora correspondientes a las jugadas previas. Estos datos se almacenan en un archivo .txt (resultados_historicos.txt). Además, se le da la opción al usuario de ver los resultados gráficos (una gráfica lineal y otra circular), redirigiendolo a "graficas.html" mediante un botón. Allí, puede descargar las gráficas como pdf. 

-Finalmente, si decide acceder al listado de películas, se redirecciona a "listar_peliculas.html", donde se observan todas las películas en orden alfabético y enumeradas.

En cada pantalla hay botones que permiten volver a la página principal.
La página web fue personalizada añadiendo imágenes, centrando textos, coloreando los botones, etc.
