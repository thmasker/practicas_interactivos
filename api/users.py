from flask import Blueprint, jsonify, abort, make_response, request
from re import match

class User:
    def __init__(self, email, password):
        #   Comprobamos que es un email con estructura válida
        if match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            self.email = email
        else:
            raise ValueError
        self.password = password
        self.__id = user_list[-1].id + 1 if user_list else 1
        self.logged = False

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise PermissionError

# Construcción de la "base de datos"
#############################################################################################
user_list = []
user_list.append(User('diego.pedregal@alu.uclm.es', 'ApiRest2019'))
user_list.append(User('api.rest@alu.uclm.es', 'AdminAdmin'))
#############################################################################################

### ERROR messages
REQUEST_JSON_BAD_REQUEST = 'No se han recibido los datos'
PASS_JSON_BAD_REQUEST = 'Password no recibida'
EMAIL_JSON_BAD_REQUEST = 'Email no recibido'
LOGIN_NOT_FOUND = 'Email y/o password incorrectos'
LOGOUT_NOT_FOUND = 'Email no existe'
EMAIL_NOT_VALID = 'El email no es válido'
USER_NOT_FOUND = 'El usuario no existe'

users_api = Blueprint('users_api', __name__)

# Chequeamos las peticiones recibidas
def checkRequest(req):
    if not req:
        abort(400, REQUEST_JSON_BAD_REQUEST)
    elif not 'password' in req:
        abort(400, PASS_JSON_BAD_REQUEST)
    elif not 'email' in req:
        abort(400, EMAIL_JSON_BAD_REQUEST)

# Busca usuarios por id
def findUser(id):
    for user in user_list:
        if user.id == id:
            return user
    abort(404, USER_NOT_FOUND)

# curl -X PUT -H "Content-Type: application/json" -d "{\"email\": \"diego.pedregal@alu.uclm.es\", \"password\": \"ApiRest2019\"}" http://127.0.0.1:2000/users/login/
@users_api.route('/users/login/', methods=['PUT'])
def logIn():
    checkRequest(request.json)

    password = request.json.get('password')
    email = request.json.get('email')

    for user in user_list:
        if user.email == email and user.password == password:
            user.logged = True
            return jsonify({'msg': "Bienvenido al sistema"}), 200
    abort(404, LOGIN_NOT_FOUND)

# curl -X GET http://127.0.0.1:2000/users/logout/
@users_api.route('/users/logout/', methods=['PUT'])
def logOut():
    if not request.json:
        abort(400, REQUEST_JSON_BAD_REQUEST)
    elif not 'email' in request.json:
        abort(400, EMAIL_JSON_BAD_REQUEST)

    email = request.json.get('email')

    for user in user_list:
        if user.email == email:
            user.logged = False
            return jsonify({'msg': "Hasta pronto!"}), 200
    abort(404, LOGOUT_NOT_FOUND)

# curl -X GET http://127.0.0.1:2000/users/
@users_api.route('/users/', methods=['GET'])
def getUsers():
    return jsonify({'users': user_list}), 200

# curl -X POST -H "Content-Type: application/json" -d "{\"email\": \"diego.pedregal@alu.uclm.es\", \"password\": \"ApiRest2019\"}" http://127.0.0.1:2000/users/
@users_api.route('/users/', methods=['POST'])
def createUser():
    checkRequest(request.json)

    password = request.json.get('password')
    email = request.json.get('email')
    
    try:
        user = User(email, password)
    except ValueError:
        abort(400, EMAIL_NOT_VALID)

    user_list.append(user)
    
    return jsonify({'user': user}), 201

# curl -X GET http://127.0.0.1:2000/users/2/
@users_api.route('/users/<int:id>/', methods=['GET'])
def getUser(id):
    user = findUser(id)
    return jsonify({'user': user}), 200

# curl -X PUT -H "Content-Type: application/json" -d "{\"email\": \"diego.pedregal@alu.uclm.es\", \"password\": \"PassCambiada\"}" http://127.0.0.1:2000/users/1/
@users_api.route('/users/<int:id>/', methods=['PUT'])
def updateUser(id):
    user = findUser(id)
    user.password = request.json.get('password', user.password)
    user.email = request.json.get('email', user.email)

    return jsonify({'user': user}), 200

# curl -X DELETE http://127.0.0.1:2000/users/2/
@users_api.route('/users/<int:id>/', methods=['DELETE'])
def deleteUser(id):
    user = findUser(id)
    user_list.remove(user)
    
    return jsonify({}), 200

### ERROR HANDLERS
@users_api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({error.name: error.description}), 400)

@users_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({error.name: error.description}), 404)
