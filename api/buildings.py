from flask import Blueprint, jsonify, abort, make_response, request

class Building:
    def __init__(self, name, consumptions):
        self.__id = building_list[-1].id + 1 if building_list else 1
        self.name = name
        self.consumptions = consumptions

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        raise PermissionError

# Construcción de la "base de datos"
#######################################################################################################
building_list = []
building_list.append(Building('ESI', []))
building_list.append(Building('Industriales', []))
#######################################################################################################

buildings_api = Blueprint('buildings_api', __name__)

### ERROR mensajes
REQUEST_JSON_BAD_REQUEST = 'No se han recibido los datos'
NAME_JSON_BAD_REQUEST = 'Nombre del edificio no recibido'
BUILDING_NOT_FOUND = 'El edificio no existe'

# Busca edificios por id
def findBuilding(id):
    for bld in building_list:
        if bld.id == id:
            return bld
    abort(404, BUILDING_NOT_FOUND)

# curl -X GET http://127.0.0.1:2000/buildings/
@buildings_api.route('/buildings/', methods=['GET'])
def getBuildings():
    return jsonify({'buildings': building_list}), 200

# curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Fermin Caballero\"}" http://127.0.0.1:2000/buildings/
@buildings_api.route('/buildings/', methods=['POST'])
def createBuilding():
    if not request.json:
        abort(400, REQUEST_JSON_BAD_REQUEST)
    elif not 'name' in request.json:
        abort(400, NAME_JSON_BAD_REQUEST)

    name = request.json.get('name')

    building = Building(name, [])
    building_list.append(building)

    return jsonify({'building': building}), 201

# curl -X GET http://127.0.0.1:2000/buildings/2/
@buildings_api.route('/buildings/<int:id>/', methods=['GET'])
def getBuilding(id):
    building = findBuilding(id)
    return jsonify({'building': building}), 200

# curl -X PUT -H "Content-Type: application/json" -d "{\"name\": \"Fermin Caballero\"}" http://127.0.0.1:2000/buildings/1/
@buildings_api.route('/buildings/<int:id>/', methods=['PUT'])
def updateBuilding(id):
    building = findBuilding(id)
    building.name = request.json.get('name', building.name)

    return jsonify({'building': building}), 200

# curl -X DELETE http://127.0.0.1:2000/buildings/2/
@buildings_api.route('/buildings/<int:id>/', methods=['DELETE'])
def deleteBuilding(id):
    building = findBuilding(id)
    
    building_list.remove(building)
    return jsonify({}), 200

### ERROR HANDLERS
@buildings_api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({error.name: error.description}), 400)

@buildings_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({error.name: error.description}))
