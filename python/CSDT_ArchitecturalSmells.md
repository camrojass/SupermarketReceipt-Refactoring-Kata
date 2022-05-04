# Proyecto Curso: SupermarketReceipt Refactoring - Deuda en Arquitectura


## Requisitos 

* Repositorio (puede ser en [github](https://github.com/))
* Proyecto público en [Azure DevOps](https://dev.azure.com/)**
* Cuenta en Sonarcloud [SonarCloud](https://sonarcloud.io/)

** Debido que para poder ser analizado a través de SonarCloud, solicita que el proyecto esté como público. Implica que se deba pedir el permiso "_Azure DevOps Parallelism Request_" [Request Parallelism](https://forms.office.com/pages/responsepage.aspx?

## Instalación de SonarCloud en Azure

Con el proyecto como público, realizar los pasos a continuación:
1. Ingresar a SonarCloud, sino tiene cuenta creada, puede crear su cuenta a través de la cuenta de Azure DevOps
2. Instale la extensión Sonarcloud a través de [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarcloud)
3. Agregar el Endpoind del servicio de SonarCloud en Azure
  * Ir a la configuración del proyecto a la opción Connexiones de servicio
  * Agregar la conexión de servicio tipo SonarCloud
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
   1. Cree un nuevo archivo en la raíz del proyecto que se llame ```sonar-project.properties```
   2. Copie y guarde la siguiente configuración en el archivo
   ```
  sonar.projectKey=LLAVEDELPROYECTOSONARCLOUD
  sonar.organization=NOMBREORGANIZACIONSONARCLOUD

  # This is the name and version displayed in the SonarCloud UI.
  #sonar.projectName=LLAVEDELPROYECTOSONARCLOUD
  #sonar.projectVersion=1.0

  # Path is relative to the sonar-project.properties file. Replace "\" by "/" on Windows.
  #sonar.sources=.

  # Encoding of the source code. Default is default system encoding
  #sonar.sourceEncoding=UTF-8
   ```

**NOTA**: Para los proyectos publicos es necesario solicitar "_Azure DevOps Parallelism Request_" (especialmente si son proyectos públicos) esto se hace a través de siguiente link [Request Parallelism](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR63mUWPlq7NEsFZhkyH8jChUMlM3QzdDMFZOMkVBWU5BWFM3SDI2QlRBSC4u)

## Instalación de SonarCloud en Github
1. Ingresar a SonarCloud, sino tiene cuenta creada, puede crear su cuenta a través de la cuenta de GitHub.
2. Instale la extensión de SonarCloud para GitHub
3. Otorgue los permisos solicitados por SonarCloud para GitHub

## Resultados SonarCloud con AzureDevOps

![image](https://user-images.githubusercontent.com/100396227/162575562-2aa23a41-a3a5-4b63-b44d-ebe26bb7aa1a.png)
SonarCloud está evaluando la carpeta "test" como carpeta de código adicional, debido a que no se encuentra en la raíz.
* ### Descripción del Proyecto
![image](https://user-images.githubusercontent.com/100396227/162576792-5bc4a193-7cde-455a-9370-913d62d84782.png)
En la gráfica de Coverage vs Deuda técnica evidencia que en general el CodeSmell detectado no es de alto impacto (color verde) lo cual evidencia que en general el proyecto tiene cosas por mejorar que no son de alto impacto. Por otro lado, y teniendo en cuenta que está contemplando la carpeta de pruebas como una carpeta de código y no de pruebas unitarias, indica que el principal trabajo a realizar en esta carpeta.
* ### CodeSmell detectado
![image](https://user-images.githubusercontent.com/100396227/162575804-dc72c58d-685c-4033-adde-8886a0309d7f.png)
Los CodeSmell detectados por Sonar se debe principalmente al uso de caracteres especiales o el guardado de información en variables poco claras (i,x... etc) en especial en las pruebas unitarias. Sonar hace la aclaración que la prioridad son las variables debido a que son errores críticos, sin embargo, se evidencia que la calificación general del proyecto respecto al item es calificación A.
* ### Debt Radio
![image](https://user-images.githubusercontent.com/100396227/162575868-ff120a77-6317-41ea-8f6a-3cb3f1b57dee.png)
El indice de deuda indica que el porcentaje de deuda técnica con respecto a la solución completa es pequeño y optimo debido que solo es un 1.1% del código que tiene deuda respecto al total de las líneas de código.
## Resultados SonarCloud con Github

![image](https://user-images.githubusercontent.com/100396227/161389617-f78b701c-023e-4ffc-9361-6bc7b86e3516.png)
* ### Descripción del proyecto
![image](https://user-images.githubusercontent.com/100396227/162576213-1c4128f4-c49d-4553-b39c-abc87b6cc961.png)
No muestra resultados debido a que no ha habido cambios de código en los últimos 30 días.
* ### CodeSmell detectado
![image](https://user-images.githubusercontent.com/100396227/161389670-84ed94b0-ed9b-468b-8058-0283fc9a2557.png)
Al igual que en los resultados con Azure DevOps, Los CodeSmell detectados por Sonar se debe principalmente al uso de caracteres especiales o el guardado de información en variables poco claras (i,x... etc) en especial en las pruebas unitarias.
* ### Debt Radio
![image](https://user-images.githubusercontent.com/100396227/161389748-af27e7f0-57e7-4281-9257-5eca2d89a54e.png)
Al igual que en los resultados con Azure DevOps, El indice de deuda indica que el porcentaje de deuda técnica con respecto a la solución completa es pequeño y optimo debido que solo es un 1.1% del código que tiene deuda respecto al total de las líneas de código.

En general la solución tiene buena calificación respecto a su tamaño, lo cual la cataloga como solución buena debido al raiting A en los diferentes aspectos analizados por Sonar.

## Comparativa de resultados
Cabe mencionar que dado que se hizo la integración continua con Azure DevOps, y existen dos ramas allí se ve el doble de líneas de código entre los dos resultados. Teniendo en cuenta lo anterior, en general, los resultados son identicos lo cual evidencia que el uso de _SonarCloud_ en diferentes plataformas no tiene variación. Sin embargo, un punto interesante a contemplar es el ítem de tiempo puesto que la comparación del coverage vs la deuda técnica no es visible en Github debido a que en los últimos 30 días no han habido cambios de código, cosa que no tiene en cuenta con el resultado de Azure DevOps.

## Taller de atributos de calidad
Teniendo en cuenta los resultados obtenidos en los diferentes analisis realizados a través de SonarCloud, se hace necesario considerar los siguientes escenarios de negocio como parte de la mejora continua de la arquitectura del proyecto.

### Escenario No. 1
Se evidencia en los diferentes análisis que una de las actuales limitaciones del sistema es la cobertura de código diversa en los diferentes elementos o componentes del proyecto, por tal razón se hace necesario establecer un estandar mínimo para todo el código.
![image](https://user-images.githubusercontent.com/100396227/165436208-453a7c99-e480-40fd-be70-20901a68b3d6.png)
### Escenario No. 2
Teniendo en cuenta que las diferentes ofertas se encuentran en un código spagetti, se hace evidente que se establezca un escenario de nuevos descuentos a aplicar con consideraciones más específicas como lo es el descuento de _Madrugón_ o _Trasnochón_ que los supermercados realizan en fechas especiales del año. 

![image](https://user-images.githubusercontent.com/100396227/165436118-c66ae79b-75bd-4bb1-95d2-f024dbd295ea.png)
### Escenario No. 3
Dentro de las consideraciones a tener en cuenta está el aumento de clientes que puede tener un supermercado en horas pico lo cual hace innevitable que se agregue más componentes para mejorar el tiempo de servicio, sin embargo, esto implica realizar escalamientos del sistema manteniendo el rendimiento actual.

![image](https://user-images.githubusercontent.com/100396227/166619513-12b35694-a029-4f08-93b4-324d42861d93.png)

## Autores ✒️

* **Camilo Alejandro Rojas** - *Trabajo y documentación* - [camrojass](https://github.com/camrojass)

## Licencia 📄

Este proyecto está bajo la Licencia - mira el archivo [LICENSE.txt](LICENSE.txt) para detalles
