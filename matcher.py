"""Job matching: TF-IDF cosine similarity + skill-overlap score."""
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_skills


def clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def match_jobs(resume_text: str, resume_skills: set, jobs: pd.DataFrame,
               w_text: float = 0.4, w_skill: float = 0.6) -> pd.DataFrame:
    """Return jobs ranked by final match score (0-100)."""
    job_docs = (jobs["title"] + " " + jobs["description"] + " " + jobs["skills"].str.replace(";", " ")).map(clean)
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    X = vec.fit_transform([clean(resume_text)] + job_docs.tolist())
    text_sim = cosine_similarity(X[0], X[1:])[0]

    rows = []
    for i, job in jobs.reset_index(drop=True).iterrows():
        required = {s.strip().lower() for s in job["skills"].split(";") if s.strip()}
        matched = required & resume_skills
        missing = required - resume_skills
        skill_score = len(matched) / len(required) if required else 0
        final = w_text * min(text_sim[i] * 2.5, 1.0) + w_skill * skill_score   # scale: raw tf-idf sims are small
        rows.append({
            "Job Title": job["title"], "Company": job["company"],
            "Match %": round(final * 100, 1),
            "Text Similarity %": round(text_sim[i] * 100, 1),
            "Skill Match %": round(skill_score * 100, 1),
            "Matched Skills": ", ".join(sorted(matched)) or "-",
            "Missing Skills": ", ".join(sorted(missing)) or "-",
        })
    return pd.DataFrame(rows).sort_values("Match %", ascending=False).reset_index(drop=True)


def job_from_text(title: str, jd_text: str) -> pd.DataFrame:
    """Build a one-row job table from a pasted job description."""
    skills = ";".join(sorted(extract_skills(jd_text)))
    return pd.DataFrame([{"title": title or "Custom Job", "company": "Custom", "description": jd_text, "skills": skills}])
