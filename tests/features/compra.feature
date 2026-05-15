Feature: Compra de produto

  Scenario: Compra com sucesso sem cupom
    Given que o produto "teclado" está disponível no estoque
    When o cliente realiza a compra com cartão "1234 5678 9012 3456"
    Then a compra é aprovada com valor de R$ 200.00

  Scenario: Compra com cupom GEEK20
    Given que o produto "teclado" está disponível no estoque
    When o cliente compra com cupom "GEEK20" e cartão "1234 5678 9012 3456"
    Then o valor pago é R$ 160.00
