from flask import Blueprint, request
from .localizacao_service import LocalizacaoService

class LocalizacaoController:
    
    blueprint = Blueprint('localizacao', __name__)

    @staticmethod
    @blueprint.route('/api/localizacao', methods=['POST'])
    def criar_localizacao():
        
        return LocalizacaoService.handle_criar_localizacao(request)

    @staticmethod
    @blueprint.route('/api/localizacoes', methods=['GET'])
    def listar_localizacoes():
        
        return LocalizacaoService.listar_localizacoes()

    @staticmethod
    @blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['GET'])
    def obter_localizacao(localizacao_id):
        
        return LocalizacaoService.obter_localizacao(localizacao_id)

    @staticmethod
    @blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['PUT'])
    def atualizar_localizacao(localizacao_id):
        
        return LocalizacaoService.handle_atualizar_localizacao(localizacao_id, request)

    @staticmethod
    @blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['DELETE'])
    def deletar_localizacao(localizacao_id):
        
        return LocalizacaoService.deletar_localizacao(localizacao_id)


localizacao_blueprint = LocalizacaoController.blueprint