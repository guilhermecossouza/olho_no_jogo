from typing import Optional

from app.modules.times.repository import TimeRepository
from app.modules.times.models import TimeModel

import json


class ErroDeNegocio(Exception):
    """Erro esperado, com mensagem amigável para o usuário."""
    pass


class TimeService:
    def __init__(self):
        self.repo = TimeRepository()

    # ---------- cadastro em lote (JSON) ----------

    def processa_statistica_partida(self, form: dict) -> dict:
        try:
            statistic_json = json.loads(form["json"])
        except (KeyError, json.JSONDecodeError) as e:
            raise ErroDeNegocio(f"JSON inválido: {e}")

        criados = 0
        ignorados = 0
        erros = []

        for standing in statistic_json.get("standings", []):
            for row in standing.get("rows", []):
                team = row.get("team", {})
                name = f"{team.get('name', '')} ({team.get('shortName', '')})".strip()
                id_sofascore = team.get("id")

                try:
                    self.cadastrar(nome=name, id_sofascore=id_sofascore)
                    criados += 1
                except ErroDeNegocio as e:
                    ignorados += 1
                    erros.append(str(e))

        return {"criados": criados, "ignorados": ignorados, "erros": erros}

    # ---------- CRUD ----------

    def cadastrar(self, nome: Optional[str], id_sofascore: Optional[int] = None) -> TimeModel:
        nome = (nome or "").strip()

        if not nome:
            raise ErroDeNegocio("O nome do time é obrigatório.")

        if self.repo.existe_com_nome(nome):
            raise ErroDeNegocio(f"Já existe um time com o nome '{nome}'.")

        if id_sofascore is not None and self.repo.existe_com_sofascore(id_sofascore):
            raise ErroDeNegocio(f"Já existe um time com o código SofaScore {id_sofascore}.")

        return self.repo.criar(nome=nome, id_sofascore=id_sofascore)

    def atualizar(self, id_time: int, nome: str, id_sofascore: Optional[int]) -> TimeModel:
        nome = (nome or "").strip()

        if not nome:
            raise ErroDeNegocio("O nome do time é obrigatório.")

        time = self.repo.buscar_por_id(id_time)
        if time is None:
            raise ErroDeNegocio(f"Time com id {id_time} não encontrado.")

        if self.repo.existe_com_nome(nome, ignorar_id=id_time):
            raise ErroDeNegocio(f"Já existe outro time com o nome '{nome}'.")

        if id_sofascore is not None and self.repo.existe_com_sofascore(id_sofascore, ignorar_id=id_time):
            raise ErroDeNegocio(f"Já existe outro time com o código SofaScore {id_sofascore}.")

        return self.repo.atualizar(
            time=time,
            campos={"name": nome, "idSofascore": id_sofascore},
        )

    def deletar(self, id_time: int) -> None:
        time = self.repo.buscar_por_id(id_time)
        if time is None:
            raise ErroDeNegocio(f"Time com id {id_time} não encontrado.")
        self.repo.deletar(time)

    def listar_todos(self) -> list[TimeModel]:
        return self.repo.listar_todos()

    def buscar_por_id(self, id_time: int) -> Optional[TimeModel]:
        return self.repo.buscar_por_id(id_time)