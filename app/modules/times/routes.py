from flask import render_template, flash, redirect, url_for, abort
from typing import Optional

from . import times_bp
from .forms import TimeForm, TimeJsonForm
from .services import TimeService, ErroDeNegocio

import logging

logger = logging.getLogger(__name__)


# ============================================================
# LISTAGEM
# ============================================================

@times_bp.route("/", methods=["GET"])
def busca_page():
    service = TimeService()
    times = service.listar_todos()
    return render_template("busca.html", times=times)


# ============================================================
# CADASTRAR / EDITAR
# ============================================================

@times_bp.route("/cadastrar", methods=["GET", "POST"])
@times_bp.route("/cadastrar/<int:id>", methods=["GET", "POST"])
def cadastrar_page(id: Optional[int] = None):
    service = TimeService()
    time = None

    # --- modo edição: valida se o ID existe ---
    if id is not None:
        time = service.buscar_por_id(id)
        if time is None:
            flash(f"Time com id {id} não encontrado.", "warning")
            return redirect(url_for("times.busca_page"))

    form = TimeForm(time=time)

    if form.validate_on_submit():
        try:
            id_time = form.id_time.data or None

            if id_time is None:
                service.cadastrar(
                    nome=form.nome.data,
                    id_sofascore=form.codigo_sofascore.data,
                )
                flash("Time cadastrado com sucesso!", "success")
            else:
                service.atualizar(
                    id_time=int(id_time),
                    nome=form.nome.data,
                    id_sofascore=form.codigo_sofascore.data,
                )
                flash("Time atualizado com sucesso!", "success")

            return redirect(url_for("times.busca_page"))

        except ErroDeNegocio as e:
            flash(str(e), "danger")
        except Exception:
            logger.exception("Erro inesperado ao salvar time")
            flash("Erro inesperado ao salvar. Contate o suporte.", "danger")

    # se caiu aqui, é GET ou form com erro de validação
    return render_template("cadastrar.html", form=form)


# ============================================================
# DELETAR
# ============================================================

@times_bp.route("/deletar/<int:id>", methods=["POST"])
def deletar_page(id: int):
    service = TimeService()
    try:
        service.deletar(id)
        flash("Time removido com sucesso!", "success")
    except ErroDeNegocio as e:
        flash(str(e), "danger")
    except Exception:
        logger.exception("Erro inesperado ao deletar time")
        flash("Erro inesperado ao deletar.", "danger")

    return redirect(url_for("times.busca_page"))


# ============================================================
# CADASTRO EM LOTE (JSON)
# ============================================================

@times_bp.route("/cadastrar/json", methods=["GET", "POST"])
def cadastra_time_json():
    form = TimeJsonForm()

    if form.validate_on_submit():
        try:
            service = TimeService()
            resultado = service.processa_statistica_partida(form.data)

            flash(
                f"Cadastro em lote: {resultado['criados']} criados, "
                f"{resultado['ignorados']} ignorados.",
                "info",
            )
            if resultado["erros"]:
                for erro in resultado["erros"][:5]:
                    flash(erro, "warning")

            return redirect(url_for("times.busca_page"))

        except ErroDeNegocio as e:
            flash(str(e), "danger")
        except Exception:
            logger.exception("Erro inesperado no cadastro em lote")
            flash("Erro inesperado no cadastro em lote.", "danger")

    return render_template("cadastrar_json.html", form=form)