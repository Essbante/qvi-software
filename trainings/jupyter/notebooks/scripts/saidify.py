import json
import os
from keri.core import coring, scheming

# Define default values and keys used in the functions for clarity and easy modification.
DEFAULT_SAID_KEY = coring.Saids.dollar  # Default dictionary key to store the SAID
DEFAULT_HASH_CODE = coring.MtrDex.Blake3_256 # Default hashing algorithm for SAID generation
JSON_SCHEMA_ID_KEY = '$id' # Standard key often used to mark a sub-schema for identification
PROPERTY_KEYS_TO_PROCESS = ["a", "e", "r"] # Specific property keys to check within the schema

def add_saids_to_data(data_dict: dict, said_key: str = DEFAULT_SAID_KEY, hash_code: str = DEFAULT_HASH_CODE) -> dict:
    """
    Adds Self-Addressing Identifiers (SAIDs) to specific parts of a dictionary,
    typically representing a schema or structured data.

    It processes predefined top-level properties ('a', 'e', 'r') and their 'oneOf' lists,
    adding SAIDs based on the content. It also adds a SAID for the entire input dictionary.

    Args:
        data_dict: The dictionary (e.g., loaded JSON schema) to process.
        said_key: The dictionary key where the generated SAID should be stored.
        hash_code: The KERI MtrDex code specifying the hashing algorithm (e.g., Blake3_256).

    Returns:
        The modified dictionary with SAIDs added.
    """
    if 'properties' in data_dict:
        properties = data_dict['properties']
        for prop_key in PROPERTY_KEYS_TO_PROCESS:
            if prop_key in properties:
                prop_value = properties[prop_key]
                # Check if the direct property value is a dict marked with JSON_SCHEMA_ID_KEY
                if isinstance(prop_value, dict) and JSON_SCHEMA_ID_KEY in prop_value:
                    # Calculate and add SAID to this sub-dictionary
                    prop_value[said_key] = coring.Saider(sad=prop_value, code=hash_code, label=said_key).qb64
                # Check if the property value contains a 'oneOf' list
                elif isinstance(prop_value, dict) and 'oneOf' in prop_value and isinstance(prop_value['oneOf'], list):
                    # Process each item in the 'oneOf' list
                    for item in prop_value['oneOf']:
                        if isinstance(item, dict) and said_key in item:
                            # Calculate and add SAID to this item within 'oneOf'
                            item[said_key] = coring.Saider(sad=item, code=hash_code, label=said_key).qb64

    # Calculate and add SAID for the entire input dictionary
    data_dict[said_key] = coring.Saider(sad=data_dict, code=hash_code, label=said_key).qb64

    return data_dict

# --- File Handling ---

def _write_json_file(data: dict, filepath: str):
    """Helper function to write dictionary data to a JSON file with indentation."""
    try:
        # Ensure the directory exists before writing
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error writing JSON to {filepath}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing {filepath}: {e}")

# --- Example Usage ---
#     process_schema_file('test_schema.json', 'schemas')
def process_schema_file(input_filepath: str, output_schema_dir: str):
    """
    Reads a JSON file, adds SAIDs using add_saids_to_data, wraps it in a KERI Schemer,
    and writes the processed data back to the original file location and to a
    specified output directory.

    Args:
        input_filepath: Path to the input JSON file.
        output_schema_dir: Path to the directory where the processed schema
                           should also be saved.
    """
    try:
        # Read the input JSON file
        with open(input_filepath, 'r') as infile:
            original_data = json.load(infile)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_filepath}: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading {input_filepath}: {e}")
        return

    # Add SAIDs to the data
    # Uses default said_key and hash_code unless specified otherwise
    data_with_saids = add_saids_to_data(original_data.copy()) # Process a copy if needed

    # Create a Schemer object using the SAID-ified data
    # The Schemer might perform validation or further processing based on the SAIDs.
    schemer = scheming.Schemer(sed=data_with_saids)
    processed_data = schemer.sed # Use the data managed by the Schemer

    # Write the processed data back to the original file path
    _write_json_file(processed_data, input_filepath)

    # Construct the output path in the specified schema directory
    base_filename = os.path.basename(input_filepath)
    output_filepath_in_dir = os.path.join(output_schema_dir, base_filename)

    # Write the processed data to the schema directory
    _write_json_file(processed_data, output_filepath_in_dir)

    print(f"Processed '{input_filepath}' and saved results to itself and '{output_filepath_in_dir}'")

