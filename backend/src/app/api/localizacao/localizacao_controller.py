from flask import Blueprint, request
from .localizacao_service import LocalizacaoService

class LocalizacaoController:
    # Criação do Blueprint
    blueprint = Blueprint('localizacao', __name__)

    @staticmethod
    @blueprint.route('/api/localizacao', methods=['POST'])
    def criar_localizacao():
        """
        Controller para criar uma nova localização
        """
        return LocalizacaoService.handle_criar_localizacao(request)

    @staticmethod
    @blueprint.route('/api/localizacoes', methods=['GET'])
    def listar_localizacoes():
        """
        Controller para listar todas as localizações
        """
        return LocalizacaoService.listar_localizacoes()

    @staticmethod
    @blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['GET'])
    def obter_localizacao(localizacao_id):
        """
        Controller para obter uma localização específica
        """
        return LocalizacaoService.obter_localizacao(localizacao_id)

    @staticmethod
    @blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['PUT'])
    def atualizar_localizacao(localizacao_id):
        """
        Controller para atualizar uma localização
        """
        return LocalizacaoService.handle_atualizar_localizacao(localizacao_id, request)

    @staticmethod
    @blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['DELETE'])
    def deletar_localizacao(localizacao_id):
        """
        Controller para deletar uma localização
        """
        return LocalizacaoService.deletar_localizacao(localizacao_id)

# Exporta o blueprint para ser usado no app.py
localizacao_blueprint = LocalizacaoController.blueprint