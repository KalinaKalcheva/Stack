import multiprocessing

from flask import Flask, jsonify
from flask_restful import Resource, Api
from apispec import APISpec

from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from waitress import serve

from exceptions.stack_exceptions import InternalError
from schemas.stack_schemas import StackPushRequestSchema, StackResponseSchema
from services.stack_service import is_input_valid, push, pop, max, is_empty, get_stack

THREAD_COUNT = multiprocessing.cpu_count() * 2 + 1

app = Flask(__name__)  # Flask app instance initiated
api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title="Kalina's Stack",
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


# Custom error handler for handling empty stack errors
@app.errorhandler(InternalError)
def handle_empty_stack(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# GET request on stack resource; returns the elements in the stack
class Stack(MethodResource, Resource):
    @doc(description='Get all elements of the stack',
         tags=['Stack'])
    @marshal_with(StackResponseSchema)  # marshalling the response
    def get(self):
        return {'message': get_stack()}


# POST request on pop resource; pops last element and returns it
class StackPop(MethodResource, Resource):
    @doc(description='Pop an element from the stack',
         tags=['Stack'])
    @marshal_with(StackResponseSchema)
    def post(self):
        if is_empty():
            raise InternalError(message='Empty Stack')
        else:
            value = pop()
            return {'message': f'{value} was popped'}


# POST request on push resource; pushes an integer into the stack
class StackPush(MethodResource, Resource):
    @doc(description='Push an Integer into the stack ',
         tags=['Stack'])
    @use_kwargs(StackPushRequestSchema, location=('json'))
    @marshal_with(StackResponseSchema)
    def post(self, **kwargs):
        value = int(kwargs['value'])
        if is_input_valid(value):
            push(value)
            return {'message': f'{value} was pushed'}
        else:
            return {'message': 'input was not valid'}


# GET request on max resource; returns the current max integer from the stack
class StackMax(MethodResource, Resource):
    @doc(description='Get the largest integer from the stack',
         tags=['Stack'])
    @marshal_with(StackResponseSchema)
    def get(self):
        if is_empty():
            raise InternalError(message='Empty Stack')
        else:
            return {'message': max()}


# Adding all the resources and methods with their path
api.add_resource(StackPush, '/push')
api.add_resource(StackPop, '/pop')
api.add_resource(Stack, '/stack')
api.add_resource(StackMax, '/max')

# Registering the resources into the documentation
docs.register(StackPush)
docs.register(StackPop)
docs.register(Stack)
docs.register(StackMax)

if __name__ == '__main__':
    print("Running")

    # Starting a waintress server - production-quality pure-Python WSGI server with very acceptable performance.
    serve(app, host='127.0.0.1', port=5000, threads=THREAD_COUNT, connection_limit=100000)

    print("done")
