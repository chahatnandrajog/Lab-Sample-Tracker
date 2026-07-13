# 🧪 Lab Sample Tracker

A lightweight Laboratory Information Management System (LIMS) built with **FastAPI**, **SQLite**, **SQLAlchemy**, and a simple **HTML/CSS/JavaScript** frontend. The application helps users manage laboratory samples, validate uploaded CSV files, monitor sample statistics through a dashboard, and generate AI-powered summaries of laboratory data.

This project was built to strengthen my full-stack development skills by combining backend API development, database management, frontend integration, data validation, and AI-assisted analytics.

---

## 🚀 Features

### Sample Management
- Create new laboratory samples
- View all samples in a searchable table
- Retrieve individual sample records
- Automatically display validation status

### CSV Import & Validation
- Upload laboratory samples in bulk using CSV files
- Detect duplicate Sample IDs
- Validate required fields
- Validate temperature values
- Skip invalid records while importing valid ones
- Display detailed validation errors after upload

### Dashboard
- View total sample count
- Track valid and invalid samples
- Display summary statistics
- Update metrics in real time

### AI Summary
Generate an AI-powered summary of laboratory data, including:
- Overall data quality
- Validation issues
- Trends within uploaded samples
- Suggested improvements

Powered using the **Groq API**.

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| AI Integration | Groq API |
| Server | Uvicorn |

---

# 📁 Project Structure

```text
Lab-Sample-Tracker/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── ai_service.py    
│   └── routes/
│
├── static/
│   ├── style.css
│   └── script.js
│   └── index.html
│
├── data/
│
├── samples.csv
├── bad_samples.csv
│  
```

---

# 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/samples` | Retrieve all samples |
| GET | `/samples/{id}` | Retrieve a single sample |
| POST | `/samples` | Create a new sample |
| POST | `/upload-csv` | Upload and validate CSV data |
| GET | `/dashboard-summary` | Retrieve dashboard statistics |
| POST | `/generate-summary` | Generate an AI summary |

---

# ✅ CSV Validation

During upload, the application validates:

- Duplicate Sample IDs
- Missing required fields
- Invalid temperature values
- Invalid dates
- Empty rows

Only valid records are inserted into the database.

Example validation output:

```text
Imported 18 samples successfully.

Skipped:
- Duplicate Sample ID: S005
- Temperature 500°C is outside the allowed range
- Missing collection_date
```

---

# 🗄️ Database

The application uses **SQLite** with **SQLAlchemy** for data persistence.

Each sample record contains information such as:

- Sample ID
- Sample Name
- Collection Date
- Temperature
- Status
- Validation Status

---

# 🤖 AI Summary

The AI assistant analyzes uploaded laboratory data and provides:

- Overall laboratory health
- Common validation issues
- Data quality observations
- Recommendations for improving data integrity

Example output:

> The laboratory currently contains 42 samples. Most records are valid, with a small number of duplicate IDs detected during import. A few samples contain temperatures outside the expected range, suggesting possible collection or recording errors. Overall data quality is good with only minor validation issues.

---

# ▶️ Running the Project

## 1. Clone the repository

```bash
git clone https://github.com/chahatnandrajog/lab-sample-tracker.git
cd lab-sample-tracker
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

## 4. Open the application

Navigate to:

```
http://127.0.0.1:8000
```

or open the frontend using Live Server if applicable.

---

# 📈 Future Improvements

- User authentication and authorization
- Role-based access control
- Edit and delete sample records
- PostgreSQL support
- Docker containerization
- Cloud deployment
- Export data to CSV or PDF
- Interactive charts and analytics
- Audit history for sample changes

---

# 💡 Skills Demonstrated

- REST API development
- CRUD operations
- Database design
- SQLAlchemy ORM
- Frontend and backend integration
- File upload handling
- CSV parsing
- Data validation
- Exception handling
- AI API integration
- JSON processing
- Responsive UI development

---


# 🎯 Why I Built This

I built Lab Sample Tracker to gain hands-on experience developing a full-stack application that combines database management, REST APIs, frontend development, and AI integration. The project simulates a simplified laboratory information management system by allowing users to organize sample data, validate uploaded records, and generate intelligent summaries. Through this project, I strengthened my understanding of backend architecture, database interactions, API design, and building user-friendly applications.

---

## 📄 License

This project is licensed under the MIT License.
