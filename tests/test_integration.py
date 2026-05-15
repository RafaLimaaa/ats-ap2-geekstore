import sqlite3
import pytest


class TestListarProdutos:
    def test_retorna_200_com_lista(self, client):
        resp = client.get("/api/produtos")
        assert resp.status_code == 200

    def test_estrutura_de_cada_produto(self, client):
        produtos = client.get("/api/produtos").json()
        assert len(produtos) >= 1
        for p in produtos:
            assert "nome" in p
            assert "preco" in p
            assert "estoque" in p

    def test_teclado_presente_com_estoque(self, client):
        produtos = client.get("/api/produtos").json()
        teclado = next((p for p in produtos if p["nome"] == "teclado"), None)
        assert teclado is not None
        assert teclado["preco"] == pytest.approx(200.0)
        assert teclado["estoque"] == 10


class TestComprar:
    CARTAO = "1234 5678 9012 3456"

    def test_compra_teclado_retorna_200(self, client):
        resp = client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": self.CARTAO,
        })
        assert resp.status_code == 200

    def test_compra_retorna_campos_esperados(self, client):
        corpo = client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": self.CARTAO,
        }).json()
        assert corpo["status"] == "sucesso"
        assert "mensagem" in corpo
        assert "valor_pago" in corpo

    def test_compra_sem_cupom_cobra_preco_cheio(self, client):
        corpo = client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": self.CARTAO,
        }).json()
        assert corpo["valor_pago"] == pytest.approx(200.0)

    def test_cupom_geek20_aplica_desconto(self, client):
        corpo = client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": self.CARTAO,
            "cupom": "GEEK20",
        }).json()
        assert corpo["valor_pago"] == pytest.approx(160.0)

    def test_produto_inexistente_retorna_404(self, client):
        resp = client.post("/api/comprar", json={
            "produto": "monitor",
            "cartao": self.CARTAO,
        })
        assert resp.status_code == 404

    def test_mouse_sem_estoque_retorna_400(self, client):
        # mouse foi semeado com estoque=0 exatamente para cobrir esse caminho
        resp = client.post("/api/comprar", json={
            "produto": "mouse",
            "cartao": self.CARTAO,
        })
        assert resp.status_code == 400
        assert "estoque" in resp.json()["detail"].lower()

    def test_estoque_decrementa_apos_compra(self, client, db):
        client.post("/api/comprar", json={
            "produto": "teclado",
            "cartao": self.CARTAO,
        })
        conn = sqlite3.connect(db)
        row = conn.execute(
            "SELECT estoque FROM produtos WHERE nome = 'teclado'"
        ).fetchone()
        conn.close()
        assert row[0] == 9

    def test_compras_multiplas_decrementam_acumulativamente(self, client, db):
        for _ in range(3):
            client.post("/api/comprar", json={
                "produto": "teclado",
                "cartao": self.CARTAO,
            })
        conn = sqlite3.connect(db)
        row = conn.execute(
            "SELECT estoque FROM produtos WHERE nome = 'teclado'"
        ).fetchone()
        conn.close()
        assert row[0] == 7
