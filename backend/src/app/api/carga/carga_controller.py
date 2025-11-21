from flask import Blueprint, request, jsonify
from .carga_service import CargaService

carga_blueprint = Blueprint('carga', __name__)
carga_service = CargaService()


@carga_blueprint.route('/api/carga', methods=['POST'])
def criar_carga():
    try:
        data = request.get_json()
        valor = data.get('valor')
        peso = data.get('peso')
        volumes = data.get('volumes')
        cotacao_id = data.get('cotacao_id')

        if not all([valor, peso, volumes, cotacao_id]):
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        carga = carga_service.criar_carga(valor, peso, volumes, cotacao_id)
        return jsonify(carga), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@carga_blueprint.route('/api/cargas', methods=['GET'])
def listar_cargas():
    try:
        cargas = carga_service.listar_cargas()
        return jsonify(cargas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@carga_blueprint.route('/api/carga/<int:carga_id>', methods=['GET'])
def obter_carga(carga_id):
    try:
        carga = carga_service.obter_carga(carga_id)
        if carga:
            return jsonify(carga), 200
        return jsonify({"message": "Carga não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@carga_blueprint.route('/api/carga/<int:carga_id>', methods=['PUT'])
def atualizar_carga(carga_id):
    try:
        data = request.get_json()
        valor = data.get('valor')
        peso = data.get('peso')
        volumes = data.get('volumes')

        if not all([valor, peso, volumes]):
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        carga = carga_service.atualizar_carga(carga_id, valor, peso, volumes)
        return jsonify(carga), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@carga_blueprint.route('/api/carga/<int:carga_id>', methods=['DELETE'])
def deletar_carga(carga_id):
    try:
        carga_service.deletar_carga(carga_id)
        return jsonify({"message": "Carga deletada com sucesso!", "carga_id": carga_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
