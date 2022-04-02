# Proyecto Curso: Primera entrega SupermarketReceipt Refactoring

La solución en Python consiste en un supermercado que dispone de un catálogo con diferentes tipos de productos (arroz, manzanas, leche, cepillos de dientes,etc.). Cada producto tiene precio, y el precio total del carrito de compras es el total de todos los precios de los artículos. La solución da un recibo que detalla los artículos que compró, el precio total y los descuentos que se aplicaron.

El supermercado ofrece ofertas especiales, por ejemplo:
 - Compra dos cepillos de dientes, llévate uno gratis. El precio del cepillo de dientes normal es de 0,99€
 - 20% de descuento en manzanas, precio normal 1,99€ el kilo.
 - 10% de descuento en arroz, precio normal 2,49€ la bolsa
 - Cinco tubos de pasta de dientes por 7,49 €, precio normal 1,79 €
 - Dos cajas de tomates cherry por 0,99€, precio normal 0,69€ la caja.

## Code Smells detectados

 1. "Bloaters" en el código "shopping_cart.py" utiliza 'if' para detallar todas las ofertas posibles, dificultando agregar nuevas ofertas.
 
  ``` 
                if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3
 
                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                        discount_n = unit_price * quantity - total
                        discount = Discount(p, "2 for " + str(offer.argument), -discount_n)
 
                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5
 
                number_of_x = math.floor(quantity_as_int / x)
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                    discount_amount = quantity * unit_price - (
                                (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                    discount = Discount(p, "3 for 2", -discount_amount)
 ```
 2. "Long Method" en los códigos "receipt_printer.py", y "shopping_cart.py" lo cual dificulta el entendimiento del código al momento de leerlo y de hacer posibles actualizaciones o ingreso de nuevas funcionalidades
 3. "Feature envy" en los códigos "receipt.py", "receipt_printer.py" y "shopping_cart.py" no utiliza los métodos propios sino que utiliza más los métodos del código "model_objects.py", "receipt_printer.py" y "model_objects.py" respectivamente.
```
    def print_receipt(self, receipt):
        result = ""
        for item in receipt.items:
            receipt_item = self.print_receipt_item(item)
            result += receipt_item

        for discount in receipt.discounts:
            discount_presentation = self.print_discount(discount)
            result += discount_presentation

        result += "\n"
        result += self.present_total(receipt)
        return str(result)
```

### Tecnicas a Utilizar para solucionar Code Smells

1. Refactoring al archivo "receipt_printer.py" realizando la extracción de método, movimiendo la lógica de salto de línea a una nueva clase.
2. Refactoring al archivo "shopping_cart.py" realizando la extracción de método, movimiendo los calculos de ofertas a una nueva clase llamada detalle.
3. Refactoring al detalle de "shopping_cart.py" modificando la lógica del método para evitar la depentencia de los "ifs".

### Características de Clean Code no cumplidas

#### Código enfocado: 
 - El código de "shopping_cart.py" contiene la cantidad de productos y adicionalmente realiza los calculos de descuentos.
p.e.
```
@property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                        discount_n = unit_price * quantity - total
                        discount = Discount(p, "2 for " + str(offer.argument), -discount_n)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5
```

#### Entendible
 - El código de "shopping_cart.py" no tiene un código simple incumpliendo el principio KIS.
```
  def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                        discount_n = unit_price * quantity - total
                        discount = Discount(p, "2 for " + str(offer.argument), -discount_n)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5

                number_of_x = math.floor(quantity_as_int / x)
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                    discount_amount = quantity * unit_price - (
                                (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                    discount = Discount(p, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(p, str(offer.argument) + "% off",
                                        -quantity * unit_price * offer.argument / 100.0)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                    discount_total = unit_price * quantity - (
                                offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
                    discount = Discount(p, str(x) + " for " + str(offer.argument), -discount_total)

                if discount:
                    receipt.add_discount(discount)
```
#### Escalable
 - El código de "shopping_cart.py" no tiene un código escalable en la lógica de descuentos.
```
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                    discount_amount = quantity * unit_price - (
                                (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                    discount = Discount(p, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(p, str(offer.argument) + "% off",
                                        -quantity * unit_price * offer.argument / 100.0)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                    discount_total = unit_price * quantity - (
                                offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
                    discount = Discount(p, str(x) + " for " + str(offer.argument), -discount_total)
```
#### Abstracción
 - El código de "shopping_cart.py" utiliza un método largo para el calculo de los descuentos.
 - El código de "receipt_printer.py" utiliza una clase extensa para imprimir el recibo que contiene la lista de productos y la estructura que el recibo debe tener.

