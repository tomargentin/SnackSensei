import sqlite3
import random
import os
from groq import Groq

client = Groq(api_key="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")

categories = {
    "Vegetables": [],
    "Fruits": [],
    "Dairy Products": [],
    "Meat": [],
    "Bakery": [],
    "Beverages": [],
    "Snacks": [],
    "Frozen Foods": [],
}

def fetch_items_from_groq(category, batch_size=50, total_items=500):
    items = []
    while len(items) < total_items:
        system_message = {
            "role": "system",
            "content": (
                "You are a helpful assistant. Your task is to generate a list of grocery items, including item name, price, and quantity. "
                "Please provide 50 unique items in the specified category with their prices and quantities. "
                "Each item should be unique and the data should be structured in JSON format strictly adhering to this schema and nothing else:\n"
                "{\n"
                "    \"items\": [\n"
                "        {\n"
                "            \"item_name\": \"string\",\n"
                "            \"price\": \"float\",\n"
                "            \"quantity\": \"int\"\n"
                "        },\n"
                "        ...\n"
                "    ]\n"
                "}\n"
                "Only provide the JSON output with no extra information."
            )
        }

        user_message = {
            "role": "user",
            "content": f"Generate a list of {batch_size} unique items in the {category} category with their prices and quantities."
        }

        try:
            chat_completion = client.chat.completions.create(
                messages=[system_message, user_message],
                model="llama3-8b-8192",
                response_format={"type": "json_object"},
                temperature=1,
            )

            response = chat_completion.choices[0].message.content
            response_data = eval(response)  # Parse the string response to dictionary
            batch_items = response_data['items']
            items.extend(batch_items)
            print(f"Successfully fetched items for category {category}.")
        except (SyntaxError, KeyError) as e:
            print(f"Error parsing response for category {category}: {response} - {e}")
        except Exception as e:
            print(f"An error occurred for category {category}: {e}")

    return items

def fetch_and_store_items_for_store(store_name):
    store_categories = {}
    for category in categories.keys():
        items = fetch_items_from_groq(category)
        store_categories[category] = items
    return store_categories

def insert_items(store_name, store_categories):
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()

    for category, items in store_categories.items():
        for item in items:
            item_name = item['item_name']
            price = float(item['price'])
            quantity = int(item['quantity'])
            if item_name and price and quantity:
                c.execute(f'''
                    INSERT INTO {store_name} (item, price, quantity)
                    VALUES (?, ?, ?)
                ''', (item_name, price, quantity))

    conn.commit()
    conn.close()

def populate_all_stores():
    stores = ['aldi', 'kaufland', 'abc', 'pqr']
    for store in stores:
        store_categories = fetch_and_store_items_for_store(store)
        insert_items(store, store_categories)
        print(f"Successfully inserted items for store {store}.")

if __name__ == '__main__':
    # create_database()
    populate_all_stores()