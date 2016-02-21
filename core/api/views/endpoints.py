from flask import Module, jsonify, request
from flask.views import MethodView

from core.utils.RequestValidator import CreateUnikernelValidator
from core.api.decorators import jsonp

api = Module(
    __name__,
    url_prefix='/api'
)


def jsonify_status_code(*args, **kw):
    response = jsonify(*args, **kw)
    response.status_code = kw['code']
    return response


@api.route('/')
def index():
    """
    The root of the API returns an error
    """
    return jsonify_status_code(
        code=400,
        message='Room no 404: File not found'
    )


class CreateUnikernel(MethodView):
    @jsonp
    def get(self):
        return jsonify_status_code(
            code=405,
            message='HTTP method GET is not allowed for this URL'
        )

    @jsonp
    def post(self):
        content = request.get_json(force=False, silent=True)
        if not content:
            return jsonify_status_code(
                code=400,
                message='Bad HTTP POST request'
            )
        else:
            # Validate JSON
            if not CreateUnikernelValidator.validate(content):
                return jsonify_status_code(
                    code=400,
                    message='HTTP POST request data is invalid. Refer to the Dune API documentation for details.'
                )
            else:
                # do something
                pass


CreateUnikernel_view = CreateUnikernel.as_view('create_unikernel')
api.add_url_rule(
    '/unikernel/create',
    view_func=CreateUnikernel_view,
    methods=['GET', 'POST']
)
