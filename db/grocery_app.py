from flask import Flask, request, jsonify
import sqlite3
import difflib

app = Flask(__name__)

# List of available stores
available_stores = ['aldi', 'kaufland', 'abc', 'pqr', 'std']

def get_store_items(store_name):
    # Connect to SQLite database
    conn = sqlite3.connect('../uploaded_files/prices.db')
    c = conn.cursor()
    # Get items from the specified store
    c.execute(f'SELECT item, price, quantity FROM {store_name}')
    items = c.fetchall()
    conn.close()
    # Format the fetched items
    store_items = [{"item_name": item[0], "price": item[1], "quantity": item[2]} for item in items]
    return store_items

def find_cheapest_products(ingredients, store_names):
    cheapest_products = {}

    # Store all items from each store in a dictionary to reduce database calls
    store_items_dict = {store: get_store_items(store) for store in store_names}

    for ingredient in ingredients:
        current_cheapest = None

        for store, store_items in store_items_dict.items():
            # Find items that match the ingredient with a high similarity score
            matching_items = [item for item in store_items if
                              difflib.SequenceMatcher(None, item['item_name'], ingredient).ratio() > 0.8]

            # Debug print statements to track matching items
            print(f"Matching items for {ingredient} in {store}: {matching_items}")

            # Find the cheapest item among matching items
            if matching_items:
                store_cheapest = min(matching_items, key=lambda x: x['price'])

                # Debug print statements to track cheapest item in current store
                print(f"Cheapest item for {ingredient} in {store}: {store_cheapest}")

                # Compare with the current cheapest found across previous stores
                if current_cheapest is None or store_cheapest['price'] < current_cheapest['price']:
                    current_cheapest = store_cheapest
                    current_cheapest['store'] = store  # Add store information to the cheapest item

        # After comparing across all stores, save the cheapest item for the ingredient
        if current_cheapest:
            cheapest_products[ingredient] = {
                "store": current_cheapest['store'],
                "item_name": current_cheapest['item_name'],
                "price": current_cheapest['price']
            }
        else:
            # If no item was found, set the value to 'NA'
            cheapest_products[ingredient] = {
                "store": "NA",
                "item_name": "NA",
                "price": "NA"
            }

    return cheapest_products

@app.route('/get-items', methods=['POST'])
def get_items():
    data = request.get_json()
    store_names = data.get("store_name", [])
    ingredients = data.get("ingredients", [])

    # Validate the store names against the available stores
    valid_stores = [store for store in store_names if store in available_stores]
    print(valid_stores)
    if not valid_stores:
        return jsonify({"error": "No valid stores provided"}), 400

    cheapest_products = find_cheapest_products(ingredients, valid_stores)

    return jsonify(cheapest_products)

if __name__ == '__main__':
    app.run(debug=True)
