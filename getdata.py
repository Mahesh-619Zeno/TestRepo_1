# Scenario 2: Misleading function name 'getData' that performs a delete operation

def getData(record_id):
    """
    Expected to retrieve data, but actually deletes it – misleading
    """
    print(f"Deleting record with ID: {record_id}")
    delete_from_db(record_id)

def delete_from_db(id):
    print(f"[DB] Record {id} deleted.")

getData(101)  # This deletes data, not "gets" it
