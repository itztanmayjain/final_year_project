import base64
from io import BytesIO
import cv2
import os
import glob
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template,jsonify

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])

if 'static' not in os.listdir('.'):
    os.mkdir('static')

if 'uploads' not in os.listdir('static/'):
    os.mkdir('static/uploads')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def remove_background(input_path,output_path):
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/remback',methods=['POST'])
def remback():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        rembg_img_name = filename.split('.')[0]+"_nobg.png"
        remove_background(UPLOAD_FOLDER+'/'+filename,UPLOAD_FOLDER+'/'+rembg_img_name)
        return render_template('result.html',org_img_name=filename,rembg_img_name=rembg_img_name)

@app.route('/Multi_remback', methods=['POST'])
def Multi_remback():
    if 'file' not in request.files:
        return "No file part", 400
    
    files = request.files.getlist('file')  # Get list of uploaded files
    
    if not files:
        return "No files uploaded", 400

    processed_images = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            rembg_img_name = filename.split('.')[0] + "_nobg.png"
            
            # Call your background removal function here
            remove_background(os.path.join(app.config['UPLOAD_FOLDER'], filename), 
                              os.path.join(app.config['UPLOAD_FOLDER'], rembg_img_name))
            
            # Add original and processed image names to the list
            processed_images.append({
                'org_img_name': filename,
                'rembg_img_name': rembg_img_name
            })
    
    # Pass the processed images list to your template for rendering
    return render_template('result.html', processed_images=processed_images)


@app.route('/API_Multi_remback', methods=['POST'])
def API_Multi_remback():
    data = request.get_json()  # Expecting a JSON payload
    
    if not data or 'files' not in data:
        return jsonify({"error": "No files part in the request"}), 400

    files = data['files']  # Get list of base64 encoded images
    
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    processed_images = []

    for idx, file_data in enumerate(files):
        try:
            # Decode the Base64 image
            image_data = base64.b64decode(file_data)
            image = Image.open(BytesIO(image_data))
            filename = f"image_{idx}.png"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(file_path)  # Save original image to process it
            
            # Define name for the processed (background-removed) image
            rembg_img_name = f"image_{idx}_nobg.png"
            rembg_img_path = os.path.join(app.config['UPLOAD_FOLDER'], rembg_img_name)

            # Call your background removal function here
            remove_background(file_path, rembg_img_path)

            # Convert processed image back to Base64 for the response
            with open(rembg_img_path, "rb") as processed_image_file:
                rembg_img_base64 = base64.b64encode(processed_image_file.read()).decode('utf-8')

            # Add original and processed image (in Base64) to the response list
            processed_images.append({
                'original_image': file_data,  # Original Base64 input
                'background_removed_image': rembg_img_base64  # Processed Base64 output
            })

        except Exception as e:
            return jsonify({"error": f"Failed to process image {idx}: {str(e)}"}), 500

    return jsonify({"processed_images": processed_images}), 200


if __name__ == '__main__':
    app.run(debug=True)