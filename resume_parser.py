"""Resume parsing: text extraction + NLP-based information extraction."""
import io
import re
from skills import SKILLS, ALIASES

try:
    import spacy
    _nlp = spacy.load("en_core_web_sm")
except Exception:          # spaCy / model not installed -> fallback to heuristics
    _nlp = None

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?91[\s-]?)?[6-9]\d{9}|\+?\d[\d\s-]{9,14}\d")
EXP_RE = re.compile(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)", re.I)
EDU_RE = re.compile(
    r"\b(b\.?\s?e\.?|b\.?\s?tech|m\.?\s?tech|m\.?\s?e\.?|b\.?\s?sc|m\.?\s?sc|b\.?\s?c\.?a|m\.?\s?c\.?a|"
    r"mba|ph\.?d|diploma|bachelor[^,\n]*|master[^,\n]*)\b", re.I)


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Read text from PDF, DOCX or TXT."""
    name = filename.lower()
    if name.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join((p.extract_text() or "") for p in pdf.pages)
    if name.endswith(".docx"):
        import docx
        d = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in d.paragraphs)
    return file_bytes.decode("utf-8", errors="ignore")


def extract_skills(text: str) -> set:
    """Dictionary + alias based skill extraction with word-boundary regex."""
    t = text.lower()
    found = set()
    terms = {s: s for s in SKILLS}
    terms.update(ALIASES)
    for term, canon in terms.items():
        pattern = r"(?<![\w+#.])" + re.escape(term) + r"(?![\w+#])"
        if re.search(pattern, t):
            found.add(canon)
    return found


def extract_name(text: str) -> str:
    if _nlp:
        doc = _nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
    for line in text.splitlines():
        line = line.strip()
        words = line.split()
        if 1 < len(words) <= 4 and all(w.replace(".", "").isalpha() for w in words):
            return line.title()
    return "Not found"


def parse_resume(text: str) -> dict:
    email = EMAIL_RE.search(text)
    phone = PHONE_RE.search(text)
    years = [float(x) for x in EXP_RE.findall(text)]
    education = sorted({m.group(0).strip() for m in EDU_RE.finditer(text)})
    return {
        "name": extract_name(text),
        "email": email.group(0) if email else "Not found",
        "phone": phone.group(0).strip() if phone else "Not found",
        "education": education or ["Not found"],
        "experience_years": max(years) if years else 0,
        "skills": sorted(extract_skills(text)),
    }
