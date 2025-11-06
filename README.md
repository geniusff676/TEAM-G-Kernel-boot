# 🎯 AI-Powered Personalized Career & Course Recommendation System

> **Status**: 🚧 Proposed Solution | Concept Phase  
> **Domain**: AI/ML (Primary) | **Subdomain**: Web Development (Frontend + Backend Integration)  
> **Core Focus**: Personalized course, career path, and university resource recommendations based on student academic data

---

## 🚀 Project Overview

This project proposes an **AI-powered personalized guidance system** for students that will recommend:

- ✅ **Courses** based on their GPA, interests, skills, and career goals
- ✅ **Career paths & roadmaps** personalized to their academic strengths
- ✅ **University resources** such as hackathons, clubs, and events relevant to their interests
- ✅ **Career counselling chatbot** to answer student queries interactively

The system will intelligently connect a student's profile with the right learning and career opportunities — all through a unified dashboard.

---

## 🧱 Proposed System Architecture
```
            ┌────────────────────────────┐
            │     Student Profile        │
            │ GPA | Skills | Projects    │
            └──────────────┬─────────────┘
                           │
                           ▼
        ┌────────────────────────────┐
        │    Recommendation Engine   │
        │ Content-based + ML Hybrid  │
        └──────────────┬─────────────┘
                           │
        ┌─────────────────┼───────────────────┐
        ▼                 ▼                   ▼
 Course Recommender   Career Roadmap     University Resources
 (Coursera/Udemy)     Generator (LLM)    (Hackathons, Clubs, etc.)
        │                 │                   │
        ▼                 ▼                   ▼
     Frontend Dashboard + Chatbot + Visualization Layer
```

---

## 🧩 Core Modules (Proposed)

### 1️⃣ Data Collection & Student Profiling

We plan to collect structured user data to build a comprehensive student profile:

| Field | Example | Purpose |
|-------|---------|---------|
| Name / Major | CSE | Filter domain-specific content |
| GPA / CGPA | 8.1 / 10 | Determines level & difficulty |
| Skills | Python, ML, Web Dev | Helps content-based matching |
| Desired Role | Data Scientist | Used to map relevant learning paths |
| Previous Courses / Projects | NLP chatbot, CNN model | Used for contextual recommendations |

All this data will form the **student knowledge graph**, which powers downstream recommendations.

---

### 2️⃣ Course Recommendation Engine

#### 🧠 Objective
To recommend personalized courses based on the user's background, skill set, and desired role.

#### 📚 Proposed Data Sources

**Static Dataset:**
- Public course datasets from Kaggle (e.g., Coursera, Udemy, edX course datasets)
- Used for model training and offline experimentation

**Live Data (Dynamic):**
- Real-time course fetching using APIs or scraping:
  - **Coursera API**: `https://api.coursera.org/api/courses.v1`
  - **Udemy API**: `https://www.udemy.com/api-2.0/courses`
  - For other platforms (edX, university portals): scraping using BeautifulSoup / Playwright

#### 🧩 Proposed Techniques

| Approach | Description |
|----------|-------------|
| **Content-Based Filtering** | Match student's interests & skills with course descriptions using NLP (TF-IDF, cosine similarity, or sentence-transformers) |
| **ML-Based Recommendation (Hybrid)** | Train a regression/classification model to predict "course relevance score" based on GPA, skill overlap, and topic embeddings |
| **Keyword Extraction** | Use KeyBERT / spaCy to extract key topics from course descriptions |

#### ⚙️ Proposed Implementation Flow
1. Fetch & preprocess data → clean course text
2. Extract embeddings (Sentence-BERT or TF-IDF)
3. Match student profile vector to course vectors
4. Rank top-10 recommended courses

---

### 3️⃣ Career Path & Roadmap Generator

#### 🎯 Objective
Recommend personalized career paths and learning roadmaps aligned with the user's role (e.g., "Machine Learning Engineer", "Full-Stack Developer").

