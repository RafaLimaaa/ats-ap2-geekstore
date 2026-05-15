# language: pt

Funcionalidade: Fluxo de compra na GeekStore
  Como cliente da GeekStore
  Quero comprar produtos pelo site
  Para receber meus itens com pagamento processado corretamente

  Cenário: Compra bem-sucedida sem cupom
    Dado que o produto "teclado" está disponível no estoque
    Quando eu realizo a compra com o cartão "1234 5678 9012 3456" sem cupom
    Então a resposta deve ter status 200
    E o valor pago deve ser 200.0
    E a mensagem deve confirmar a aprovação

  Cenário: Compra com cupom GEEK20 aplica desconto de 20%
    Dado que o produto "teclado" está disponível no estoque
    Quando eu realizo a compra com o cartão "1234 5678 9012 3456" e o cupom "GEEK20"
    Então a resposta deve ter status 200
    E o valor pago deve ser 160.0

  Cenário: Tentativa de compra de produto sem estoque
    Dado que o produto "mouse" está sem estoque
    Quando eu realizo a compra com o cartão "1234 5678 9012 3456" sem cupom
    Então a resposta deve ter status 400

  Cenário: Tentativa de compra de produto inexistente
    Quando eu tento comprar o produto "headset" com o cartão "1234 5678 9012 3456"
    Então a resposta deve ter status 404
