from flask import Blueprint, request, jsonify
from services.aula_service import (
    create_aula, get_all_aulas, get_aula_by_id,
    update_aula, delete_aula
)

aula_bp = Blueprint("aulas", __name__)

# CREATE
@aula_bp.post("/")
def create():
    data = request.get_json()
    aula = create_aula(data)
    return jsonify({"id": aula.id}), 201


# GET ALL
@aula_bp.get("/")
def get_all():
    aulas = get_all_aulas()
    result = []
    for aula in aulas:
        result.append({
            "id": aula.id,
            "turma_id": aula.turma_id,
            "data_aula": aula.data_aula.isoformat()
        })
    return jsonify(result)


# GET by ID (com nome da turma via service)
@aula_bp.get("/<int:id>")
def get_one(id):
    data = get_aula_by_id(id)
    if not data:
        return jsonify({"error": "Aula não encontrada"}), 404
    return jsonify(data)


# UPDATE
@aula_bp.put("/<int:id>")
def update(id):
    data = request.get_json()
    aula = update_aula(id, data)
    if not aula:
        return jsonify({"error": "Aula não encontrada"}), 404
    return jsonify({"message": "Atualizada"})


# DELETE
@aula_bp.delete("/<int:id>")
def delete(id):
    ok = delete_aula(id)
    if not ok:
        return jsonify({"error": "Aula não encontrada"}), 404
    return jsonify({"message": "Removida"})
