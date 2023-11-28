import sqlite3
import uuid
import os


conn = sqlite3.connect("data.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS data(uuid TEXT PRIMARY KEY,filename TEXT , extension TEXT)")
conn.commit()


def file_to_binary_chunks(file_path, chunk_size_mb=5):
    
    chunk_size = chunk_size_mb * 1024 * 1024
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    print(file_name)
    file_uuid = uuid.uuid4()
    os.makedirs("chunks",exist_ok=True)
    os.makedirs(f"chunks/{file_uuid}",exist_ok=True)


    # Open the file
    with open(file_path, 'rb') as file:
        file_no = 0
        while True:
            # Read a chunk of the file
            chunk = file.read(chunk_size)
            if not chunk:
                break  # Exit loop if we are at the end of the file

            # Write the chunk to a new file
            with open(f'chunks/{file_uuid}/{file_name}_chunk{file_no}.bin', 'wb') as chunk_file:
                chunk_file.write(chunk)

            file_no += 1

    c.execute("INSERT INTO data (uuid, filename, extension) VALUES (?, ?, ?)", (str(file_uuid), file_name, file_extension))
    conn.commit()
    c.close()
    print(f"File '{file_path}' has been split into {file_no} chunks.")

# Example usage
file_path = '/mnt/e/test.jpg'  # Replace with your file path
file_to_binary_chunks(file_path)
