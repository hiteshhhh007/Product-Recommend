import os
import sqlite3
import json
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Allow cross-origin requests from your frontend (running on port 3000)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

DATABASE = 'database.db'

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Configure the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set in backend/.env")
genai.configure(api_key=GEMINI_API_KEY)

# Helper function to shuffle a list
def shuffle_list(data_list):
    return random.sample(data_list, len(data_list))

@app.route('/api/products', methods=['GET'])
def get_products():
    """API endpoint to fetch all products from the database."""
    conn = get_db_connection()
    products_cursor = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    # Convert cursor objects to a list of dictionaries
    products = [dict(row) for row in products_cursor]
    return jsonify(products)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get AI-powered product recommendations."""
    data = request.get_json()
    if not data or 'userHistory' not in data or 'cart' not in data:
        return jsonify({"error": "Missing userHistory or cart in request body"}), 400

    user_history = data['userHistory']
    cart = data['cart']

    # --- Fetch all available products from the database ---
    conn = get_db_connection()
    all_products_rows = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    all_products = [dict(row) for row in all_products_rows]

    # --- Generate prompt for Gemini ---
    history_text = (
        f"The user has previously viewed these products: {', '.join([f'\"{p["name"]}\" ({p["description"]})' for p in user_history])}."
        if user_history else "The user has not viewed any products yet."
    )

    cart_text = (
        f"The user currently has these items in their shopping cart: {', '.join([f'\"{p["name"]}\" ({p["description"]})' for p in cart])}."
        if cart else "The user's shopping cart is empty."
    )

    # --- Scalability Enhancement: Create a smaller, curated catalog for the prompt ---
    user_product_ids = {p['id'] for p in user_history} | {p['id'] for p in cart}
    all_available_products = [p for p in all_products if p['id'] not in user_product_ids]
    
    interest_categories = {p['category'] for p in user_history} | {p['category'] for p in cart}
    relevant_products = [p for p in all_available_products if p['category'] in interest_categories]
    
    other_products = [p for p in all_available_products if p['category'] not in interest_categories]
    random_sample = shuffle_list(other_products)[:30]

    curated_catalog_map = {p['id']: p for p in relevant_products + random_sample}
    curated_catalog = list(curated_catalog_map.values())
    
    catalog_text = "\n".join(
        [f"ID: {p['id']}, Name: {p['name']}, Category: {p['category']}, Description: {p['description']}" for p in curated_catalog]
    )

    prompt = f"""
    You are an expert e-commerce product recommendation engine.

    **Curated Product Catalog (a subset of all available products):**
    {catalog_text}

    **User Behavior:**
    {history_text}
    {cart_text}

    Based on the user's behavior, recommend products from the provided curated catalog. For each recommendation, provide a very short, friendly, and compelling explanation (2 sentences max) for why it was recommended for the user, connecting to their past interests.

    Return your answer as a JSON object with a single key "recommendations" which is an array of objects, where each object has "productId" (a number) and "explanation" (a string). Do not recommend products the user has already viewed or has in their cart.
    """

    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content(prompt)
        
        json_response = json.loads(response.text)

        if "recommendations" not in json_response or not isinstance(json_response["recommendations"], list):
            print("Invalid JSON response structure:", json_response)
            return jsonify([])

        recommendations = []
        for rec in json_response["recommendations"]:
            product_id = rec.get("productId")
            explanation = rec.get("explanation")
            
            product = next((p for p in all_products if p['id'] == product_id), None)
            
            if product and explanation:
                recommendations.append({"product": product, "explanation": explanation})
        
        return jsonify(recommendations)

    except Exception as e:
        print(f"Error getting AI recommendations: {e}")
        return jsonify({"error": "Failed to fetch AI recommendations"}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible on your network
    app.run(host='0.0.0.0', port=5000, debug=True)