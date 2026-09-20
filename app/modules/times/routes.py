from flask import render_template, flash, redirect, url_for
from . import times_bp
from .forms import TimeForm
from .services import TimeService, ErroDeNegocio


@times_bp.route("/", methods=["GET"])
def busca_page():
    return render_template("busca.html")


@times_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_page():
    form = TimeForm()
    service = TimeService()

    if form.validate_on_submit():
        try:
            service.cadastrar(
                nome=str(form.nome.data or "").strip(),      # 👈 normaliza
                id_sofascore=form.codigo_sofascore.data,     # já aceita None
            )
            flash("Time cadastrado com sucesso! ⚽", "success")
            return redirect(url_for("times.cadastrar_page"))
        except ErroDeNegocio as e:
            flash(str(e), "danger")

    return render_template("cadastrar.html", form=form)


@times_bp.route("/lista", methods=["GET"])
def lista_page():
    service = TimeService()
    times = service.listar()
    return render_template("lista.html", times=times)