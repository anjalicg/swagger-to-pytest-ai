import json

def get_endpoint_schema(file_path: str, endpoint: str, method: str) -> dict:
    """Reads a local Swagger JSON file and extracts a specific endpoint schema."""
    with open(file_path, 'r', encoding='utf-8') as f:
        swagger_data = json.load(f)
    
    # Extract the schema for the given path and method
    return swagger_data["paths"][endpoint][method.lower()]

if __name__ == "__main__":
    # Assuming you run this from your root folder using: python src/parser.py
    local_swagger_file = "swagger.json" 
    
    try:
        # Let's test it by extracting the POST /pet schema
        schema = get_endpoint_schema(local_swagger_file, "/pet", "post")
        print("--- Schema for POST /pet ---")
        print(json.dumps(schema, indent=2))
    except KeyError:
        print("Error: Endpoint or method not found in the Swagger file.")
    except FileNotFoundError:
        print(f"Error: Could not find '{local_swagger_file}'. Make sure you downloaded it!")