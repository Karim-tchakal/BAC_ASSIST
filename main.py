from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json, os, shutil, uuid
from pathlib import Path

app = FastAPI(title="BAC Study Organizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path("data/app_data.json")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

DEFAULT_MODULES = [
    {"id": "math",       "name_en": "Mathematics",          "name_ar": "الرياضيات",            "coefficient": 5, "color": "#FF6B35", "manual_override": None},
    {"id": "physics",    "name_en": "Physics & Chemistry",  "name_ar": "الفيزياء والكيمياء",   "coefficient": 4, "color": "#F7931E", "manual_override": None},
    {"id": "science",    "name_en": "Natural Sciences",     "name_ar": "علوم الطبيعة والحياة", "coefficient": 4, "color": "#FFB347", "manual_override": None},
    {"id": "arabic",     "name_en": "Arabic Language",      "name_ar": "اللغة العربية",         "coefficient": 3, "color": "#FF8C00", "manual_override": None},
    {"id": "french",     "name_en": "French Language",      "name_ar": "اللغة الفرنسية",        "coefficient": 3, "color": "#FFA500", "manual_override": None},
    {"id": "english",    "name_en": "English Language",     "name_ar": "اللغة الإنجليزية",      "coefficient": 2, "color": "#FFD700", "manual_override": None},
    {"id": "history",    "name_en": "History & Geography",  "name_ar": "التاريخ والجغرافيا",    "coefficient": 2, "color": "#FF7043", "manual_override": None},
    {"id": "islamic",    "name_en": "Islamic Studies",      "name_ar": "التربية الإسلامية",     "coefficient": 2, "color": "#FF6B6B", "manual_override": None},
    {"id": "philosophy", "name_en": "Philosophy",           "name_ar": "الفلسفة",               "coefficient": 2, "color": "#FF4081", "manual_override": None},
    {"id": "pe",         "name_en": "Physical Education",   "name_ar": "تربية بدنية",           "coefficient": 1, "color": "#4CAF7D", "manual_override": None},
]

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            data = {"modules": DEFAULT_MODULES, "exams": {}, "chapters": {}, "notes": {}}
            save_data(data)
            return data

        existing_ids = {m["id"] for m in data.get("modules", [])}
        defaults_by_id = {m["id"]: m for m in DEFAULT_MODULES}

        for m in data.get("modules", []):
            d = defaults_by_id.get(m.get("id"), {})
            if "name_en" not in m:
                m["name_en"] = d.get("name_en", m.get("name", m.get("id")))
            if "name_ar" not in m:
                m["name_ar"] = d.get("name_ar", m.get("name", m.get("id")))
            if "manual_override" not in m:
                m["manual_override"] = None

        for default_mod in DEFAULT_MODULES:
            if default_mod["id"] not in existing_ids:
                data["modules"].append({**default_mod})

        return data

    return {"modules": DEFAULT_MODULES, "exams": {}, "chapters": {}, "notes": {}}


def save_data(data):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def delete_file_if_exists(pdf_path: str):
    """Delete an upload file given its URL path like /uploads/filename.pdf"""
    if not pdf_path:
        return
    file_path = Path(pdf_path.lstrip("/"))
    if file_path.exists():
        file_path.unlink()

# ── Modules ──────────────────────────────────────────────────────────────────

@app.get("/api/modules")
def get_modules():
    return load_data()["modules"]

@app.put("/api/modules/{module_id}/coefficient")
def update_coefficient(module_id: str, coefficient: float = Form(...)):
    data = load_data()
    for m in data["modules"]:
        if m["id"] == module_id:
            m["coefficient"] = coefficient
            save_data(data)
            return m
    raise HTTPException(404, "Module not found")

@app.put("/api/modules/{module_id}/override")
def set_override(module_id: str, score: float = Form(...)):
    if not (0 <= score <= 20):
        raise HTTPException(400, "Score must be between 0 and 20")
    data = load_data()
    for m in data["modules"]:
        if m["id"] == module_id:
            m["manual_override"] = round(score, 2)
            save_data(data)
            return m
    raise HTTPException(404, "Module not found")

@app.delete("/api/modules/{module_id}/override")
def reset_override(module_id: str):
    data = load_data()
    for m in data["modules"]:
        if m["id"] == module_id:
            m["manual_override"] = None
            save_data(data)
            return m
    raise HTTPException(404, "Module not found")

# ── Exams ─────────────────────────────────────────────────────────────────────

@app.get("/api/exams/{module_id}")
def get_exams(module_id: str):
    data = load_data()
    return data["exams"].get(module_id, [])

@app.post("/api/exams/{module_id}")
async def add_exam(
    module_id: str,
    name: str = Form(...),
    score: Optional[float] = Form(None),
    pdf: Optional[UploadFile] = File(None)
):
    data = load_data()
    if module_id not in data["exams"]:
        data["exams"][module_id] = []

    exam_id = str(uuid.uuid4())[:8]
    pdf_path = None

    if pdf and pdf.filename:
        ext = Path(pdf.filename).suffix or ".pdf"
        # Readable filename: moduleId_examName.ext
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name).strip("_")
        base = f"{module_id}_{safe_name}"
        filename = f"{base}{ext}"
        # Append counter if file already exists: moduleId_examName_(2).pdf
        counter = 2
        while (UPLOAD_DIR / filename).exists():
            filename = f"{base}_({counter}){ext}"
            counter += 1
        dest = UPLOAD_DIR / filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(pdf.file, f)
        pdf_path = f"/uploads/{filename}"

    exam = {"id": exam_id, "name": name, "score": score, "pdf_path": pdf_path}
    data["exams"][module_id].append(exam)
    save_data(data)
    return exam

