from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Expanded sample data
cakes = [
    {"id": 1, "name": "Chocolate Cake", "category": "Chocolate", "price": 50, "available": True, "rating": 4.8, "stock": 10},
    {"id": 2, "name": "Vanilla Cake", "category": "Classic", "price": 45, "available": True, "rating": 4.5, "stock": 5},
    {"id": 3, "name": "Red Velvet Cake", "category": "Velvet", "price": 60, "available": False, "rating": 4.9, "stock": 0},
    {"id": 4, "name": "Cheesecake", "category": "Cheese", "price": 70, "available": True, "rating": 4.7, "stock": 8},
    {"id": 5, "name": "Lemon Drizzle Cake", "category": "Citrus", "price": 55, "available": True, "rating": 4.6, "stock": 4},
    {"id": 6, "name": "Carrot Cake", "category": "Vegetable", "price": 50, "available": True, "rating": 4.3, "stock": 12},
    {"id": 7, "name": "Strawberry Shortcake", "category": "Fruit", "price": 65, "available": True, "rating": 4.8, "stock": 6},
    {"id": 8, "name": "Black Forest Cake", "category": "Chocolate", "price": 80, "available": True, "rating": 4.9, "stock": 3},
    {"id": 9, "name": "Tiramisu", "category": "Coffee", "price": 75, "available": True, "rating": 4.8, "stock": 5},
    {"id": 10, "name": "Pineapple Upside-Down Cake", "category": "Fruit", "price": 40, "available": False, "rating": 4.4, "stock": 0},
]

# Additional details for each cake
cake_details = {
    1: {"description": "A rich and creamy chocolate cake", "ingredients": ["chocolate", "flour", "sugar", "butter", "eggs"], "calories": 450, "size": "Medium"},
    2: {"description": "Classic vanilla cake with smooth frosting", "ingredients": ["vanilla", "flour", "sugar", "butter", "eggs"], "calories": 400, "size": "Small"},
    3: {"description": "Smooth red velvet with a hint of cocoa", "ingredients": ["cocoa", "buttermilk", "flour", "sugar", "eggs"], "calories": 420, "size": "Large"},
    4: {"description": "Creamy New York-style cheesecake", "ingredients": ["cream cheese", "sugar", "eggs", "vanilla extract"], "calories": 500, "size": "Medium"},
    5: {"description": "Moist lemon drizzle cake with a tangy glaze", "ingredients": ["lemon zest", "flour", "sugar", "butter", "eggs"], "calories": 380, "size": "Small"},
    6: {"description": "Moist carrot cake with walnuts", "ingredients": ["carrots", "walnuts", "flour", "sugar", "cinnamon"], "calories": 410, "size": "Medium"},
    7: {"description": "Fluffy shortcake with fresh strawberries", "ingredients": ["strawberries", "flour", "sugar", "butter", "cream"], "calories": 430, "size": "Small"},
    8: {"description": "Classic Black Forest cake with cherries", "ingredients": ["chocolate", "cherries", "flour", "sugar", "cream"], "calories": 460, "size": "Large"},
    9: {"description": "Coffee-flavored Italian dessert", "ingredients": ["espresso", "mascarpone", "sugar", "cocoa", "ladyfingers"], "calories": 390, "size": "Medium"},
    10: {"description": "Pineapple upside-down cake with caramelized edges", "ingredients": ["pineapple", "brown sugar", "flour", "butter", "cherries"], "calories": 370, "size": "Small"},
}

# Helper function to get a new ID
def get_new_id():
    if cakes:
        return max(cake["id"] for cake in cakes) + 1
    return 1

# Cake list endpoint with Create option
class CakeList(Resource):
    def get(self):
        return {"error": False, "message": "success", "count": len(cakes), "cakes": cakes}
    
    def post(self):
        data = request.json
        new_id = get_new_id()
        
        new_cake = {
            "id": new_id,
            "name": data.get("name"),
            "category": data.get("category"),
            "price": data.get("price"),
            "available": data.get("available", True),
            "rating": data.get("rating", 0),
            "stock": data.get("stock", 0)
        }
        cakes.append(new_cake)
        
        # Add details
        cake_details[new_id] = {
            "description": data.get("description", ""),
            "ingredients": data.get("ingredients", []),
            "calories": data.get("calories", 0),
            "size": data.get("size", "Medium")
        }
        
        return {"error": False, "message": "Cake created successfully", "cake": new_cake}, 201

# Cake detail endpoint with Read, Update, and Delete options
class CakeDetail(Resource):
    def get(self, cake_id):
        cake = next((cake for cake in cakes if cake["id"] == cake_id), None)
        if not cake:
            return {"error": True, "message": "Cake not found"}, 404
        
        return {"error": False, "message": "success", "cake": cake, "details": cake_details.get(cake_id)}
    
    def put(self, cake_id):
        data = request.json
        cake = next((cake for cake in cakes if cake["id"] == cake_id), None)
        if not cake:
            return {"error": True, "message": "Cake not found"}, 404
        
        # Update main cake data
        cake.update({
            "name": data.get("name", cake["name"]),
            "category": data.get("category", cake["category"]),
            "price": data.get("price", cake["price"]),
            "available": data.get("available", cake["available"]),
            "rating": data.get("rating", cake["rating"]),
            "stock": data.get("stock", cake["stock"]),
        })
        
        # Update cake details
        cake_details[cake_id].update({
            "description": data.get("description", cake_details[cake_id]["description"]),
            "ingredients": data.get("ingredients", cake_details[cake_id]["ingredients"]),
            "calories": data.get("calories", cake_details[cake_id]["calories"]),
            "size": data.get("size", cake_details[cake_id]["size"])
        })
        
        return {"error": False, "message": "Cake updated successfully", "cake": cake}
    
    def delete(self, cake_id):
        global cakes, cake_details
        cakes = [cake for cake in cakes if cake["id"] != cake_id]
        if cake_id in cake_details:
            del cake_details[cake_id]
        
        return {"error": False, "message": "Cake deleted successfully"}

# Registering resources with endpoints
api.add_resource(CakeList, "/cakes")
api.add_resource(CakeDetail, "/cakes/<int:cake_id>")

if __name__ == "__main__":
    app.run(debug=True)
