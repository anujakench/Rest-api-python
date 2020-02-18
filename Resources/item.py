
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This argument is required')
    parser.add_argument('store_id', type=float, required=True, help='This argument is required')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'Item with name {} already exists.'.format(name)}
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item_price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}