# Automated Resume Parser & Job Matching System (NLP)

## Run
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm     # optional (better name detection)
streamlit run app.py
```
Upload `sample_resume.txt` (or any PDF/DOCX resume) in the browser.

## How it works
1. **Text extraction** - pdfplumber (PDF), python-docx (DOCX), plain TXT
2. **Information extraction** - Regex (email, phone, experience, education), spaCy NER (name), dictionary + alias matching (skills)
3. **Matching** - TF-IDF (unigram+bigram) cosine similarity between resume and job + skill-overlap ratio
4. **Final score** = 0.4 x text similarity + 0.6 x skill match (adjustable in sidebar)
5. **Output** - ranked jobs, matched/missing skills, recommendation

## Files
app.py (UI) | resume_parser.py (parsing) | matcher.py (matching) | skills.py (skill DB) | jobs.csv (job data)

## Future scope
BERT/Sentence-Transformers embeddings, OCR for scanned resumes, live job APIs, database storage.
