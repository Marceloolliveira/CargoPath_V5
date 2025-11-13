from flask import Blueprint, request, jsonify
from .cubagem_service import CubagemService

cubagem_blueprint = Blueprint('cubagem', __name__, url_prefix='/api/cubagem')

@cubagem_blueprint.route('/', methods=['POST'])
def criar_cubagem():
    try:
        data = request.json
        cubagem_id = CubagemService.criar_cubagem(
            data.get('altura'),
            data.get('largura'),
            data.get('comprimento'),
            data.get('qtd'),
            data.get('carga_id')
        )

        return jsonify({
            "cubagem_id": cubagem_id,
            "message": "Cubagem criada com sucesso!"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cubagem_blueprint.route('/', methods=['GET'])
def listar_cubagens():
    cubagens = CubagemService.listar_cubagens()
    cubagens_list = [
        {
            "cubagem_id": c[0],
            "altura": c[1],
            "largura": c[2],
            "comprimento": c[3],
            "qtd": c[4],
            "carga_id": c[5],
            "created_at": c[6],
        } for c in cubagens
    ]
    return jsonify(cubagens_list), 200


@cubagem_blueprint.route('/<int:cubagem_id>', methods=['GET'])
def obter_cubagem(cubagem_id):
    cubagem = CubagemService.obter_cubagem(cubagem_id)
    if not cubagem:
        return jsonify({"message": "Cubagem não encontrada"}), 404

    cubagem_detalhe = {
        "cubagem_id": cubagem[0],
        "altura": cubagem[1],
        "largura": cubagem[2],
        "comprimento": cubagem[3],
        "qtd": cubagem[4],
        "carga_id": cubagem[5],
        "created_at": cubagem[6]
    }
    return jsonify(cubagem_detalhe), 200


@cubagem_blueprint.route('/<int:cubagem_id>', methods=['PUT'])
def atualizar_cubagem(cubagem_id):
    data = request.json
    try:
        CubagemService.atualizar_cubagem(
            cubagem_id,
            data.get('altura'),
            data.get('largura'),
            data.get('comprimento'),
            data.get('qtd')
        )
        return jsonify({"message": "Cubagem atualizada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cubagem_blueprint.route('/<int:cubagem_id>', methods=['DELETE'])
def deletar_cubagem(cubagem_id):
    try:
        CubagemService.deletar_cubagem(cubagem_id)
        return jsonify({"message": "Cubagem deletada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
