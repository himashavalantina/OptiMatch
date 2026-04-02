from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
from utils import extract_text_from_pdf, fetch_jooble_jobs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'resumes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

JOOBLE_KEY = "2d506b3a-2fdb-4f12-a3a4-a47937a0a87d" 

def get_recommendations(resume_text, target_texts):
    if not target_texts:
        return []
    vectorizer = TfidfVectorizer(stop_words='english')
    all_texts = [resume_text] + target_texts
    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        return scores[0]
    except Exception as e:
        print(f"TFIDF Error: {e}")
        return [0] * len(target_texts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/match', methods=['POST'])
def match():
    if 'cv' not in request.files:
        return jsonify({"error": "No CV file provided"}), 400
    
    cv_file = request.files['cv']
    if cv_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    country = request.form.get('country', '')
    match_type = request.form.get('type', 'both') # 'jobs', 'courses', 'both'
    
    filename = secure_filename(cv_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cv_file.save(filepath)
    
    resume_text = extract_text_from_pdf(filepath)
    if not resume_text:
        return jsonify({"error": "Could not extract text from the PDF. Make sure it is a valid text-based PDF."}), 400
        
    response_data = {}
    
    if match_type in ['jobs', 'both']:
        jobs = fetch_jooble_jobs("Software", JOOBLE_KEY, location=country)
        job_results = []
        if jobs:
            job_descriptions = [j.get('snippet', '') + " " + j.get('title', '') for j in jobs]
            job_scores = get_recommendations(resume_text, job_descriptions)
            for i, job in enumerate(jobs):
                score = job_scores[i] if len(job_scores) > i else 0
                job_results.append({
                    "score": round(score * 100, 1),
                    "title": job.get('title', 'Unknown Title'),
                    "company": job.get('company', 'Unknown Company'),
                    "url": job.get('link', '#'),
                    "location": job.get('location', '')
                })
            job_results.sort(reverse=True, key=lambda x: x['score'])
            response_data['jobs'] = job_results[:5]
        else:
            response_data['jobs'] = []

    if match_type in ['courses', 'both']:
        course_file = "data/Online_Courses.csv"
        if os.path.exists(course_file):
            courses_df = pd.read_csv(course_file).fillna("")
            courses_df['combined_text'] = courses_df.astype(str).agg(' '.join, axis=1)
            course_scores = get_recommendations(resume_text, courses_df['combined_text'].tolist())
            courses_df['Match_Score'] = course_scores
            top_courses = courses_df.sort_values(by='Match_Score', ascending=False).head(5)
            
            course_results = []
            for index, row in top_courses.iterrows():
                title_col = next((col for col in courses_df.columns if ('title' in col.lower() or 'name' in col.lower()) and 'unnamed' not in col.lower()), courses_df.columns[0])
                url_col = next((col for col in courses_df.columns if 'url' in col.lower() or 'link' in col.lower()), None)
                title = row[title_col]
                url = row[url_col] if url_col else '#'
                course_results.append({
                    "score": round(row['Match_Score'] * 100, 1),
                    "title": title,
                    "url": url,
                    "platform": row.get('Site', 'Online Provider') if 'Site' in row else 'Online Course'
                })
            response_data['courses'] = course_results
        else:
            response_data['courses'] = []
            response_data['course_error'] = "Course dataset not found."

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
