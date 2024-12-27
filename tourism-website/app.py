from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.form['query']  # Get the user input from the form
    formatted_query = user_query  # Directly use user query for search

    places = search_places(formatted_query)  # Call the function to search for places

    # Get the first place if available
    first_place = places[0] if places else None

    return render_template('results.html', places=places, first_place=first_place)  # Render results.html with places and first_place

def search_places(query):
    # Construct the API URL with the user query
    url = f"http://api.geonames.org/searchJSON?q={query}&maxRows=10&username=k1i1n1g"
    response = requests.get(url)  # Make the API call

    print(f"API URL: {url}")  # Print the URL for debugging

    if response.status_code == 200:
        results = response.json()  # Parse the JSON response
        places = []

        for index, place in enumerate(results.get('geonames', []), start=1):
            name = place.get('name', 'N/A')  # Get the place name
            places.append(name)  # Add the place name to the list

        return places  # Return the list of formatted places
    else:
        print("API request failed with status code:", response.status_code)  # Print status code for debugging
        return []  # Return an empty list if the API request fails

if __name__ == '__main__':
    app.run(debug=True)
