# BAC Study Organizer

A comprehensive study management application for BAC (Baccalauréat) students. Organize modules, track exam scores, manage chapters, and monitor your overall academic progress.

## Features

- **Module Management**: Organize all BAC modules with customizable coefficients
- **Exam Tracking**: Record exam scores and upload PDF documents
- **Chapter Organization**: Structure study materials by chapters with resource links
- **Score Calculation**: Auto-calculate module averages and BAC final score
- **Manual Overrides**: Set custom averages per module when needed
- **Physical Education**: Dedicated PE entry with adjustable coefficient
- **Bilingual Support**: English and Arabic language support
- **Desktop & Web**: Run as both a desktop application (via PyWebView) and web interface

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Karim-tchakal/BAC_ASSIST.git
   cd BAC_ASSIST
   ```

2. Install **Python 3.14** (recommended for consistent results):
   - Download from [python.org/downloads](https://www.python.org/downloads/)
   - During installation, check **"Add Python to PATH"**

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Windows (Recommended)

Double-click **`run.bat`** — it will start the server and open the app automatically.

> No terminal needed. Just double-click and go.

### Manual / Development

```bash
python run.py
```

Or start just the web server:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then visit `http://127.0.0.1:8000` in your browser.

### Virtual Environment (Optional)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python run.py
```

## Project Structure

```
.
├── main.py              # FastAPI backend
├── run.py               # Desktop application launcher
├── run.bat              # Windows one-click launcher ⭐
├── static/
│   └── index.html       # Frontend UI
├── data/
│   └── app_data.json    # Application data storage
├── uploads/             # Uploaded PDF files
└── requirements.txt     # Python dependencies
```

## API Endpoints

### Modules
- `GET /api/modules` — Get all modules
- `PUT /api/modules/{module_id}/coefficient` — Update module coefficient
- `PUT /api/modules/{module_id}/override` — Set manual score override
- `DELETE /api/modules/{module_id}/override` — Remove score override

### Exams
- `GET /api/exams/{module_id}` — Get exams for a module
- `POST /api/exams/{module_id}` — Add new exam with optional PDF
- `PUT /api/exams/{module_id}/{exam_id}/score` — Update exam score
- `DELETE /api/exams/{module_id}/{exam_id}` — Delete exam

### Chapters
- `GET /api/chapters/{module_id}` — Get chapters for a module
- `POST /api/chapters/{module_id}` — Add new chapter
- `DELETE /api/chapters/{module_id}/{chapter_id}` — Delete chapter
- `POST /api/chapters/{module_id}/{chapter_id}/links` — Add study link
- `DELETE /api/chapters/{module_id}/{chapter_id}/links/{link_id}` — Delete link

### Stats
- `GET /api/stats` — Get statistics including BAC score calculation

## Default Modules

| Subject | Coefficient |
|---|---|
| Mathematics | 5 |
| Physics & Chemistry | 4 |
| Natural Sciences | 4 |
| Arabic Language | 3 |
| French Language | 3 |
| English Language | 2 |
| History & Geography | 2 |
| Islamic Studies | 2 |
| Philosophy | 2 |
| Physical Education | 1 |

All coefficients are editable from the Statistics page.

## Data Storage

Application data is stored in `data/app_data.json`:
- **modules**: Module definitions with coefficients and overrides
- **exams**: Exam records per module with scores and PDF paths
- **chapters**: Chapter structure per module with study links
- **notes**: Reserved for future note storage

Existing data is automatically migrated on upgrade — no need to reset.

## License

All rights reserved.