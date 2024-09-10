from flask import Flask, request, jsonify
import outlier_las  # Import outlier detection module

app = Flask(__name__)

@app.route('/api/process_files', methods=['POST'])
def process_files():
    directory_path = request.json.get('directory_path')

    try:
        # Use the outlier detection module
        outlier_las.process_files_in_directory(directory_path)
        return jsonify({'message': 'Process completed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)  # Run the server and accept all requests