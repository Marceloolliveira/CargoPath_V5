from flask import Blueprint, request, jsonify
from .embalagem_service import EmbalagemService

embalagem_blueprint = Blueprint('embalagem', __name__)

@embalagem_blueprint.route('/api/embalagem', methods=['POST'])
def criar_embalagem():
    data = request.json
    try:
        embalagem = EmbalagemService.criar_embalagem(data)
        return jsonify(embalagem), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@embalagem_blueprint.route('/api/embalagens', methods=['GET'])
def listar_embalagens():
    try:
        embalagens = EmbalagemService.listar_embalagens()
        return jsonify(embalagens), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@embalagem_blueprint.route('/api/embalagem/<int:embalagem_id>', methods=['GET'])
def obter_embalagem(embalagem_id):
    try:
        embalagem = EmbalagemService.obter_embalagem(embalagem_id)
        if embalagem:
            return jsonify(embalagem), 200
        return jsonify({"message": "Embalagem não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@embalagem_blueprint.route('/api/embalagem/<int:embalagem_id>', methods=['PUT'])
def atualizar_embalagem(embalagem_id):
    data = request.json
    try:
        embalagem = EmbalagemService.atualizar_embalagem(embalagem_id, data)
        return jsonify(embalagem), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@embalagem_blueprint.route('/api/embalagem/<int:embalagem_id>', methods=['DELETE'])
def deletar_embalagem(embalagem_id):
    try:
        resultado = EmbalagemService.deletar_embalagem(embalagem_id)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