@app.put("/api/exams/{module_id}/{exam_id}/score")
def update_score(module_id: str, exam_id: str, score: float = Form(...)):
    data = load_data()
    for exam in data["exams"].get(module_id, []):
        if exam["id"] == exam_id:
            exam["score"] = score
            save_data(data)
            return exam
    raise HTTPException(404, "Exam not found")

@app.delete("/api/exams/{module_id}/{exam_id}")
def delete_exam(module_id: str, exam_id: str):
    data = load_data()
    exams = data["exams"].get(module_id, [])
    # Delete associated PDF file from disk
    for e in exams:
        if e["id"] == exam_id:
            delete_file_if_exists(e.get("pdf_path", ""))
            break
    data["exams"][module_id] = [e for e in exams if e["id"] != exam_id]
    save_data(data)
    return {"ok": True}

# ── Chapters ──────────────────────────────────────────────────────────────────

@app.get("/api/chapters/{module_id}")
def get_chapters(module_id: str):
    data = load_data()
    return data["chapters"].get(module_id, [])

@app.post("/api/chapters/{module_id}")
def add_chapter(module_id: str, title: str = Form(...)):
    data = load_data()
    if module_id not in data["chapters"]:
        data["chapters"][module_id] = []
    ch = {"id": str(uuid.uuid4())[:8], "title": title, "links": []}
    data["chapters"][module_id].append(ch)
    save_data(data)
    return ch

@app.delete("/api/chapters/{module_id}/{chapter_id}")
def delete_chapter(module_id: str, chapter_id: str):
    data = load_data()
    chs = data["chapters"].get(module_id, [])
    data["chapters"][module_id] = [c for c in chs if c["id"] != chapter_id]
    save_data(data)
    return {"ok": True}

@app.post("/api/chapters/{module_id}/{chapter_id}/links")
def add_link(module_id: str, chapter_id: str, title: str = Form(...), url: str = Form(...)):
    data = load_data()
    for ch in data["chapters"].get(module_id, []):
        if ch["id"] == chapter_id:
            link = {"id": str(uuid.uuid4())[:8], "title": title, "url": url}
            ch["links"].append(link)
            save_data(data)
            return link
    raise HTTPException(404)

@app.delete("/api/chapters/{module_id}/{chapter_id}/links/{link_id}")
def delete_link(module_id: str, chapter_id: str, link_id: str):
    data = load_data()
    for ch in data["chapters"].get(module_id, []):
        if ch["id"] == chapter_id:
            ch["links"] = [l for l in ch["links"] if l["id"] != link_id]
            save_data(data)
            return {"ok": True}
    raise HTTPException(404)

# ── Stats ─────────────────────────────────────────────────────────────────────

@app.get("/api/stats")
def get_stats():
    data = load_data()
    modules = data["modules"]
    exams = data["exams"]

    result = []
    total_coeff = 0
    weighted_sum = 0

    for m in modules:
        mid = m["id"]
        module_exams = exams.get(mid, [])
        scored = [e["score"] for e in module_exams if e.get("score") is not None and e["score"] > 0]
        auto_avg = sum(scored) / len(scored) if scored else None

        override = m.get("manual_override")
        effective_avg = override if override is not None else auto_avg
        pct = (effective_avg / 20 * 100) if effective_avg is not None else 0

        result.append({
            **m,
            "auto_average": auto_avg,
            "average": effective_avg,
            "is_overridden": override is not None,
            "percentage": pct,
            "exam_count": len(module_exams),
            "scored_count": len(scored)
        })

        if effective_avg is not None:
            total_coeff += m["coefficient"]
            weighted_sum += effective_avg * m["coefficient"]

    bac_score = weighted_sum / total_coeff if total_coeff > 0 else None
    return {"modules": result, "bac_score": bac_score, "total_coeff": total_coeff}

# ── Static files ──────────────────────────────────────────────────────────────

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/{path:path}")
def spa(path: str):
    return FileResponse("static/index.html")