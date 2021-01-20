from .views import index
from .resources import Login, User, Holding, HoldingAddExit, Note, HoldingList, Fund


def web_routes(blueprint):
    blueprint.add_url_rule('', endpoint='index',
                           view_func=index, methods=["GET"])


def api_routes(api):
    api.add_resource(Login, '/login')
    api.add_resource(User, '/user')
    api.add_resource(HoldingList, '/holding_list')
    api.add_resource(Holding, '/holding', '/holding/<int:id>')
    api.add_resource(HoldingAddExit, '/holding/add_exit')
    api.add_resource(Note, '/holding/<int:holding_id>/note',
                     '/holding/<int:holding_id>/note/<int:id>')
    api.add_resource(Fund, '/fund', '/fund/add_withdraw')
