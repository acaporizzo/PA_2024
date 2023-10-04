def calcular_aw_promedio(self, p_clase, cajon):
    total_aw = 0.0
    contador = 0

    for alimento in cajon:
        if isinstance(alimento,p_clase):
            total_aw += self.calcular_aw()
            contador += 1

    if contador == 0:
        return 0.0
    else:
        return (total_aw/contador)
        