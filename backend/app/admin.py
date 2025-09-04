from flask_admin.contrib.sqla import ModelView
from flask import request, Response
import os

class SecureModelView(ModelView):
    column_list = ['session_id', 'user_id', 'status', 'created_at']
    column_filters = ['status']
    column_searchable_list = ['session_id', 'user_id']
    can_create = False
    can_edit = False
    can_delete = False

    def is_accessible(self):
        auth = request.authorization
        return (
            auth and
            auth.username == os.getenv("ADMIN_USERNAME") and
            auth.password == os.getenv("ADMIN_PASSWORD")
        )

    def inaccessible_callback(self, name, **kwargs):
        return Response(
            "Access denied. Please provide valid admin credentials.",
            401,
            {"WWW-Authenticate": "Basic realm='Login Required'"}
        )
