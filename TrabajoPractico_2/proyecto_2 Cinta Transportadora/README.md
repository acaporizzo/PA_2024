### Plantilla inicial de proyecto

El proyecto se trata de un juego de trivia de películas, y consta de dos instancias:

---Una interfaz por consola, donde se pueden realizar 5 acciones diferentes en "aplicacion1.py", llevadas a cabo mediante funciones definidas en el módulo "modulo1.py". Allí, el usuario puede participar y decidir entre sus opciones ingresando números. Puede mostrar una lista de películas, jugar una trivia las veces que desee, acceder a un historial del juego, borrarlo, y salir del programa.

---Una segunda instancia, la interfaz web, fue desarrollada en "server.py" y cuenta con una página inicial "home.html", donde el usuario puede completar con sus datos en casilleros y así acceder a jugar la trivia de películas, o a ver sus resultados históricos. Si se decide jugar trivia se le redirecciona a "trivia.html" donde se inicia el juego, que consta de una frase al azar (sin repeticiones) y 3 opciones distintas de películas, de las cuales se debe seleccionar una y enviar ese resultado. "respuestas.html" contiene información sobre el juego: si se acertó o no, la calificación final, y la posibilidad de seguir jugando o de volver al inicio mediante un botón. Si se decide observar resultados históricos, "resultados.html" mostrará el nombre de usuario, calificación, fecha y hora correspondientes a las jugadas previas. Estos datos se almacenan en un archivo .txt (resultados_historicos.txt). Finalmente, se regresa a la página inicial con un botón. 

La página web fue personalizada añadiendo imágenes, centrando textos, coloreando los botones, etc.