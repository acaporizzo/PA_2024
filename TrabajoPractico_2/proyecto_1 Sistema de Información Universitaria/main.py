from modules.persona_facultativa import Estudiante

if __name__=="__main__":
    persona_1 = Estudiante("juan","perez","5489465")
    persona_1.nombre =" nombre nuevo"
    print(persona_1.nombre)


