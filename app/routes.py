from flask import Blueprint, request, jsonify
from app.models import Dados
from app import db

bp = Blueprint("main", __name__)


# Endpoint para salvar dados enviados pelo Streamlit
@bp.route("/dados", methods=["POST"])
def salvar_dados():
    data = request.json

    # Criar instância do modelo e salvar no banco de dados
    novo_dado = Dados(nome=data.get("nome"), email=data.get("email"))
    db.session.add(novo_dado)
    db.session.commit()

    return jsonify({"mensagem": "Dados salvos com sucesso!"}), 201


# Endpoint para listar todos os dados (opcional)
@bp.route("/dados", methods=["GET"])
def listar_dados():
    dados = Dados.query.all()
    return jsonify([{"id": d.id, "nome": d.nome, "email": d.email} for d in dados])
