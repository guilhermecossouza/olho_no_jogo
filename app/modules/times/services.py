from typing import Optional

from app.extensions import db
from .repository import TimeRepository


class ErroDeNegocio(Exception):
    """Erro esperado, com mensagem amigável para o usuário."""
    pass


class TimeService:
    def __init__(self):
        self.repo = TimeRepository()

    def cadastrar(self, nome: Optional[str], id_sofascore: Optional[int] = None) -> dict:
        """
        Cadastra um novo time.
        Aceita nome opcional; valida e normaliza internamente.
        """
        nome = (nome or "").strip()      # 👈 defesa + normalização

        # Regra 1: nome obrigatório (após normalizar)
        if not nome:
            raise ErroDeNegocio("O nome do time é obrigatório.")

        # Regra 2: nome duplicado
        if self.repo.existe_com_nome(nome):
            raise ErroDeNegocio(f"Já existe um time cadastrado com o nome '{nome}'.")

        # Regra 3: SofaScore duplicado (só se informado)
        if id_sofascore is not None:
            if self.repo.existe_com_sofascore(id_sofascore):
                raise ErroDeNegocio(
                    f"Já existe um time com o código SofaScore {id_sofascore}."
                )

        try:
            time = self.repo.criar(nome=nome, id_sofascore=id_sofascore)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ErroDeNegocio(f"Erro ao salvar no banco: {e}")

        return {
            "idTime": time.idTime,
            "name": time.name,
            "idSofascore": time.idSofascore,
        }

    def listar(self, ordem: str = "asc") -> list[dict]:
        return [
            {"idTime": t.idTime, "name": t.name, "idSofascore": t.idSofascore}
            for t in self.repo.listar_todos(ordem=ordem)
        ]