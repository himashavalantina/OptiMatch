# 🚀 OptiMatch AI

**OptiMatch AI** is an advanced AI-driven career companion that analyzes your CV and intelligently matches you with live job opportunities and recommended online courses. Originally developed as a Python CLI tool, OptiMatch AI has evolved into a full-stack web application featuring a modern Glassmorphism UI, real-time API integrations, and Natural Language Processing (NLP) for intelligent matching.

---

# ✨ Features

* 🧠 **AI-Powered Matching**
  Uses Scikit-Learn's **TF-IDF Vectorizer** and **Cosine Similarity** to match CV skills with job descriptions and course content.

* 🎨 **Premium Modern Interface**
  Responsive Glassmorphism UI with animated background orbs, drag-and-drop CV upload, and smooth layout animations.

* 💼 **Live Job Aggregation**
  Integrates with the **Jooble API** to fetch real, location-specific job postings.

* 📚 **Course Recommendations**
  Uses Kaggle Online Courses dataset to recommend relevant courses (Coursera, Udemy, etc.).

* ⚙️ **Customizable Search**
  Users can filter by preferred country and choose to search for **Jobs**, **Courses**, or **Both**.

---

# 🛠️ Technology Stack

## Backend

* Python 3
* Flask
* Flask-CORS
* Werkzeug

## AI / Data Engineering

* Pandas
* NumPy
* Scikit-Learn (TF-IDF, Cosine Similarity)

## Frontend

* HTML5
* CSS3 (Glassmorphism UI)
* Vanilla JavaScript
* FontAwesome

## PDF Processing

* PyPDF2

## External APIs

* Jooble API

---

# 📦 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/himashavalantina/OptiMatch.git
cd OptiMatch
```

## 2. Install Dependencies

Make sure Python 3 is installed, then run:

```bash
pip install -r requiremnets.txt
```

Ensure the following packages are included:

* flask
* flask-cors
* pandas
* scikit-learn
* PyPDF2
* requests

---

# 📊 Data Assets

Download a course dataset from Kaggle (e.g., **Online_Courses.csv**) and place it inside the `/data` folder:

```
OptiMatch/
 └── data/
      └── Online_Courses.csv
```

---

# 🔐 Environment Configuration

Currently, the Jooble API key is configured inside `app.py`.
For production environments, it is recommended to store the API key in a `.env` file.

Example:

```
JOOBLE_API_KEY=your_api_key_here
```

---

# 🚀 Running the Application

## Start Flask Backend

```bash
python app.py
```

## Open Web Interface

Go to:

```
http://127.0.0.1:5000
```

---

# 🖥️ Usage

1. Drag & drop your PDF Resume/CV into the upload area.
2. Enter an optional preferred country/location.
3. Click **Find My Matches**.
4. The system will generate:

   * Top Job Matches
   * Recommended Courses

---

# 📁 Project Structure

```
OptiMatch/
├── app.py                   # Main Flask API Server
├── main.py                  # Original CLI Script & Engine
├── utils.py                 # PDF Extraction & Job Fetching Scripts
├── requiremnets.txt         # Project Dependencies
├── data/
│   └── Online_Courses.csv   # Course Dataset
├── resumes/                 # Uploaded CV files
├── static/
│   ├── css/
│   │   └── style.css        # UI Styling
│   └── js/
│       └── script.js        # Frontend logic
└── templates/
    └── index.html           # Main Web Page
```

---

# 🎯 Future Improvements

* User accounts and login system
* Save job matches history
* Deploy to cloud (AWS / Azure / GCP)
* Use advanced NLP models (BERT / Sentence Transformers)
* Add LinkedIn job scraping
* Resume skill gap analysis

---

# 📜 License

This project is open-source and available under the MIT License.

---

# 👨‍💻 Author

**Himasha Valantina**
