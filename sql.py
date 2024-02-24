import os
import mysql.connector
import csv


# Function to connect to MySQL database
def connect_to_mysql(host, user, password, database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# Function to create table in MySQL database
def create_table(cursor, table_name, columns):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")

# Function to insert data into MySQL table
def insert_data(cursor, table_name, data):
    placeholders = ', '.join(['%s' for _ in data[0]])
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.executemany(query, data)

# Main function
def main():
    # MySQL connection parameters
    host = "localhost"
    user = "root"
    password = "xxxxxx"
    database = "music_store"

    # Folder containing CSV files
    csv_folder = r"C:\Users\hp\Desktop\Gen AI1\music store data"

    # Connect to MySQL
    conn = connect_to_mysql(host, user, password, database)
    cursor = conn.cursor()

    # Iterate through CSV files in the folder
    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            table_name = os.path.splitext(filename)[0]
            csv_file = os.path.join(csv_folder, filename)
            
            # Read CSV file
            with open(csv_file, 'r',encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                header = next(csv_reader)
                columns = [f"{col} TEXT" for col in header]
                data = [row for row in csv_reader]

            # Create table in MySQL database
            create_table(cursor, table_name, columns)

            # Insert data into MySQL table
            insert_data(cursor, table_name, data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Data inserted successfully!")

if __name__ == "__main__":
    main()
