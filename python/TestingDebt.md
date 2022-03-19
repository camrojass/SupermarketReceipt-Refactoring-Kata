# Testing Debt

## Diagnóstico Inicial

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

### Prácticas Cumplidas
- Utiliza un estándar de nombramiento (Para el uso de pytest el test debe comienzar con la palabra "test").

### Prácticas No Cumplidas
- No utiliza practicas de Clean Code en sus UT.
- Solo valida un escenario.
- Tiene muchos asserts en su único test (7).
- Las prueba unitaria depende del archivo "fake_catalog.py" que en teoría es independiente de la solución.
- No  utiliza el patron AAA (Arrange, Act, Assert).
- No promueve un alto cubrimiento (Coverage).

## Propuesta de Pruebas Unitarias

Se propone 3 pasos para mejorar el Coverage de las pruebas unitarias
Paso 1. Estandarizar las UT actuales con el Patron AAA (Arrange, Act, Assert) y determinar los asserts determinantes.
Paso 2. Complementar con más escenearios de ofertas especiales.
Paso 3. Complementar con pruebas por clase o por sección.

### PASO 1
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

### PASO 2
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
  
  ### PASO 3
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
  
  ## Mejoras para reducción de deuda
  
  - Ser más organizado con el código (incluyendo UT).
  - Utilizar las prácticas de clean code hasta en las Pruebas Unitarias.
  - Segmentar mejor las pruebas
  
