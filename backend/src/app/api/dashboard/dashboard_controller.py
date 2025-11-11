from flask import Blueprint, request, jsonify
from ...services.dashboard_service import DashboardService

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_blueprint.route('/', methods=['GET'])
def get_dashboard_summary():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "O user_id é obrigatório."}), 400

    try:
        summary = DashboardService.get_dashboard_summary(user_id, start_date, end_date)
        return jsonify(summary), 200
    except Exception as e:
        print(f"Erro ao carregar o resumo do dashboard: {e}")
        return jsonify({"error": str(e)}), 500
