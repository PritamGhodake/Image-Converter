from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from PIL import Image
import os
import uuid

app = Flask(__name__)

# Folder to save converted images temporarily
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


# Route to handle image upload and conversion
@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the uploaded image temporarily
        input_filename = f"{uuid.uuid4().hex}.png"  # Default as PNG if no format is specified
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        file.save(input_path)

        # Get output format from user
        output_format = request.form.get('output_format', 'jpg')

        # Generate output file name
        output_filename = f"{uuid.uuid4().hex}.{output_format}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Convert image to desired format
        try:
            with Image.open(input_path) as img:
                img.save(output_path)

            # Return the converted image
            return send_from_directory(UPLOAD_FOLDER, output_filename, as_attachment=True)

        except Exception as e:
            return f"Error: {str(e)}"

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
