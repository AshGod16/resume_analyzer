from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
from docx import Document
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API using environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are a senior recruiter with 10+ years of experience in tech hiring. Analyze this resume against the provided job description and provide specific, actionable feedback in the following format:\
\
1. Overall Match Assessment: Initial evaluation of how well the resume aligns with the role.\
\
2. Key Skills Match:\
   * Strong Matches: Skills and experiences that align perfectly\
   * Partial Matches: Areas where experience exists but needs better highlighting\
   * Missing Skills: Critical requirements that aren't addressed\
\
3. Experience Relevance:\
   * High-Impact Points: Experience that directly maps to role requirements\
   * Areas for Improvement: How to better frame existing experience\
   * Missing Requirements: Critical experience gaps to address\
\
4. Specific Improvement Suggestions:\
   * Quantify: Identify where to add metrics and numbers\
   * Keywords: Important terms from the JD to incorporate\
   * Reframing: How to better present existing experience\
   * Formatting: Structural improvements for better readability\
\
Keep your feedback constructive, specific, and actionable. Focus on how to enhance rather than just what's missing."
    )

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded'}), 400
    
    file = request.files['resume']
    job_description = request.form.get('jobDescription', '')
    
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Extract text based on file type
            if filename.endswith('.pdf'):
                resume_text = extract_text_from_pdf(file_path)
            else:  # docx
                resume_text = extract_text_from_docx(file_path)
            
            # Clean up the uploaded file
            os.remove(file_path)
            
            # Prepare prompt for Gemini
            prompt = f"""
            Please analyze this resume against the job description. Consider:
            1. Key skills match
            2. Experience relevance
            3. Missing critical requirements
            4. Suggested improvements
            
            Resume:
            {resume_text}
            
            Job Description:
            {job_description}
            """
            
            # Get analysis from Gemini
            response = model.generate_content(
                prompt,
                generation_config = genai.GenerationConfig(
                    temperature=0.2,
                ))
            analysis = response.text
            
            return jsonify({'analysis': analysis})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)