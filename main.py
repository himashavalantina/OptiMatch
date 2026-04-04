from utils import extract_text_from_pdf, fetch_jooble_jobs
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os # Added to check if files exist

# --- 🔑 CONFIGURATION ---
JOOBLE_KEY = {enter the key here}

def get_recommendations(resume_text, target_texts):
    if not target_texts:
        return []
    vectorizer = TfidfVectorizer(stop_words='english')
    all_texts = [resume_text] + target_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return scores[0]

def run_skill_bridge():
    print("--- 🚀 OptiMatch AI Starting ---")
    
    resume_path = "resumes/valantina.pdf" 
    print(f"🔍 Looking for resume at: {resume_path}")
    
    resume_text = extract_text_from_pdf(resume_path)
    
    if not resume_text:
        print(f"❌ Could not find or read {resume_path}. Check your folder!")
        return

    # ==========================================
    # 💼 PART 1: JOB MATCHING
    # ==========================================
    print("\n✅ Resume loaded. Fetching jobs...")
    query_skills = "Software" # Kept broad so you always get results
    jobs = fetch_jooble_jobs(query_skills, JOOBLE_KEY, location="") 
    
    if jobs:
        print(f"✅ Found {len(jobs)} jobs. Calculating matches...")
        job_descriptions = [j.get('snippet', '') + " " + j.get('title', '') for j in jobs]
        job_scores = get_recommendations(resume_text, job_descriptions)

        print("\n--- 💼 Top 5 Job Matches ---")
        # Let's sort the jobs by score so the best ones are at the top!
        job_results = []
        for i, job in enumerate(jobs):
            score = job_scores[i] if len(job_scores) > i else 0
            job_results.append((score, job.get('title', 'Unknown'), job.get('company', 'Unknown')))
        
        job_results.sort(reverse=True, key=lambda x: x[0]) # Sort descending
        
        for score, title, company in job_results[:5]: # Only print top 5
            print(f"Match: {score*100:.1f}% | {title} at {company}")
    else:
        print("❌ No jobs found.")

    # ==========================================
    # 📚 PART 2: COURSE RECOMMENDATIONS
    # ==========================================
    print("\n--- 📚 Recommended Courses ---")
    course_file = "data/Online_Courses.csv"

    if os.path.exists(course_file):
        print(f"✅ Found {course_file}. Analyzing course dataset...")
        try:
            # Read the CSV file
            courses_df = pd.read_csv(course_file)
            
            # --- 🧹 THE FIX: DATA CLEANING ---
            # Replace all empty cells (NaN) with blank text so the AI doesn't crash
            courses_df = courses_df.fillna("")
            
            # Combine all text in the row to make sure we don't miss any skills!
            courses_df['combined_text'] = courses_df.astype(str).agg(' '.join, axis=1)
            
            # Run the AI Math!
            course_scores = get_recommendations(resume_text, courses_df['combined_text'].tolist())
            courses_df['Match_Score'] = course_scores
            
            # Get Top 5 Courses
            top_courses = courses_df.sort_values(by='Match_Score', ascending=False).head(5)

            for index, row in top_courses.iterrows():
                # We try to automatically find the 'Title' or 'Name' column from the Kaggle dataset
                # Exclude 'unnamed' to avoid picking up index columns like 'Unnamed: 0'
                title_col = next((col for col in courses_df.columns if ('title' in col.lower() or 'name' in col.lower()) and 'unnamed' not in col.lower()), courses_df.columns[0])
                title = row[title_col]
                print(f"Course Match: {row['Match_Score']*100:.1f}% | {title}")

        except Exception as e:
            print(f"❌ Error processing {course_file}. Make sure it is a valid CSV. Error: {e}")
    else:
        print(f"⚠️ '{course_file}' not found in the folder.")
        print("💡 ACTION REQUIRED: Download a course dataset from Kaggle, name it 'courses.csv', and place it in the OptiMatch folder.")

if __name__ == "__main__":
    run_skill_bridge()