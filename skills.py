"""Skill dictionary used for skill extraction (add more as you like)."""
SKILLS = [
    # programming
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "sql", "r", "go", "php", "kotlin", "swift", "matlab",
    # web
    "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi", "spring boot", "bootstrap", "rest api",
    # data / ml / nlp
    "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "data analysis",
    "data science", "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "spacy", "nltk", "transformers",
    "tableau", "power bi", "excel", "statistics", "data visualization", "matplotlib", "opencv",
    # databases
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "firebase", "redis",
    # devops / cloud / tools
    "git", "github", "docker", "kubernetes", "aws", "azure", "gcp", "linux", "jenkins", "ci/cd", "jira", "postman",
    # testing / general
    "selenium", "junit", "manual testing", "automation testing", "agile", "scrum", "oop", "data structures", "algorithms",
    # embedded / networking / misc
    "arduino", "raspberry pi", "iot", "embedded c", "networking", "cyber security", "android", "flutter",
]

# alias -> canonical skill
ALIASES = {
    "js": "javascript", "reactjs": "react", "react.js": "react", "nodejs": "node.js", "node": "node.js",
    "ml": "machine learning", "dl": "deep learning", "sklearn": "scikit-learn", "scikit learn": "scikit-learn",
    "postgres": "postgresql", "mongo": "mongodb", "k8s": "kubernetes", "powerbi": "power bi",
    "ds": "data structures", "dsa": "data structures", "oops": "oop", "rest apis": "rest api", "restful api": "rest api",
}