### Principios de Programación no cumplidos en el código

#### KISS 
No todo es un código simple, en especial el código de "shopping_cart.py" ya que incluye la lógica de los productos y sus cantidades y adicionalmente, la lógica de descuentos con muchos if de por medio.

#### SOLID
 - A como está con el código hoy, en especial el código de "shopping_cart.py" está abierto a modificaciones debido a la forma en que se maneja la lógica de descuentos. Esto también implica que la clase de este código esté afectada ya que hace varias cosas, tiene la lógica de cantidad y productos y la lógica de descuento.
 - En la clase del código "receipt_printer.py" incluye el formato del recibo y recibe la información de productos y cantidades.

### Practicas XP para utilizar en el código
Como parte de las sugerencias para complementar la solución revisada, se sugiere utilizar las siguientes prácticas XP para mejorar el proyecto.
### Refactoring
### Diseño Simple
### Integración continua
### Estandarización de códigos
### Juego de planificación
### Pequeños Releases

### Diagnóstico Inicial Testing Debt

El proyecto cuenta con una sola prueba unitaria "test ten percent discount" la cual tiene como objetivo probar uno de los escenarios de descuento o de oferta ofrecidos por el almacen tiene las siguientes características y falencias:

  ``` 
  def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity  
  ``` 

#### Prácticas Cumplidas
- Utiliza un estándar de nombramiento (Para el uso de pytest el test debe comienzar con la palabra "test").

#### Prácticas No Cumplidas
- No utiliza practicas de Clean Code en sus UT.
- Solo valida un escenario.
- Tiene muchos asserts en su único test (7).
- Las prueba unitaria depende del archivo "fake_catalog.py" que en teoría es independiente de la solución.
- No  utiliza el patron AAA (Arrange, Act, Assert).
- No promueve un alto cubrimiento (Coverage).

### Propuesta de Pruebas Unitarias

Se propone 3 pasos para mejorar el Coverage de las pruebas unitarias
Paso 1. Estandarizar las UT actuales con el Patron AAA (Arrange, Act, Assert) y determinar los asserts determinantes.
Paso 2. Complementar con más escenearios de ofertas especiales.
Paso 3. Complementar con pruebas por clase o por sección.

 #### PASO 1
 Estandarizar la prueba actual con el Patron AAA (Arrange, Act, Assert) y hacer la respectiva división de assert o dejar los que dan mayor alcance y utilizar las prácticas de Clen Code.
  ``` 
  def test_ten_percent_discount():
    #ARRANGE
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)   
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    teller = Teller(catalog)
    
    #ACT
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    cart = ShoppingCart()
    cart.add_item_quantity(apples, 3)
    receipt = teller.checks_out_articles_from(cart)
    receipt_item = receipt.items[0]
    ResponseExpected = 3 * 1.99

    #ASSERT
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    assert apples == receipt_item.product
    assert ResponseExpected == pytest.approx(receipt.total_price(), 0.01)
    assert ResponseExpected == pytest.approx(receipt_item.total_price, 0.01)
  ``` 

 #### PASO 2
 Continuando la estrategía de pruebas propuesta en la solución (probar los escenarios de descuentos) se necesita complementar las pruebas por escenario de Oferta especial. Por ejemplo:

