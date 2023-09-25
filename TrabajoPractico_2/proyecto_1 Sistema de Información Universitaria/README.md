### Plantilla general del proyecto

En el Proyecto 1 del Trabajo Práctico 2 nos enfocamos en elaborar un diseño de relaciones estructurales para un Sistema de Información Universitaria. Para ello, utilizando herramientas de Programación Orientada a Objetos, determinamos relaciones de:

--Herencia: entre Persona_Facultativa como clase madre, y sus clases hijas, Estudiante y Profesor.
--Composición: entre Departamento y Facultad, indicando que no puede crearse un departamento sin una facultad.
--Agregación: entre Facultad y Estudiante, determinando que facultad contiene objetos de la claase Estudiante, estudiantes.
--Asociación: 
----entre Departamento y Profesor: dos relaciones, una que determina los profesores de ese departamento, y otra que relaciona a un profesor como director de ese departamento.
----entre Profesor y Curso: determina los cursos en los que enseña un profesor, y los profesores de un curso.
----entre Estudiante y Curso: determina los cursos a los que asiste un estudiante, y los estudiantes en un curso.
----entre Departamento y Curso: determina los cursos que pertenecen a un departamento, y el departamento al que pertenece un curso. 

Para establecer dichas relaciones, empleamos los métodos y atributos necesarios para definir las acciones que puede llevar a cabo cada clase. Todo esto está expresado en un gráfico UML, en la carpeta static.