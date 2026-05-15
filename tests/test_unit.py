import pytest
from unittest.mock import MagicMock

from main import calcular_desconto, processar_pedido, GatewayPagamento


class TestCalcularDesconto:
    def test_cupom_geek20_aplica_vinte_porcento(self):
        assert calcular_desconto(200.0, "GEEK20") == pytest.approx(160.0)

    def test_cupom_invalido_nao_altera_valor(self):
        assert calcular_desconto(200.0, "INVALIDO") == pytest.approx(200.0)

    def test_sem_cupom_retorna_valor_original(self):
        assert calcular_desconto(150.0, "") == pytest.approx(150.0)

    def test_desconto_preserva_casas_decimais(self):
        # R$99,90 com 20% de desconto → R$79,92
        assert calcular_desconto(99.90, "GEEK20") == pytest.approx(79.92)


class TestProcessarPedido:
    def _gateway_aprovado(self) -> GatewayPagamento:
        gw = MagicMock(spec=GatewayPagamento)
        gw.cobrar.return_value = True
        return gw

    def _gateway_recusado(self) -> GatewayPagamento:
        gw = MagicMock(spec=GatewayPagamento)
        gw.cobrar.return_value = False
        return gw

    def test_pagamento_aprovado_retorna_mensagem(self):
        gw = self._gateway_aprovado()
        resultado = processar_pedido(200.0, "1234 5678 9012 3456", gw)
        assert resultado == "Compra aprovada!"

    def test_valor_zero_levanta_value_error(self):
        gw = self._gateway_aprovado()
        with pytest.raises(ValueError, match="maior que zero"):
            processar_pedido(0, "1234 5678 9012 3456", gw)

    def test_valor_negativo_levanta_value_error(self):
        gw = self._gateway_aprovado()
        with pytest.raises(ValueError, match="maior que zero"):
            processar_pedido(-50.0, "1234 5678 9012 3456", gw)

    def test_gateway_recusa_levanta_value_error(self):
        gw = self._gateway_recusado()
        with pytest.raises(ValueError, match="recusado"):
            processar_pedido(200.0, "1234 5678 9012 3456", gw)

    def test_gateway_cobrar_chamado_com_valor_correto(self):
        gw = self._gateway_aprovado()
        processar_pedido(160.0, "9999 8888 7777 6666", gw)
        gw.cobrar.assert_called_once_with("9999 8888 7777 6666", 160.0)