- test_SingleProduct_NoDiscount
  ``` 
  def test_SingleProduct_NoDiscount():
    qty = 5
    price = 2.99
    #ARRANGE
    catalog = FakeCatalog()
    oranges = Product("oranges", ProductUnit.KILO)
    catalog.add_product(oranges, price)
    teller = Teller(catalog)
    

    #ACT
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, oranges, 5.0)
    
    cart = ShoppingCart()
    cart.add_item_quantity(oranges,qty)
    
    receipt = teller.checks_out_articles_from(cart)
    receipt_item = receipt.items[0]
    ResponseExpected = qty*price

    #ASSERT
    assert ResponseExpected == pytest.approx(receipt_item.total_price, 0.01)
    assert oranges == receipt_item.product 
  ``` 
  Como el caso anterior, incluiría los siguientes casos adicionales
  - test_two_for_amount_discount
  - test_five_for_amount_discount
  - test_three_for_two_discount
  
  #### PASO 3
  Por último se considera necesario agregar pruebas unitarias por sección. La solución propuesta tiene la ventaja de estar divida en varias partes (teller, Shopping_cart, model_objects, etc) lo recomentable es que por cada parte incluir al menos una prueba unitaria.
  ``` 
   def test_teller_qty():
    #ARRANGE
    catalog = FakeCatalog()
    apples = Product("apples", ProductUnit.KILO) 
    catalog.add_product(apples, 1.99)
    cart = ShoppingCart()

    #ACT
    teller = Teller(catalog)
    cart.add_item_quantity(apples, 3)
    receipt = teller.checks_out_articles_from(cart)
    Receipt_item = receipt.items[0]
    ReceiptExpected = 3

    #ASSERT
    assert ReceiptExpected == Receipt_item.quantity
  ``` 
  
  ### Mejoras para reducción de deuda
  
  - Ser más organizado con el código (incluyendo UT).
  - Utilizar las prácticas de clean code hasta en las Pruebas Unitarias.
  - Segmentar mejor las pruebas

  ## Modelo de Calidad
  
  ### Pasos preliminares
  
  Para realizar el análisis a través [bettercodehub](http://bettercodehub.com/) se debe tener cuenta en la plataforma o se puede utilizar la cuenta de de github. Se puede utilizar en versión gratuita la cual permite realizar análisis ilimitados pero las soluciones que quedan públicas o la cuenta paga la cual permite el análisis a soluciones privadas. Cabe mencionar que los planes pagos tienen una versión de prueba por un tiempo limitado.
  
  Una vez seleccionado el plan la herramienta precarga la información de todos los repositorios de tu cuenta github. Selecciona el repositorio correspondiente y ejecuta el análisis.
  
  ### Resultado del Análisis 
  
  [![BCH compliance](https://bettercodehub.com/edge/badge/camrojass/SupermarketReceipt-Refactoring-Kata?branch=main)](https://bettercodehub.com/)
  
  ![image](https://user-images.githubusercontent.com/100396227/159835996-b36e78ad-272e-4889-afda-dc9ba072a0ac.png)
  ![image](https://user-images.githubusercontent.com/100396227/159836079-ff756deb-4977-4667-8479-66708f66d250.png)
  ![image](https://user-images.githubusercontent.com/100396227/159836725-171ee016-82e5-419b-bcba-873d8bea0516.png)
  
Después de la ejecución del ánalisis en la solución a través de [bettercodehub](http://bettercodehub.com/), el cual presenta un análisis en multiples aspectos (10 aspectos), se detecta que e código cumple con los siguientes ítems positivos.
  
  * #### Escribir el código en pequeñas unidades
  Esto indica que el código en general está seccionado en pequeñas unidades.
  
  * #### Escribir código una sola vez (No repetido)
  El código no tiene secciones repetidas.
  
  * #### Separar código por módulos
  El código está seperado por módulos (Modelo de Objetos, Carro de compras, Recibido, etc.)
  
  * #### Componentes de Arquitectura libres
  Se debe tener en cuenta que su estructura la solución es un solo código lo cual lo hace independiente y sin necesidad de otros componentes. Se debe tener en cuenta para el momento de agregar nuevo código que se mantenga esa condición.
  
  * #### Mantener el código pequeño
  El código está divido en secciones pequeñas.
  
  * #### Pruebas automatizadas
  El código cueta con pruebas automatizadas.
  
  * #### Código limpio
  

Sin embargo, tiene por mejorar los siguientes ítems

  * #### Escribir unidades pequeñas
  Esto debido a que una parte de la solución es muy extensa, específicamente en el módulo de Shopping_Car al incluir las ofertas de descuento.
 ```
    def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                        discount_n = unit_price * quantity - total
                        discount = Discount(p, "2 for " + str(offer.argument), -discount_n)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5

                number_of_x = math.floor(quantity_as_int / x)
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                    discount_amount = quantity * unit_price - (
                                (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                    discount = Discount(p, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(p, str(offer.argument) + "% off",
                                        -quantity * unit_price * offer.argument / 100.0)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                    discount_total = unit_price * quantity - (
                                offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
                    discount = Discount(p, str(x) + " for " + str(offer.argument), -discount_total)

                if discount:
                    receipt.add_discount(discount) 
 ```
 
  * #### Contiene unidades de interfase pequeñas
  Se debe a que en pequeñas secciones de código se solicita muchos parámetros como por ejemplo.
 
 ```
     def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price
 ```
 
 ```
    def __init__(self):
        self._items = []
        self._product_quantities = {}
 ``` 
 
  * #### Balance de los componentes de arquitectura
  De acuerdo al análisis la solución, al ser un único componente de 176 líneas no es balanceado. Cabe mencionar que el código no complejo por lo que no es estrictamente un punto delicado. Se debe tener en cuenta al aplicar nuevas funciones que los componentes no superen las 170 líneas por componente.

## Integración Continua

### Requisitos 

* Repositorio (puede ser en [github](https://github.com/))
* Cuenta en [Azure DevOps](https://dev.azure.com/)

### Instalación

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

* #### Uso de varias versiones de Python
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
* #### Instalar dependencias
  Puede usar scripts para instalar paquetes PyPI específicos con ```pip```. Por ejemplo, este YAML instala o actualiza y los paquetes ```pytest```
  **NOTA** Pytest solo está disponible para las versiones x64
  ```
  - script: |
    pip install pytest pytest-azurepipelines
    pytest --doctest-modules --junitxml=test-results.xml
  displayName: 'pytest'
  ```
* #### Prueba con pytest y recopilación de métricas de cobertura con pytest-cov
Use este YAML para instalar ```pytest``` y ```pytest-cov``` para ejecutar pruebas, ver resultados de pruebas de salida en formato JUnit y resultados de cobertura de código de salida en formato COBERTURA XML:
```
- script: |
    pip install pytest pytest-azurepipelines
    pip install pytest-cov
    pytest --doctest-modules --junitxml=test-results.xml --cov=. --cov-report=xml
  displayName: 'pytest'
```
* #### Publicación de resultados de pruebas
Agregue la tarea Publicar Resultados de pruebas para publicar los resultados de pruebas de JUnit o xUnit en el servidor. Con esto podrá ver las pruebas referenciadas directamente en azure a través del módulo de test  [Azure DevOps](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/_testManagement/runs?_a=runQuery)
```
- task: PublishTestResults@2
  condition: succeededOrFailed()
  inputs:
    testResultsFiles: 'test-results.xml'
    testRunTitle: 'Publish test results for Python $(python.version)'
```
* #### Publicación de resultados de cobertura de código
Agregue la tarea Publicar resultados de cobertura de código para publicar los resultados de cobertura de código en el servidor. Puede ver las métricas de cobertura en el resumen de compilación y descargar informes HTML para su posterior análisis.
```
- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: Cobertura
    summaryFileLocation: '$(System.DefaultWorkingDirectory)/**/coverage.xml'
```
Para ver el proyecto en Azure seguir el siguiente link [Azure DevOps](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/)

### Resultados
[![Build Status](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/_apis/build/status/camrojass.SupermarketReceipt-Refactoring-Kata?branchName=main)](https://dev.azure.com/camilorojas-s/SupermarketReceipt-Refactoring-Kata/_build/latest?definitionId=1&branchName=main)

* #### Build
![image](https://user-images.githubusercontent.com/100396227/160519119-5721d0bf-df7b-4a8e-ba63-ed1f2a3fcbf6.png)
![image](https://user-images.githubusercontent.com/100396227/160519021-3a0cfdfa-af47-49ea-b48d-12c58c7a9683.png)

* #### Code Analysis
![image](https://user-images.githubusercontent.com/100396227/160519199-2f66f7f5-ce09-4d5f-86cc-596e8c16c72e.png)

* #### Test
![image](https://user-images.githubusercontent.com/100396227/160518543-4270c370-3175-4f67-a990-f9d85c5a9cd8.png)
![image](https://user-images.githubusercontent.com/100396227/160518667-adac0090-7087-46e4-a727-f5a1a024a119.png)

## Autores ✒️

* **Dave Thomas** - *Descripción Inicial* - [codekata](http://codekata.com/kata/kata01-supermarket-pricing/)
* **Emily Bache** - *Variacion de la Kata* - [emilybache](https://github.com/emilybache)
* **Camilo Alejandro Rojas** - *Trabajo y documentación* - [camrojass](https://github.com/camrojass)

## Licencia 📄

Este proyecto está bajo la Licencia - mira el archivo [LICENSE.txt](LICENSE.txt) para detalles

## Bibliografia

  * [Integrate Your GitHub Projects With Azure Pipelines](https://www.azuredevopslabs.com/labs/azuredevops/github-integration/)
  * [Microsoft docs python](https://docs.microsoft.com/es-mx/azure/devops/pipelines/ecosystems/python?view=azure-devops)
