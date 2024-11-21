from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
@dashboard_blueprint.route('/', methods=['GET'])
def get_dashboard_summary():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    user_id = request.args.get('user_id')  # Obtém o user_id da requisição

    if not user_id:
        return jsonify({"error": "O user_id é obrigatório."}), 400

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        query = """
            SELECT 
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN status = 'finalizado' THEN 1 ELSE 0 END) AS completed,
                SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS cancelled
            FROM cotacoes
            WHERE user_id = %s
        """
        params = [user_id]

        if start_date and end_date:
            query += " AND data_agendamento BETWEEN %s AND %s"
            params.extend([start_date, end_date])

        cursor.execute(query, params)
        result = cursor.fetchone()

        summary = {
            "total": result[0] or 0,
            "pending": result[1] or 0,
            "completed": result[2] or 0,
            "cancelled": result[3] or 0
        }
        return jsonify(summary), 200

    except Exception as e:
        print(f"Erro ao carregar o resumo do dashboard: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        db.close()

