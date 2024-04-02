En esta carpeta deben guardarse todos los archivos, ya sean de texto, csv, JSON, etc. de los cuales se obtengan datos utilizados en el proyecto, así como los archivos que contengan resultados del mismo o que sirvan para almacenar información.

No se guardan en esta carpeta los archivos de bases de datos.

png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)
    # Codificar la imagen PNG a cadena de texto base64
    png_image_b64_string = "data:image/png;base64,"
    png_image_b64_string += base64.b64encode(png_image.getvalue()).decode('utf8')

    return (png_image_b64_string) 

