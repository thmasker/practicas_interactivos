from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
from random import uniform

from .buildings import building_list, findBuilding, REQUEST_JSON_BAD_REQUEST

FORMATO_DATE = '%Y-%m-%d'

class Consumption:
    def __init__(self, date, value):
        self.date = datetime.strptime(date, FORMATO_DATE)
        self.__value = round(value, 2)
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = round(v, 2)

# Construcción de la "base de datos"
#########################################################################################
for bld in building_list:
    for m in range(1, 13):
        for d in range(1, 32):
            try:
                bld.consumptions.append(Consumption('2019-' + str(m) + '-' + str(d), round(uniform(120, 3000), 2)))
            except ValueError:
                continue
#########################################################################################

### ERROR messages
CONSUMPTION_NOT_FOUND = 'El consumo solicitado no existe'
INICIAL_DATE_BAD_REQUEST = 'La fecha inicial no es correcta'
FINAL_DATE_BAD_REQUEST = 'La fecha final no es correcta'
DATE_BAD_REQUEST = 'Fecha no recibida'
DATE_BAD_FORMAT = 'La fecha tiene un formato incorrecto'
CONSUMPTION_BAD_REQUEST = 'Consumo energético no recibido'
VALUE_BAD_FORMAT = 'El formato del consumo energético no es correcto'
CONSUMPTION_ALREADY_EXISTING = 'La fecha ya tiene consumo asignado. Solamente puede editarlo'

consumptions_api = Blueprint('consumptions_api', __name__)

# Busca un consumo en un edificio dado
def findConsumption(building, date):
    for c in building.consumptions:
        if c.date == datetime.strptime(date, FORMATO_DATE):
            return c
    return None

# curl -X GET http://127.0.0.1:2000/consumptions/2/2019-12-1/2019-12-31/
@consumptions_api.route('/consumptions/<int:b_id>/<string:inicio>/<string:final>/', methods=['GET'])
def getConsumptions(b_id, inicio, final):
    try:
        d_inicio = datetime.strptime(inicio, FORMATO_DATE)
    except ValueError:
        abort(400, INICIAL_DATE_BAD_REQUEST)
    try:
        d_final = datetime.strptime(final, FORMATO_DATE)
    except:
        abort(400, FINAL_DATE_BAD_REQUEST)

    building = findBuilding(b_id)
    return jsonify({'consumptions': getConsumptions(bld, (d_inicio, d_final))}), 200

def getConsumptions(building, dates):
    consumptions = []
    for c in building.consumptions:
        if c.date >= dates[0] and c.date <= dates[1]:
            consumptions.append(c)
    return consumptions

# curl -X POST -H "Content-Type: application/json" -d "{\"date\": \"2020-2-9\", \"value\": 127.33}" http://127.0.0.1:2000/consumptions/2/
@consumptions_api.route('/consumptions/<int:b_id>/', methods=['POST'])
def createConsumption(b_id):
    if not request.json:
        abort(400, REQUEST_JSON_BAD_REQUEST)
    elif not 'date' in request.json:
        abort(400, DATE_BAD_REQUEST)
    elif not 'value' in request.json:
        abort(400, CONSUMPTION_BAD_REQUEST)

    building = findBuilding(b_id)

    date = request.json.get('date')
    value = request.json.get('value')
    try:
        consumption = Consumption(date, value)
    except TypeError:
        abort(400, VALUE_BAD_FORMAT)
    except ValueError:
        abort(400, DATE_BAD_FORMAT)
    
    if findConsumption(building, date):
            abort(400, CONSUMPTION_ALREADY_EXISTING)

    building.consumptions.append(consumption)
    return jsonify({'consumption': consumption}), 201

# curl -X PUT -H "Content-Type: application/json" -d "{\"value\": 123.1231241}" http://127.0.0.1:2000/consumptions/1/2019-12-2/
@consumptions_api.route('/consumptions/<int:b_id>/<string:date>/', methods=['PUT'])
def updateConsumption(b_id, date):
    if not request.json:
        abort(400, REQUEST_JSON_BAD_REQUEST)
    elif not 'value' in request.json:
        abort(400, DATE_BAD_REQUEST)
    

    building = findBuilding(b_id)
    consumption = findConsumption(building, date)

    if not consumption:
        abort(404, CONSUMPTION_NOT_FOUND)
    
    try:
        consumption.value = request.json.get('value', consumption.value)
    except TypeError:
        abort(400, VALUE_BAD_FORMAT)

    return jsonify({'consumption': consumption}), 200

# curl -X DELETE http://127.0.0.1:2000/consumptions/2/2019-4-5/
@consumptions_api.route('/consumptions/<int:b_id>/<string:date>/', methods=['DELETE'])
def deleteConsumption(b_id, date):
    building = findBuilding(b_id)
    consumption = findConsumption(building, date)

    if not consumption:
        abort(404, CONSUMPTION_NOT_FOUND)

    building.consumptions.remove(consumption)
    return jsonify({}), 200

### ERROR HANDLERS
@consumptions_api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({error.name: error.description}), 400)

@consumptions_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({error.name: error.description}), 404)
