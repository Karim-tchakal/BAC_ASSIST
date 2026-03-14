# BAC Study Organizer

A comprehensive study management application for BAC (Baccalauréat) students. Organize modules, track exam scores, manage chapters, and monitor your overall academic progress.

## Features

- **Module Management**: Organize all BAC modules with customizable coefficients
- **Exam Tracking**: Record exam scores and upload PDF documents
- **Chapter Organization**: Structure study materials by chapters with resource links
- **Score Calculation**: Auto-calculate module averages and BAC final score
- **Manual Overrides**: Set custom averages per module when needed
- **Bilingual Support**: English and Arabic language support
- **Desktop & Web**: Run as both a desktop application (via PyWebView) and web interface

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- PyWebView
- python-multipart

## Installation

1. Clone or download this project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Desktop Application (PyWebView)
```bash
python run.py
```
This launches the application in a native desktop window.

### Web Server Only
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```
Then visit `http://127.0.0.1:8000` in your browser.

## Project Structure

```
.
├── main.py              # FastAPI backend
├── run.py               # Desktop application launcher
├── static/
│   └── index.html       # Frontend UI
├── data/
│   └── app_data.json    # Application data storage
├── uploads/             # Uploaded PDF files
└── requirements.txt     # Python dependencies
```

## API Endpoints

### Modules
- `GET /api/modules` - Get all modules
- `PUT /api/modules/{module_id}/coefficient` - Update module coefficient
- `PUT /api/modules/{module_id}/override` - Set manual score override
- `DELETE /api/modules/{module_id}/override` - Remove score override

### Exams
- `GET /api/exams/{module_id}` - Get exams for a module
- `POST /api/exams/{module_id}` - Add new exam with optional PDF
- `PUT /api/exams/{module_id}/{exam_id}/score` - Update exam score
- `DELETE /api/exams/{module_id}/{exam_id}` - Delete exam

### Chapters
- `GET /api/chapters/{module_id}` - Get chapters for a module
- `POST /api/chapters/{module_id}` - Add new chapter
- `DELETE /api/chapters/{module_id}/{chapter_id}` - Delete chapter
- `POST /api/chapters/{module_id}/{chapter_id}/links` - Add study link
- `DELETE /api/chapters/{module_id}/{chapter_id}/links/{link_id}` - Delete link

### Stats
- `GET /api/stats` - Get statistics including BAC score calculation

## Default Modules

- Mathematics (Coefficient: 5)
- Physics & Chemistry (Coefficient: 4)
- Natural Sciences (Coefficient: 4)
- Arabic Language (Coefficient: 3)
- French Language (Coefficient: 3)
- English Language (Coefficient: 2)
- History & Geography (Coefficient: 2)
- Islamic Studies (Coefficient: 2)
- Philosophy (Coefficient: 2)

## Data Storage

Application data is stored in `data/app_data.json` with the following structure:
- **modules**: Module definitions with coefficients and overrides
- **exams**: Exam records per module with scores and PDF paths
- **chapters**: Chapter structure per module with study links
- **notes**: Reserved for future note storage

## License

All rights reserved.
