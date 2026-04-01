
<h1>🚀 Smart Resume & Job Matcher (AI-Powered)</h1> 

An end-to-end Machine Learning application designed to bridge the gap between students and the industry. It analyzes a user's PDF resume, fetches live jobs from global markets, and recommends learning paths to fill identified skill gaps.

---

## 📌 Key Features
* **PDF Parsing:** Extracts structured text from unstructured PDF resumes using `PyPDF2`.
* **Live Job Fetching:** Real-time job data integration via the **Adzuna API**.
* **AI Matchmaking:** Uses **Natural Language Processing (NLP)** and **TF-IDF Vectorization** to calculate the similarity between candidate skills and job requirements.
* **Course Recommendations:** Suggests specialized courses from a dataset of online courses (Kaggle) based on identified skill gaps.

---

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Libraries:** `Scikit-learn` (Machine Learning), `Pandas` (Data Handling), `Requests` (API Calls), `PyPDF2` (PDF Processing).
* **NLP Techniques:** Tokenization, Stop-word removal, Cosine Similarity.

---

## ⚙️ How it Works

The system follows a standard Machine Learning pipeline to ensure accurate matching:

1.  **Text Processing:** The app cleans the resume text by removing punctuation and common "stop words" (e.g., "the", "and").
2.  **Vectorization:** The Resume and Job Descriptions are converted into mathematical vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)**.
3.  **Similarity Scoring:** We use **Cosine Similarity** to find the "distance" between the two vectors. 
    * *Closer to 1.0 = Strong Match.*
    * *Closer to 0.0 = Significant Skill Gap.*

---
