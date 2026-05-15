import pytest
from unittest.mock import MagicMock

from main import app, get_gateway, GatewayPagamento


CARTAO = "1234 5678 9012 3456"


@pytest.fixture(autouse=True)
def _reset_overrides():
    yield
    # Garante que overrides de um teste não vazem para o próximo
    app.dependency_overrides.clear()


def _mock_gateway(aprovado: bool = True) -> GatewayPagamento:
    gw = MagicMock(spec=GatewayPagamento)
    gw.cobrar.return_value = aprovado
    return gw


def _inject(gw: GatewayPagamento) -> None:
    app.dependency_overrides[get_gateway] = lambda: gw


class TestGatewayIsolado:
    def test_cobrar_chamado_uma_vez_com_valor_correto(self, client):
        gw = _mock_gateway()
        _inject(gw)

        client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": CARTAO,
        })

        gw.cobrar.assert_called_once_with(CARTAO, 200.0)

    def test_cobrar_com_desconto_geek20(self, client):
        gw = _mock_gateway()
        _inject(gw)

        client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": CARTAO,
            "cupom": "GEEK20",
        })

        gw.cobrar.assert_called_once_with(CARTAO, 160.0)

    def test_gateway_nao_chamado_para_produto_inexistente(self, client):
        gw = _mock_gateway()
        _inject(gw)

        resp = client.post("/api/comprar", json={
            "produto": "produto_que_nao_existe",
            "cartao": CARTAO,
        })

        assert resp.status_code == 404
        gw.cobrar.assert_not_called()

    def test_gateway_recusa_retorna_400(self, client):
        gw = _mock_gateway(aprovado=False)
        _inject(gw)

        resp = client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": CARTAO,
        })

        assert resp.status_code == 400
        assert "recusado" in resp.json()["detail"].lower()

    def test_gateway_nao_chamado_quando_sem_estoque(self, client):
        gw = _mock_gateway()
        _inject(gw)

        # mouse foi semeado com estoque=0
        resp = client.post("/api/comprar", json={
            "produto": "mouse",
            "cartao": CARTAO,
        })

        assert resp.status_code == 400
        gw.cobrar.assert_not_called()
