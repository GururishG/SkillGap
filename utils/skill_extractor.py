import re
from typing import List
from data.skills_database import SKILLS_DATABASE

def extract_skills_from_pdf(file) -> List[str]:
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return extract_skills_from_text(text)
    except ImportError:
        try:
            import pdfplumber
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return extract_skills_from_text(text)
        except ImportError:
            return []

def extract_skills_from_docx(file) -> List[str]:
    try:
        from docx import Document
        doc = Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return extract_skills_from_text(text)
    except ImportError:
        return []

def extract_skills_from_text(text: str) -> List[str]:
    all_skills = []
    for category in SKILLS_DATABASE.values():
        all_skills.extend(category)
    
    text_lower = text.lower()
    
    lines = [line.strip() for line in text.replace(',', '\n').split('\n')]
    
    found_skills = set()
    
    for skill in all_skills:
        skill_lower = skill.lower()
        
        if skill_lower in text_lower:
            found_skills.add(skill)
        
        for line in lines:
            line_clean = line.strip().lower()
            if line_clean == skill_lower or (len(line_clean) > 0 and skill_lower == line_clean):
                found_skills.add(skill)
    
    for line in lines:
        line_clean = line.strip()
        if len(line_clean) > 1 and len(line_clean) < 30:
            for skill in all_skills:
                if line_clean.lower() == skill.lower():
                    found_skills.add(skill)
    
    return sorted(list(found_skills))
