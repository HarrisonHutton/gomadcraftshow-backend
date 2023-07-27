import pandas as pd
import sys
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Replace with the path to your service account key JSON file
cred = credentials.Certificate("environments/gomad-craft-show-firebase-adminsdk-uzbiz-133156689e.json")

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 importspaces.py <excel_file>")
        sys.exit(1)

    spaces_excel_file = sys.argv[1]
    
    try:
        # Step 1: Convert Excel to CSV
        csv_file = excel_to_csv(spaces_excel_file)

        # Step 2: Process the data
        processed_data = process_data(csv_file)

        # Step 3: Write data to Firestore
        write_to_firestore(processed_data)

        # Cleanup: Delete the temporary CSV file
        os.remove(csv_file)

    except Exception as e:
        print("An error occurred:", str(e))


def excel_to_csv(excel_file):
    # Convert Excel file to a temporary CSV file
    df = pd.read_excel(excel_file)
    temp_csv_file = "temp.csv"
    df.to_csv(temp_csv_file, index=False)
    return temp_csv_file


# From the admin app, @models folder:
# export interface VendorSpace {
#     name: string;
#     fee: number;
#     location: Location;
#     /* `vendor` is a reference to the vendor who owns this space and may be null in the
#      * case that no vendor has applied for the space yet. */
#     vendor?: Vendor;    
# }

def process_data(csv_file) -> list[dict]:
    # Process the data from the CSV file (e.g., apply transformations, calculations)
    df = pd.read_csv(csv_file)
    # Do your data processing here
    
    vendorSpaces = []
    
    for _, row in df.iterrows():
        space = {
            "name": row["Space Name"],
            "fee": row["Fee"],
            "location": row["Location"],
        }
        vendorSpaces.append(space)
    
    return vendorSpaces


def write_to_firestore(data: list[dict]):
    # Get a reference to the Firestore collection
    db = firestore.client()
    collection_ref = db.collection("vendorSpaces")

    # Write data to Firestore
    for vendorSpace in data:
        collection_ref.add(vendorSpace)

    print("Data has been written to Firestore.")
    

if __name__ == "__main__":
    main()