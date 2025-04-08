import csv
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load data into memory
LoadedData = []
try:
    with open("LE.csv", "r", encoding="latin1") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            LoadedData.append(row)
except FileNotFoundError:
    print("The file LE.csv was not found.")
    LoadedData = []

# search route with pagination
@app.route('/getdata', methods=['GET'])
def search_and_paginate():
    """Searches for rows that match query parameters and returns paginated results."""
    name = request.args.get('name')
    sn = request.args.get('sn')
    page = int(request.args.get('page', 1))  # Default to page 1
    per_page = int(request.args.get('per_page', 10))  # Default to 10 items per page

    # Filter the data based on the query parameters
    filtered_data = filter_data(LoadedData, name, sn)

    # Paginate the results
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = filtered_data[start:end]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(filtered_data),
        "results": paginated_data
    })

# Function to filter data
def filter_data(data, name=None, sn=None):
    filtered = []
    for item in data:
        # Case-insensitive partial match for the 'name' query
        if name and name.lower() not in item[1].lower():  # Assuming name is in the second column
            continue
        # Filter by serial number if 'sn' is provided
        if sn and sn not in item:
            continue
        filtered.append(item)
    return filtered

# pagination route
@app.route('/pagination', methods=['GET'])
def get_paginated_data():
    # Get the page and per_page parameters for pagination
    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 10))  # Default per_page is 10

    # If there's data in the LoadedData, apply pagination
    if LoadedData:
        # Calculate the start and end indices for pagination
        start = (page - 1) * per_page
        end = start + per_page

        # Slice the LoadedData to return only the relevant items for the requested page
        paginated_data = LoadedData[start:end]

        # Pagination metadata
        total_items = len(LoadedData)
        total_pages = (total_items // per_page) + (1 if total_items % per_page > 0 else 0)

        # Return the paginated results as JSON with pagination metadata
        return jsonify({
            'page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': total_pages,
            'data': paginated_data
        })
    else:
        return jsonify({"error": "No data found or file could not be loaded."}), 500

if __name__ == '__main__':
    app.run(debug=True)
