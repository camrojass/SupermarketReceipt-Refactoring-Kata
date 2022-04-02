# Proyecto Curso: SupermarketReceipt Refactoring - Deuda en Arquitectura


## Requisitos 

* Repositorio (puede ser en [github](https://github.com/))
* Proyecto público en [Azure DevOps](https://dev.azure.com/)**
* Cuenta en Sonarcloud [SonarCloud](https://sonarcloud.io/)

** Debido que para poder ser analizado a través de SonarCloud, solicita que el proyecto esté como público. Implica que se deba pedir el permiso "_parallelism_"

## Instalación de SonarCloud en Azure

Con el proyecto como publico, realizar los siguientes pasos a continuación
1. Ingresar a SonarCloud, sino tiene cuenta creada, puede crear su cuenta a través de la cuenta de Azure DevOps
2. Instale la extensión Sonarcloud a través de [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarcloud)
3. Agregar el Endpoind del servicio de SonarCloud en Azure
  * Ir a la configuración del proyecto a la opción Connexciones de servicio
  * Agregar la conexión de servicio tupo SonarCloud
  * Usar el token propuesto por SonarCloud
  * Hacer clic en verificar
4. Configurar el pipeline de Azure de acuerdo al lenguaje de desarrollo del proyecto. (En el caso del proyecto se encuentra en python)
   * Preparar la configuración del análisis
   1. Seleccionar el endpoint de SonarCloud
   2. Seleccionar la organización de SonarCloud
   3. En la seleccion de tipo de análisis, seleccionar **Use Standalone scanner**
   4. En modo, seleccionar **Configuración proveida manualmente**
   5. En el campo Clave de proyecto, ingresar la clave proveida por SonarCloud
   6. en el nombre del proyecto, ingresar el nombre del proyecto
    **IMPORTANTE** Asegurese que la tarea de sonarcloud quede después del paso de build.
   * Correr el análisis.
   * Resultados de la publicación.
   * Guardar y correr el pipeline.
 5. Cree el archivo ```sonar-project.properties```
   1. Cree un nuevo archivo llamado ```sonar-project.properties```
   2. Copie y guarde la siguiente configuración en el archivo
   ``
  sonar.projectKey=LLAVEDELPROYECTOSONARCLOUD
  sonar.organization=NOMBREORGANIZACIONSONARCLOUD

  # This is the name and version displayed in the SonarCloud UI.
  #sonar.projectName=LLAVEDELPROYECTOSONARCLOUD
  #sonar.projectVersion=1.0

  # Path is relative to the sonar-project.properties file. Replace "\" by "/" on Windows.
  #sonar.sources=.

  # Encoding of the source code. Default is default system encoding
  #sonar.sourceEncoding=UTF-8
   ``

**NOTA**: Para los proyectos publicos es necesario solicitar "_Azure DevOps Parallelism Request_" (especialmente si son proyectos públicos) esto se hace a través de siguiente link [Request Parallelism](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR63mUWPlq7NEsFZhkyH8jChUMlM3QzdDMFZOMkVBWU5BWFM3SDI2QlRBSC4u)

## Instalación de SonarCloud en Github
1. Ingresar a SonarCloud, sino tiene cuenta creada, puede crear su cuenta a través de la cuenta de GitHub.
2. Instale la extensión de SonarCloud para GitHub
3. Otorgue los permisos solicitados por SonarCloud para GitHub

## Resultados Github

![image](https://user-images.githubusercontent.com/100396227/161389617-f78b701c-023e-4ffc-9361-6bc7b86e3516.png)
* ### CodeSmell detectado
![image](https://user-images.githubusercontent.com/100396227/161389670-84ed94b0-ed9b-468b-8058-0283fc9a2557.png)
Los CodeSmell detectados por Sonar se debe principalmente al uso de caracteres especiales o el guardado de información en variables poco claras (i,x... etc) en especial en las pruebas unitarias. Sonar hace la aclaración que la prioridad son las variables debido a que son errores críticos, sin embargo, se evidencia que la calificación general del proyecto respecto al item es calificación A.
* Debt Radio
![image](https://user-images.githubusercontent.com/100396227/161389748-af27e7f0-57e7-4281-9257-5eca2d89a54e.png)
El indice de deuda indica que el porcentaje de deuda técnica con respecto a la solución completa es pequeño y optimo debido que solo es un 1.1% del código que tiene deuda respecto al total de las líneas de código.

En general la solución tiene buena calificación respecto a su tamaño, lo cual la cataloga como solución buena debido al reiting A en los diferentes aspectos analizados por Sonar.

## Autores ✒️

* **Camilo Alejandro Rojas** - *Trabajo y documentación* - [camrojass](https://github.com/camrojass)

## Licencia 📄

Este proyecto está bajo la Licencia - mira el archivo [LICENSE.txt](LICENSE.txt) para detalles
