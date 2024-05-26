import requests
import csv
import configparser

class GroceryStoreFetcher:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = "AIzaSyAp96Qxg3Rm8Fvik9oLIF4r72u_quW0WIY"
    
    def fetch_all_grocery_stores(self, latitude, longitude, radius=1000.0):
        all_stores = []
        nearbyplace_url = "https://places.googleapis.com/v1/places:searchNearby"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.displayName"
        }

        payload = {
            "includedTypes": ["grocery_store"],
            "maxResultCount": 10,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": radius
                }
            }
        }

        while True:
            response = requests.post(nearbyplace_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for place in data.get('places', []):
                    display_name = place.get('displayName', {}).get('text', 'Unknown')
                    all_stores.append(display_name)
                if 'next_page_token' in data:
                    payload['pagetoken'] = data['next_page_token']
                else:
                    break
            else:
                print(f"Error: {response.status_code}")
                break

        return all_stores

    def get_coordinates(self, address):
        print("USER ADDRESS IN CORD", address)
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': address,
            'key': self.api_key
        }

        response = requests.get(geocode_url, params=params)
        if response.status_code == 200:
            results = response.json().get('results')
            if results:
                location = results[0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print("No results found for the address.")
                return None
        else:
            print(f"Geocoding API Error: {response.status_code}")
            return None
    
    def write_stores_to_csv(self, stores, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Store_Name"])
            for store in stores:
                writer.writerow([store])

    def fetch_near_grocery_stores_by_address(self, address, radius=1000.0):
        coordinates = self.get_coordinates(address)
        if coordinates:
            latitude, longitude = coordinates
            return self.fetch_all_grocery_stores(latitude, longitude, radius)
        else:
            print("Could not find coordinates for the address.")
            return []


if __name__ == "__main__":
    config_file = 'config.ini'
    address = "Danziger straße, 6 Uttenreuth  91080 , Germany"
    output_file = 'grocery_stores.csv'
    
    fetcher = GroceryStoreFetcher(config_file)
    coordinates = fetcher.get_coordinates(address)
    if coordinates:
        latitude, longitude = coordinates
        all_grocery_stores = fetcher.fetch_all_grocery_stores(latitude, longitude)
        for store in all_grocery_stores:
            print(store)
        fetcher.write_stores_to_csv(all_grocery_stores, output_file)
