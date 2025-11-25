from flask import Blueprint, request, jsonify
from services.aluno_service import (
    create_aluno, get_alunos, get_aluno, update_aluno, delete_aluno
)

aluno_bp = Blueprint("alunos", __name__)

@aluno_bp.post("/")
def create():
    data = request.json
    aluno = create_aluno(data)
    return jsonify({"id": aluno.id, "nome": aluno.nome, "matricula": aluno.matricula})

@aluno_bp.get("/")
def list_all():
    alunos = get_alunos()
    return jsonify([
        {"id": s.id, "nome": s.nome, "matricula": s.matricula} for s in alunos
    ])

@aluno_bp.get("/<int:id>")
def get_one(id):
    aluno = get_aluno(id)
    if not aluno:
        return jsonify({"error": "aluno not found"}), 404
    return jsonify({"id": aluno.id, "nome": aluno.nome, "matricula": aluno.matricula})

@aluno_bp.put("/<int:id>")
def update(id):
    data = request.json
    aluno = update_aluno(id, data)
    if not aluno:
        return jsonify({"error": "aluno not found"}), 404
    return jsonify({"id": aluno.id, "nome": aluno.nome, "matricula": aluno.matricula})

@aluno_bp.delete("/<int:id>")
def delete(id):
    ok = delete_aluno(id)
    if not ok:
        return jsonify({"error": "aluno not found"}), 404
    return jsonify({"message": "Deleted"})