from flask import Blueprint, request, jsonify
from .cotacao_service import CotacaoService

cotacao_blueprint = Blueprint('cotacao', __name__, url_prefix='/api/cotacao')
cotacao_service = CotacaoService()

# Criar cotação
@cotacao_blueprint.route('/', methods=['POST'])
def criar_cotacao():
    try:
        data = request.get_json()
        result = cotacao_service.criar_cotacao(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Listar todas
@cotacao_blueprint.route('/', methods=['GET'])
def listar_cotacoes():
    try:
        result = cotacao_service.listar_cotacoes()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Buscar por ID
@cotacao_blueprint.route('/<int:cotacao_id>', methods=['GET'])
def obter_cotacao(cotacao_id):
    try:
        result = cotacao_service.obter_cotacao(cotacao_id)
        if result:
            return jsonify(result), 200
        return jsonify({"message": "Cotação não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Atualizar
@cotacao_blueprint.route('/<int:cotacao_id>', methods=['PUT'])
def atualizar_cotacao(cotacao_id):
    try:
        data = request.get_json()
        result = cotacao_service.atualizar_cotacao(cotacao_id, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Deletar
@cotacao_blueprint.route('/<int:cotacao_id>', methods=['DELETE'])
def deletar_cotacao(cotacao_id):
    try:
        cotacao_service.deletar_cotacao(cotacao_id)
        return jsonify({"message": "Cotação deletada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Resumo por ID
@cotacao_blueprint.route('/resumo/<int:cotacao_id>', methods=['GET'])
def obter_resumo(cotacao_id):
    try:
        result = cotacao_service.obter_resumo_cotacao(cotacao_id)
        if result:
            return jsonify(result), 200
        return jsonify({"message": "Cotação não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Coletas por usuário
@cotacao_blueprint.route('/user/<int:user_id>/coletas', methods=['GET'])
def listar_coletas_por_usuario(user_id):
    try:
        result = cotacao_service.listar_coletas_por_usuario(user_id)
        if result:
            return jsonify(result), 200
        return jsonify({"message": "Nenhuma coleta encontrada."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Histórico
@cotacao_blueprint.route('/user/<int:user_id>/historico', methods=['GET'])
def obter_historico(user_id):
    try:
        result = cotacao_service.obter_historico(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Faturas
@cotacao_blueprint.route('/user/<int:user_id>/faturas', methods=['GET'])
def listar_faturas_pagas(user_id):
    try:
        result = cotacao_service.listar_faturas_pagas(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
