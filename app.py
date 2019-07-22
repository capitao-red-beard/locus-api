from flask import Flask, jsonify, make_response, request, abort
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tableservice import TableService

table_service = TableService(account_name='',
                             account_key='')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return '<h1>Hello Azure!</h1>'


@app.route('/locus/container/locations', methods=['GET'])
def get_container_locations():
    # get the desired ship from table service
    e = table_service.query_entities('emerson',
                                     filter="PartitionKey eq 'container'")

    # return a JSON version of the ship locations
    return jsonify(e.items)


@app.route('/locus/container/location/<string:device_id>', methods=['GET'])
def get_container_location(device_id):
    # get the desired ship from table service
    e = table_service.get_entity('emerson', 'container', device_id)

    # return a JSON version of the ship locations
    return jsonify(e)


@app.route('/locus/container/location', methods=['POST'])
def set_container_location():
    # if POST is not JSON or does not contain a trackerId abort
    if not request.json or 'DeviceId' not in request.json:
        abort(400)

    e = Entity()
    e.PartitionKey = 'container'
    e.RowKey = request.json['DeviceId']
    e.device_id = request.json['DeviceId']
    e.latitude = request.json['Properties']['1012']
    e.longitude = request.json['Properties']['1013']
    e.time = request.json['Properties']['5018']

    table_service.insert_or_replace_entity('emerson', e)

    # return success with submitted shipping location
    return jsonify(e), 201


@app.errorhandler(404)
def not_found(error):
    # return not found error
    return make_response(jsonify({'error': 'Not found'}), 404)
