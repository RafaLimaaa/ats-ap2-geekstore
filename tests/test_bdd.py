import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/compra.feature")


# Fixture de contexto compartilhado — pytest-bdd não tem objeto "context" como o Behave,
# então usamos um dict mutável para passar estado entre steps do mesmo cenário.
@pytest.fixture
def ctx():
    return {}


@given(parsers.parse('que o produto "{nome}" está disponível no estoque'), target_fixture="ctx")
def produto_disponivel(ctx, nome):
    ctx["produto"] = nome
    return ctx


@given(parsers.parse('que o produto "{nome}" está sem estoque'), target_fixture="ctx")
def produto_sem_estoque(ctx, nome):
    ctx["produto"] = nome
    return ctx


@when(
    parsers.parse('eu realizo a compra com o cartão "{cartao}" sem cupom'),
    target_fixture="resposta",
)
def comprar_sem_cupom(client, ctx, cartao):
    produto = ctx.get("produto", "teclado")
    return client.post("/api/comprar", json={
        "produto": produto,
        "cartao": cartao,
        "cupom": "",
    })


@when(
    parsers.parse('eu realizo a compra com o cartão "{cartao}" e o cupom "{cupom}"'),
    target_fixture="resposta",
)
def comprar_com_cupom(client, ctx, cartao, cupom):
    produto = ctx.get("produto", "teclado")
    return client.post("/api/comprar", json={
        "produto": produto,
        "cartao": cartao,
        "cupom": cupom,
    })


@when(
    parsers.parse('eu tento comprar o produto "{produto}" com o cartão "{cartao}"'),
    target_fixture="resposta",
)
def comprar_produto_qualquer(client, produto, cartao):
    return client.post("/api/comprar", json={
        "produto": produto,
        "cartao": cartao,
        "cupom": "",
    })


@then(parsers.parse("a resposta deve ter status {codigo:d}"))
def verificar_status(resposta, codigo):
    assert resposta.status_code == codigo


@then(parsers.parse("o valor pago deve ser {valor:f}"))
def verificar_valor_pago(resposta, valor):
    assert resposta.json()["valor_pago"] == pytest.approx(valor)


@then("a mensagem deve confirmar a aprovação")
def verificar_mensagem_aprovacao(resposta):
    assert "aprovada" in resposta.json()["mensagem"].lower()