#### 🔍 Proposed Approach
- Use the student's skills + GPA + desired role to infer their readiness level
- Generate a roadmap using:
  - **Predefined templates** (structured JSON of learning paths)
  - **AI-based generation** using LLMs (e.g., GPT, Mistral, or Llama3) to suggest next steps dynamically

#### 🧠 Example Output

For a student wanting to be a **Data Scientist**:
```
1️⃣ Learn Statistics and Probability
2️⃣ Master Python for Data Analysis
3️⃣ Learn Machine Learning Algorithms
4️⃣ Work on Kaggle projects
5️⃣ Build portfolio with real datasets
6️⃣ Apply for internships / research roles
```

---

### 4️⃣ AI Chatbot – Career & Academic Counsellor

#### 💬 Proposed Functionality
A conversational chatbot that:
- Guides users on "What course should I take next?"
- Answers questions like "How do I become a Data Scientist?"
- Gives resource links and personalized tips

#### 🧰 Proposed Tech Stack
- **LLM Backend**: OpenAI / HuggingFace API
- **Frontend**: React/Next.js chatbot interface
- **Integration**: RAG (Retrieval-Augmented Generation) for personalized responses using user's profile + fetched courses

---

### 5️⃣ University Resource Integration

#### 🎓 Objective
Connect students with university opportunities such as:
- Hackathons
- Technical Club Events
- Research or Innovation Cells
- Campus Career Fairs

#### 🔍 Proposed Implementation
- Scrape university websites (using BeautifulSoup or Selenium) to extract event names, dates, and descriptions
- Store in a local DB or API endpoint
- Filter events relevant to the student's interests (e.g., "AI Hackathon" for ML students)

#### 🧩 Example Scraping Approach
```python
url = "https://university.edu/events"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

events = [div.text for div in soup.find_all("div", class_="event-card")]
```

Then match these events with students' skill tags to show personalized university opportunities.

---

## 🧠 Proposed Tech Stack

| Layer | Tools & Frameworks |
|-------|-------------------|
| **Frontend** | React / Next.js + Tailwind + Chart.js |
| **Backend** | Flask / FastAPI |
| **ML & NLP** | Scikit-learn, SentenceTransformers, KeyBERT |
| **Database** | PostgreSQL / MongoDB |
| **Scraping & APIs** | BeautifulSoup, Selenium, Coursera API, Udemy API |
| **Chatbot / LLMs** | OpenAI GPT API or local Llama model |
| **Hosting** | Render / Vercel / AWS |

---

## 📊 Innovation Points

✅ Combines static ML recommendations with real-time web-scraped data  
✅ Provides career roadmap generation using LLM reasoning  
✅ Integrates university resources and live hackathon listings  
✅ Includes a chatbot-based interface for smart counselling  
✅ Fully modular design → scalable and extendable  

---

## 🧩 Future Enhancements (Phase 2+)

- Fine-tune transformer models for personalized recommendation
- Integrate LinkedIn or GitHub API for auto-fetching user projects
- Add resume analyzer for skill-gap detection
- Include gamified progress tracker for learning milestones
- Implement collaborative filtering using student interaction data
- Build mobile application (React Native / Flutter)

---

## 📝 Project Status

**Current Phase**: Conceptualization & Research  
**Next Steps**: 
1. Finalize tech stack and architecture
2. Collect and preprocess datasets
3. Build MVP with basic course recommendation
4. Integrate LLM-based chatbot
5. Deploy alpha version for testing

---

## 👥 Team & Contributions

*Anmol Garg , Rohit Sharma , rohit choudhary*

---

## 📄 License

*[Add license information if applicable]*

---

## 🔗 References & Resources

- [Coursera Dataset - Kaggle](https://www.kaggle.com/datasets/siddharthm1698/coursera-course-dataset)
- [Udemy API Documentation](https://www.udemy.com/developers/affiliate/)
- [SentenceTransformers Documentation](https://www.sbert.net/)
- [KeyBERT for Keyword Extraction](https://github.com/MaartenGr/KeyBERT)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

**Note**: This is a proposed solution and concept design. Implementation details may evolve during development based on technical feasibility and resource availability.