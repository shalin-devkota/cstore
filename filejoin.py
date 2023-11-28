import sqlite3
import os

def join_file_chunks(uuid):
    os.makedirs("outputs",exist_ok=True)
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    
    c.execute("SELECT filename, extension FROM data WHERE uuid = ?", (uuid,))
    result = c.fetchone()
    if result is None:
        print("No file found with the given UUID.")
        return
    filename, extension = result

    
    dir_path = f"chunks/{uuid}"
    output_file_path = f"outputs/{filename}.{extension}"

    
    content = b''
    i = 0
    # Read and concatenate each chunk
    chunk_files = sorted(os.listdir(dir_path))
    for chunk_file in chunk_files:
        print(i)
        with open(os.path.join(dir_path, chunk_file), 'rb') as file:
            content += file.read()
        i +=1

    # Write the concatenated content to a new file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(content)

    # Close the database connection
    # c.close()
    # conn.close()

    # Delete the chunks and the directory
    

    print(f"Chunks have been joined and saved to {output_file_path}.")

# Example usage
join_file_chunks("ac02530e-488a-43d7-ae87-0ec17de1a784")
