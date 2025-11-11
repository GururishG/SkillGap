# SkillGap Analyzer

## Overview

SkillGap Analyzer is a career development web application built with Streamlit that helps users identify skill gaps for target job roles. The application analyzes user skills (extracted from resumes or manual input), compares them against job role requirements, and provides personalized career guidance, learning paths, and skill assessments through interactive quizzes.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Choice: Streamlit**
- **Problem**: Need for rapid development of an interactive data application with minimal frontend code
- **Solution**: Streamlit framework for Python-based web applications
- **Rationale**: Streamlit enables data scientists and Python developers to create web apps without JavaScript/HTML/CSS knowledge, with built-in support for data visualization and interactivity
- **Key Features**:
  - Session state management for user data persistence across interactions
  - Wide layout mode for dashboard-style interface
  - Component-based structure with expandable sidebar navigation

**Visualization Framework: Plotly**
- **Solution**: Plotly Express and Graph Objects for interactive charts
- **Purpose**: Create dynamic, interactive visualizations for skill gap analysis, career progression, and quiz results
- **Benefits**: Rich interactivity, professional appearance, and seamless Streamlit integration

### Application Logic Architecture

**Modular Utility Structure**
- **Design Pattern**: Separation of concerns with dedicated utility modules
- **Components**:
  1. **Skill Extractor** (`utils/skill_extractor.py`): Extracts skills from PDF/DOCX resumes or plain text using pattern matching against skill database
  2. **Skill Analyzer** (`utils/skill_analyzer.py`): Compares user skills against job role requirements, calculates match scores with weighted scoring (70% required skills, 30% preferred skills)
  3. **Career Advisor** (`utils/career_advisor.py`): Provides contextual career advice based on skill match levels (high/medium/low match categories)
  4. **Quiz Generator** (`utils/quiz_generator.py`): Creates skill assessment quizzes from predefined question banks
  5. **PDF Generator** (`utils/pdf_generator.py`): Generates downloadable analysis reports using ReportLab

**Class-Based Services**
- `SkillAnalyzer`, `CareerAdvisor`, and `QuizGenerator` use class-based architecture for stateful operations and configuration management
- Enables instantiation with custom configurations and maintains internal state for templates and question banks

### Data Architecture

**Static Data Storage**
- **Approach**: Python dictionaries and lists in dedicated data modules
- **Rationale**: For this application scale, static data structures provide simplicity without database overhead
- **Data Models**:
  1. **Skills Database** (`data/skills_database.py`): Categorized skills (technical, soft skills, business) and job role definitions with required/preferred skills and salary ranges
  2. **Career Templates** (`data/career_templates.py`): Career progression paths and structured learning paths for skills

**Session State Management**
- **Technology**: Streamlit's built-in session state
- **Purpose**: Persist user data across page interactions without backend database
- **Stored Data**:
  - User profile (name, experience level, target role)
  - Analysis results and history
  - Active and completed quizzes
  - Learning paths and preferences
  - Unique user ID (UUID-based)
  - Current page selection (for stable navigation)

**Navigation Stability**
- **Challenge**: Streamlit reruns the entire script on user interactions (e.g., clicking radio buttons), which could reset page selection
- **Solution**: `st.session_state.current_page` persists the active page across reruns
- **Implementation**:
  - Sidebar selectbox uses `current_page` as its index value
  - Page changes update `current_page` and trigger `st.rerun()` for UI sync
  - Auto-redirect after skill analysis updates `current_page` before rerunning
- **Benefit**: Users can interact with quizzes (clicking radio buttons) without unexpected navigation

### Document Processing Pipeline

**Multi-Format Resume Parser**
- **Supported Formats**: PDF (PyPDF2/pdfplumber), DOCX (python-docx), plain text
- **Processing Strategy**: 
  1. Extract raw text from documents
  2. Normalize text (lowercase conversion)
  3. Pattern match against comprehensive skill database
  4. Return deduplicated skill set
- **Fallback Mechanism**: Multiple PDF parsing libraries (PyPDF2 primary, pdfplumber fallback) for reliability

### Scoring Algorithm

**Skill Match Calculation**
- **Weighted Scoring Model**:
  - Required skills: 70% weight
  - Preferred skills: 30% weight
- **Formula**: `Overall Score = (Required Match % × 0.7) + (Preferred Match % × 0.3)`
- **Output**: Percentage-based match score with categorized readiness levels

### Report Generation

**PDF Export System**
- **Library**: ReportLab for programmatic PDF creation
- **Content Structure**: Title, role information, match score, user skills, matching skills, and skill gaps
- **Error Handling**: Graceful degradation with explanatory message if ReportLab unavailable

## External Dependencies

### Core Framework
- **Streamlit**: Web application framework and UI library
- **Purpose**: Primary application framework for building the interactive web interface

### Data Processing & Analysis
- **Pandas**: Data manipulation and analysis
- **Purpose**: Handling structured data for skill comparisons and analysis history

### Visualization
- **Plotly (Express & Graph Objects)**: Interactive plotting library
- **Purpose**: Creating skill gap visualizations, career progression charts, and quiz result displays

### Document Processing
- **PyPDF2** / **pdfplumber**: PDF parsing libraries (fallback mechanism)
- **python-docx**: Microsoft Word document processing
- **Purpose**: Extract text content from user-uploaded resumes

### PDF Generation
- **ReportLab**: PDF creation library
- **Purpose**: Generate downloadable analysis reports with formatted results

### Utilities
- **UUID**: Unique identifier generation (Python standard library)
- **Purpose**: Create unique user session identifiers
- **datetime**: Date/time handling (Python standard library)
- **Purpose**: Timestamp analysis history and track learning progress
- **base64, BytesIO**: Binary data handling (Python standard library)
- **Purpose**: Handle file uploads and downloads in Streamlit

### Data Structures
- **JSON**: Data serialization (Python standard library)
- **Purpose**: Potential data export/import functionality