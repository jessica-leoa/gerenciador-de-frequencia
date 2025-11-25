from flask import Blueprint, request, jsonify
from services.turma_service import (
    create_turma, get_turmas, get_turma, update_turma, delete_turma
)

turma_bp = Blueprint("turmas", __name__)

@turma_bp.post("/")
def create():
    data = request.json
    turma = create_turma(data)
    return jsonify({"id": turma.id, "nome": turma.nome, "carga_horaria": turma.carga_horaria})

@turma_bp.get("/")
def list_all():
    turmas = get_turmas()
    return jsonify([
        {"id": s.id, "nome": s.nome, "carga_horaria": s.carga_horaria} for s in turmas
    ])

@turma_bp.get("/<int:id>")
def get_one(id):
    turma = get_turma(id)
    if not turma:
        return jsonify({"error": "turma not found"}), 404
    return jsonify({"id": turma.id, "nome": turma.nome, "carga_horaria": turma.carga_horaria})

@turma_bp.put("/<int:id>")
def update(id):
    data = request.json
    turma = update_turma(id, data)
    if not turma:
        return jsonify({"error": "turma not found"}), 404
    return jsonify({"id": turma.id, "nome": turma.nome, "carga_horaria": turma.carga_horaria})

@turma_bp.delete("/<int:id>")
def delete(id):
    ok = delete_turma(id)
    if not ok:
        return jsonify({"error": "turma not found"}), 404
    return jsonify({"message": "Deleted"})