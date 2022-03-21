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
  
  Después de revisión de la solución a través de [bettercodehub](http://bettercodehub.com/), el cual presenta un análisis en multiples aspectos (10 aspectos), se detecta que e código cumple con los siguientes ítems positivos.
  
  ### Escribir el código en pequeñas unidades
  Esto indica que el código en general está seccionado en pequeñas unidades.
  
  ### Escribir código una sola vez (No repetido)
  El código no tiene secciones repetidas.
  
  ### Separar código por módulos
  El código está seperado por módulos (Modelo de Objetos, Carro de compras, Recibido, etc.)
  
  ### Componentes de Arquitectura libres
  Se debe tener en cuenta que su estructura la solución es un solo código lo cual lo hace independiente y sin necesidad de otros componentes. Se debe tener en cuenta para el momento de agregar nuevo código que se mantenga esa condición.
  
  ### Mantener el código pequeño
  El código está divido en secciones pequeñas.
  
  ### Pruebas automatizadas
  El código cueta con pruebas automatizadas.
  
  ### Código limpio
  

Sin embargo, tiene por mejorar los siguientes ítems

 ### Escribir unidades pequeñas
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
 
 ### Contiene unidades de interfase pequeñas
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
 
 ### Balance de los componentes de arquitectura
 De acuerdo al análisis la solución, al ser un único componente de 176 líneas no es balanceado. Cabe mencionar que el código no complejo por lo que no es estrictamente un punto delicado. Se debe tener en cuenta al aplicar nuevas funciones que los componentes no superen las 170 líneas por componente.

## Autores ✒️

* **Dave Thomas** - *Descripción Inicial* - [codekata](http://codekata.com/kata/kata01-supermarket-pricing/)
* **Emily Bache** - *Variacion de la Kata* - [emilybache](https://github.com/emilybache)
* **Camilo Alejandro Rojas** - *Trabajo y documentación* - [camrojass](https://github.com/camrojass)

## Licencia 📄

Este proyecto está bajo la Licencia - mira el archivo [LICENSE.txt](LICENSE.txt) para detalles

