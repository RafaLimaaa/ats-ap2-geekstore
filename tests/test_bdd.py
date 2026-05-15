import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/compra.feature")


@given(parsers.parse('que o produto "{nome}" está disponível no estoque'), target_fixture="ctx")
def produto_disponivel(nome):
    return {"produto": nome}


@when(
    parsers.parse('o cliente realiza a compra com cartão "{cartao}"'),
    target_fixture="resposta",
)
def comprar_sem_cupom(client, ctx, cartao):
    return client.post("/api/comprar", json={
        "produto": ctx["produto"],
        "cartao": cartao,
        "cupom": "",
    })


@when(
    parsers.parse('o cliente compra com cupom "{cupom}" e cartão "{cartao}"'),
    target_fixture="resposta",
)
def comprar_com_cupom(client, ctx, cupom, cartao):
    return client.post("/api/comprar", json={
        "produto": ctx["produto"],
        "cartao": cartao,
        "cupom": cupom,
    })


@then(parsers.parse("a compra é aprovada com valor de R$ {valor:f}"))
def compra_aprovada_com_valor(resposta, valor):
    assert resposta.status_code == 200
    assert resposta.json()["valor_pago"] == pytest.approx(valor)


@then(parsers.parse("o valor pago é R$ {valor:f}"))
def valor_pago_correto(resposta, valor):
    assert resposta.status_code == 200
    assert resposta.json()["valor_pago"] == pytest.approx(valor)
