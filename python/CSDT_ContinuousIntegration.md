# Proyecto Curso: SupermarketReceipt Refactoring - Integración Continua


## Requisitos 

* Repositorio (puede ser en [github](https://github.com/))
* Cuenta en [Azure DevOps](https://dev.azure.com/)

## Instalación

1. Inicie sesión en su Azure DevOps organización y vaya al proyecto.
2. Vaya a **Pipelines** y seleccione **Nueva canalización**.
3. Siga los pasos del asistente seleccionando primero **GitHub** como ubicación del código fuente.
4. Puede que se le redirija a GitHub para iniciar sesión. Si es así, escriba sus credenciales de GitHub.
5. Cuando vea la lista de repositorios, seleccione el repositorio.
6. Es posible que se le redirija a GitHub para instalar la aplicación Azure Pipelines. Si es así, seleccione **Aprobar instalación**.
7. Cuando aparezca la pestaña Configurar, seleccione Paquete de Python para crear un paquete de Python para probar en varias versiones de Python.
8. Cuando aparezca la nueva canalización, revisa el YAML para ver lo que hace. Cuando esté listo, seleccione **Guardar y ejecutar**.
![image](https://user-images.githubusercontent.com/100396227/160325531-f348b307-7f03-4a28-ad73-c4e56ffca93f.png)
9. Se pedirá que confirme un nuevo archivo azure-pipelines.yml en el repositorio. Una vez confirme el mensaje, seleccione **Guardar y ejecutar de nuevo**.
   Si desea ver la canalización en acción, seleccione el trabajo de compilación.
10. Cuando esté listo para realizar cambios en la canalización, selecciónelo en la Pipelines y, a continuación, edite el archivo.

**NOTA**: Para algunos proyectos es necesario solicitar "_Azure DevOps Parallelism Request_" (especialmente si son proyectos públicos) esto se hace a través de siguiente link [Request Parallelism](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR63mUWPlq7NEsFZhkyH8jChUMlM3QzdDMFZOMkVBWU5BWFM3SDI2QlRBSC4u)

### Uso de varias versiones de Python
  Para ejecutar una canalización con varias versiones de Python, por ejemplo, para probar un paquete con esas versiones, defina una matrix con las versiones de Python. A continuación, establezca UsePythonVersion la tarea para hacer referencia a la matrix variable .
  ```
  strategy:
   matrix:
     Python36:
       python.version: '3.6'
     Python37:
       python.version: '3.7'
     Python38:
       python.version: '3.8'
     Python39:
       python.version: '3.9'

  steps:  
  - task: UsePythonVersion@0
   inputs:
     versionSpec: '$(python.version)'
   displayName: 'Use Python $(python.version)'
  ```
### Instalar dependencias
  Puede usar scripts para instalar paquetes PyPI específicos con ```pip```. Por ejemplo, este YAML instala o actualiza y los paquetes ```pytest```
  **NOTA** Pytest solo está disponible para las versiones x64
  ```
  - script: |
    pip install pytest pytest-azurepipelines
    pytest --doctest-modules --junitxml=test-results.xml
  displayName: 'pytest'
  ```
### Prueba con pytest y recopilación de métricas de cobertura con pytest-cov
Use este YAML para instalar ```pytest``` y ```pytest-cov``` para ejecutar pruebas, ver resultados de pruebas de salida en formato JUnit y resultados de cobertura de código de salida en formato COBERTURA XML:
```
- script: |
    pip install pytest pytest-azurepipelines
    pip install pytest-cov
    pytest --doctest-modules --junitxml=test-results.xml --cov=. --cov-report=xml
  displayName: 'pytest'
```
### Publicación de resultados de pruebas
Agregue la tarea Publicar Resultados de pruebas para publicar los resultados de pruebas de JUnit o xUnit en el servidor. Con esto podrá ver las pruebas referenciadas directamente en azure a través del módulo de test  [Azure DevOps](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/_testManagement/runs?_a=runQuery)
```
- task: PublishTestResults@2
  condition: succeededOrFailed()
  inputs:
    testResultsFiles: 'test-results.xml'
    testRunTitle: 'Publish test results for Python $(python.version)'
```
### Publicación de resultados de cobertura de código
Agregue la tarea Publicar resultados de cobertura de código para publicar los resultados de cobertura de código en el servidor. Puede ver las métricas de cobertura en el resumen de compilación y descargar informes HTML para su posterior análisis.
```
- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: Cobertura
    summaryFileLocation: '$(System.DefaultWorkingDirectory)/**/coverage.xml'
```
Para ver el proyecto en Azure seguir el siguiente link [Azure DevOps](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/)

## Resultados
[![Build Status](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/_apis/build/status/camrojass.SupermarketReceipt-Refactoring-Kata?branchName=main)](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/_build/latest?definitionId=1&branchName=main)
### Build
![image](https://user-images.githubusercontent.com/100396227/160519119-5721d0bf-df7b-4a8e-ba63-ed1f2a3fcbf6.png)
![image](https://user-images.githubusercontent.com/100396227/160519021-3a0cfdfa-af47-49ea-b48d-12c58c7a9683.png)

### Code Analysis
![image](https://user-images.githubusercontent.com/100396227/160519199-2f66f7f5-ce09-4d5f-86cc-596e8c16c72e.png)

### Test
![image](https://user-images.githubusercontent.com/100396227/160518543-4270c370-3175-4f67-a990-f9d85c5a9cd8.png)
![image](https://user-images.githubusercontent.com/100396227/160518667-adac0090-7087-46e4-a727-f5a1a024a119.png)

## Autores ✒️

* **Camilo Alejandro Rojas** - *Trabajo y documentación* - [camrojass](https://github.com/camrojass)

## Licencia 📄

Este proyecto está bajo la Licencia - mira el archivo [LICENSE.txt](LICENSE.txt) para detalles

## Bibliografia

  * [Integrate Your GitHub Projects With Azure Pipelines](https://www.azuredevopslabs.com/labs/azuredevops/github-integration/)
  * [Microsoft docs python](https://docs.microsoft.com/es-mx/azure/devops/pipelines/ecosystems/python?view=azure-devops)

