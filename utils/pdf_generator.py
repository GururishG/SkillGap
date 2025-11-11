from io import BytesIO
from typing import Dict, List, Any

def generate_results_pdf(results: Dict[str, Any], user_skills: List[str]) -> BytesIO:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph("SkillGap Analysis Report", styles['Title']))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph(f"Target Role: {results.get('target_role', 'N/A')}", styles['Heading2']))
        elements.append(Paragraph(f"Overall Match Score: {results.get('overall_match_score', 0):.1f}%", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph("Your Skills:", styles['Heading2']))
        skills_text = ", ".join(user_skills)
        elements.append(Paragraph(skills_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        if results.get('matching_skills'):
            elements.append(Paragraph("Matching Skills:", styles['Heading2']))
            matching_text = ", ".join(results['matching_skills'])
            elements.append(Paragraph(matching_text, styles['Normal']))
            elements.append(Spacer(1, 12))
        
        if results.get('missing_skills'):
            elements.append(Paragraph("Skills to Develop:", styles['Heading2']))
            missing_text = ", ".join(results['missing_skills'])
            elements.append(Paragraph(missing_text, styles['Normal']))
            elements.append(Spacer(1, 12))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    except ImportError:
        buffer = BytesIO()
        buffer.write(b"PDF generation requires reportlab package. Install with: pip install reportlab")
        buffer.seek(0)
        return buffer
