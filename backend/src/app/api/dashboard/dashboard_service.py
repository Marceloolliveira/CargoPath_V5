from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

class DashboardService:
    @staticmethod
    def get_dashboard_summary(user_id, start_date=None, end_date=None):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        if cursor is None:
            raise Exception("Erro ao conectar ao banco de dados")

        try:
            query = 
            params = [user_id]

            if start_date and end_date:
                query += " AND data_agendamento BETWEEN %s AND %s"
                params.extend([start_date, end_date])

            cursor.execute(query, params)
            result = cursor.fetchone()

            return {
                "total": result[0] or 0,
                "pending": result[1] or 0,
                "completed": result[2] or 0,
                "cancelled": result[3] or 0
            }

        finally:
            cursor.close()
            db.close()
