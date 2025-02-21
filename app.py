from flask import Flask, request, send_file
import io

app = Flask(__name__)

# Dictionary to store files in memory (simulating a buffer)
file_storage = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400

    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400

    # Store the file in memory (buffer)
    file_buffer = io.BytesIO(file.read())
    original_filename = file.filename
    extension = original_filename.split('.')[-1]
    file.filename = f"uploaded_file.{extension}"
    file_storage[file.filename] = file_buffer

    return {"message": "File uploaded successfully", "filename": file.filename}, 200

@app.route('/get-file/<filename>', methods=['GET'])
def get_file(filename):
    if filename not in file_storage:
        return {"error": "File not found"}, 404

    # Retrieve file from memory and send it as a response
    file_buffer = file_storage[filename]
    file_buffer.seek(0)  # Move to the beginning of the buffer
    return send_file(file_buffer, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
