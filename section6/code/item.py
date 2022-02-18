import sqlite3
from unicodedata import name
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank")
    
    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name']==name, items),None)
        # return {'item':item}, 200 if item  else 404
        item=self.find_by_name(name)
        if item:
            return item        
        return {'message': 'Item not found'},404
    
    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query ="SELECT * FROM items WHERE pname=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone() 
        connection.close()
        if row:
            return {'item':{'name':row[0],'price':row[1]}}
        
    
    def post(self, name):
        # if next(filter(lambda x: x['name']==name,items),None):
        #     return {'message': "An item with name '{}' already exists".format(name)},404 
        
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)},404             
               
        data = Item.parser.parse_args()              
        item={'name':name, 'price':data['price']}
        #items.append(item)
        try:
            Item.insert(item)
        except:
            return {"message":"An error occured inserting the item."},500
        return item, 201
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query="INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'],item['price']))
        connection.commit()
        connection.close()
    
    def delete(self,name):
        # global items
        # if next(filter(lambda x: x['name']==name,items),None):
        #     items = list(filter(lambda x: x['name'] != name, items))
        #     return {'message':'Item deleted'}
        # return {'message':'Item not present'}, 404
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query="DELETE FROM items WHERE pname=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return {'message':'Item deleted'}
    
    def put(self,name):
        data = Item.parser.parse_args()        
        item = Item.find_by_name(name)
        updated_item={'name':name, 'price':data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message':'An Error Occurred while inserting the data.'}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {'message':'An Error Occurred while updating the data.'},500
        return updated_item
     
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query="UPDATE items SET price=? WHERE pname=?"
        cursor.execute(query,(item['price'],item['name']))
        connection.commit()
        connection.close()
    
class ItemList(Resource):
    def get(self):
        return ItemList.get_all()
    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query ="SELECT * FROM items"
        result = cursor.execute(query)
        items =[]
        for row in result:
            items.append({'name':row[0],'price':row[1]}) 
        connection.close()
        return {'items':items}

        
    
    