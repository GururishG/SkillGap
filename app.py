import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import base64
from io import BytesIO
import uuid

from utils.skill_extractor import extract_skills_from_pdf, extract_skills_from_docx, extract_skills_from_text
from utils.skill_analyzer import SkillAnalyzer
from utils.career_advisor import CareerAdvisor
from utils.pdf_generator import generate_results_pdf
from utils.quiz_generator import QuizGenerator
from data.skills_database import SKILLS_DATABASE, JOB_ROLES, COUNTRIES
from data.career_templates import CAREER_TEMPLATES, LEARNING_PATHS

st.set_page_config(
    page_title="SkillGap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session_state():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'user_skills' not in st.session_state:
        st.session_state.user_skills = []
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = "United States"
    if 'learning_paths' not in st.session_state:
        st.session_state.learning_paths = []
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': '',
            'experience_level': 'Mid-level',
            'target_role': '',
            'skills': []
        }
    if 'active_quizzes' not in st.session_state:
        st.session_state.active_quizzes = {}
    if 'completed_quizzes' not in st.session_state:
        st.session_state.completed_quizzes = []
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = []
    if 'redirect_to_quiz' not in st.session_state:
        st.session_state.redirect_to_quiz = False
    if 'true_skill_match' not in st.session_state:
        st.session_state.true_skill_match = None

@st.cache_resource
def get_components():
    try:
        skill_analyzer = SkillAnalyzer()
        career_advisor = CareerAdvisor()
        quiz_generator = QuizGenerator()
        return skill_analyzer, career_advisor, quiz_generator
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        st.stop()

def main():
    init_session_state()
    skill_analyzer, career_advisor, quiz_generator = get_components()
    
    st.title("🎯 SkillGap Analyzer")
    st.markdown("*Analyze your skills, discover gaps, and accelerate your career growth*")
    
    with st.sidebar:
        st.title("🧭 Navigation")
        
        st.subheader("🌍 Target Country")
        selected_country = st.selectbox(
            "Select target country:",
            COUNTRIES,
            index=COUNTRIES.index(st.session_state.selected_country) if st.session_state.selected_country in COUNTRIES else 0
        )
        if selected_country != st.session_state.selected_country:
            st.session_state.selected_country = selected_country
            st.rerun()
        
        page = st.selectbox(
            "Choose a section:",
            [
                "🔍 Analyze Skills", 
                "🧠 Skill Test Session",
                "📊 Results Dashboard", 
                "🎓 Learning Paths",
                "🤖 Career Advisor", 
                "📊 Market Trends",
                "👤 My Profile",
                "📁 Analysis History"
            ]
        )
        
        if st.session_state.analysis_results:
            st.markdown("### 📋 Quick Stats")
            results = st.session_state.analysis_results
            st.metric("Skills Analyzed", len(st.session_state.user_skills))
            
            if st.session_state.true_skill_match:
                st.metric("True Skill Match", f"{st.session_state.true_skill_match['true_skill_match']:.1f}%")
            else:
                st.metric("Resume Match", f"{results.get('overall_match_score', 0):.1f}%")
            
            st.metric("Missing Skills", len(results.get('missing_skills', [])))
            
            if st.session_state.completed_quizzes:
                st.metric("Quizzes Completed", len(st.session_state.completed_quizzes))
            
            st.markdown(f"**📍 Target Market:** {st.session_state.selected_country}")
    
    if st.session_state.redirect_to_quiz:
        st.session_state.redirect_to_quiz = False
        page = "🧠 Skill Test Session"
    
    if page == "🔍 Analyze Skills":
        analyze_skills_page(skill_analyzer, quiz_generator)
    elif page == "🧠 Skill Test Session":
        skill_test_session_page(quiz_generator)
    elif page == "📊 Results Dashboard":
        results_dashboard_page()
    elif page == "🎓 Learning Paths":
        learning_paths_page()
    elif page == "🤖 Career Advisor":
        career_advisor_page(career_advisor)
    elif page == "📊 Market Trends":
        market_trends_page()
    elif page == "👤 My Profile":
        user_profile_page()
    elif page == "📁 Analysis History":
        analysis_history_page()

def analyze_skills_page(skill_analyzer, quiz_generator):
    st.header("🔍 Skill Analysis")
    
    input_method = st.radio(
        "Choose your input method:",
        ["📄 Upload Resume", "✍️ Manual Input"],
        horizontal=True
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if input_method == "📄 Upload Resume":
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF or DOCX)",
                type=['pdf', 'docx'],
                help="Upload your resume to automatically extract skills"
            )
            
            if uploaded_file is not None:
                with st.spinner("🔍 Extracting skills from your resume..."):
                    try:
                        skills = []
                        if uploaded_file.type == "application/pdf":
                            skills = extract_skills_from_pdf(uploaded_file)
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            skills = extract_skills_from_docx(uploaded_file)
                        
                        if skills:
                            st.session_state.user_skills = skills
                            st.success(f"✅ Extracted {len(skills)} skills from your resume!")
                            
                            st.subheader("📋 Extracted Skills:")
                            st.markdown(" • ".join(skills))
                        else:
                            st.warning("⚠️ No skills were extracted from the file. Please try manual input instead.")
                    
                    except Exception as e:
                        st.error(f"❌ Error processing file: {str(e)}")
                        st.session_state.user_skills = []
        
        else:
            st.subheader("✍️ Enter Your Skills")
            skills_input = st.text_area(
                "List your skills (one per line or comma-separated):",
                height=150,
                placeholder="Python\nJavaScript\nMachine Learning\nData Analysis\nProject Management"
            )
            
            if st.button("📝 Process Skills", type="primary") and skills_input:
                try:
                    skills = extract_skills_from_text(skills_input)
                    if skills:
                        st.session_state.user_skills = skills
                        st.success(f"✅ Processed {len(skills)} skills!")
                        
                        st.subheader("📋 Your Skills:")
                        st.markdown(" • ".join(skills))
                    else:
                        st.warning("⚠️ No valid skills were found. Please check your input.")
                except Exception as e:
                    st.error(f"❌ Error processing skills: {str(e)}")
    
    with col2:
        if st.session_state.user_skills:
            st.subheader("🎯 Select Target Role")
            target_role = st.selectbox(
                "Choose your target role:",
                list(JOB_ROLES.keys())
            )
            
            if st.button("🔍 Analyze Skills Gap", type="primary"):
                with st.spinner("🔍 Analyzing your skills..."):
                    try:
                        results = skill_analyzer.analyze_skills(
                            st.session_state.user_skills,
                            target_role,
                            st.session_state.selected_country
                        )
                        st.session_state.analysis_results = results
                        
                        st.session_state.analysis_history.append({
                            'timestamp': datetime.now(),
                            'target_role': target_role,
                            'results': results,
                            'skills_count': len(st.session_state.user_skills)
                        })
                        
                        matching_skills = results.get('matching_skills', [])
                        if matching_skills:
                            st.session_state.active_quizzes = {}
                            for skill in matching_skills[:5]:
                                quiz = quiz_generator.generate_quiz(skill, num_questions=7)
                                st.session_state.active_quizzes[skill] = quiz
                        
                        st.success("✅ Analysis complete! Redirecting to Skill Test Session...")
                        st.balloons()
                        
                        st.session_state.redirect_to_quiz = True
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")

def skill_test_session_page(quiz_generator):
    st.header("🧠 Skill Test Session")
    
    if not st.session_state.active_quizzes and not st.session_state.completed_quizzes:
        st.info("📝 No quizzes available. Please analyze your skills first to generate skill verification quizzes.")
        return
    
    if st.session_state.active_quizzes:
        st.markdown("### 🎯 Verify Your Skills")
        st.markdown("Take these quizzes to validate your skill level and get your True Skill Match score!")
        
        tabs = st.tabs(list(st.session_state.active_quizzes.keys()))
        
        for idx, (skill, quiz) in enumerate(st.session_state.active_quizzes.items()):
            with tabs[idx]:
                st.subheader(f"📚 {skill} Quiz")
                st.markdown(f"**Questions:** {quiz['total_questions']} | **Status:** In Progress")
                
                st.markdown("---")
                
                user_answers = []
                
                for i, question in enumerate(quiz['questions']):
                    st.markdown(f"### Question {i+1}/{quiz['total_questions']}")
                    st.markdown(f"**{question['question']}**")
                    
                    answer = st.radio(
                        "Select your answer:",
                        question['options'],
                        key=f"{quiz['quiz_id']}_q{i}",
                        index=None
                    )
                    
                    if answer:
                        user_answers.append(question['options'].index(answer))
                    else:
                        user_answers.append(-1)
                    
                    st.markdown("---")
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button(f"✅ Submit {skill} Quiz", type="primary", key=f"submit_{skill}", use_container_width=True):
                        if -1 in user_answers:
                            st.error("⚠️ Please answer all questions before submitting!")
                        else:
                            result = quiz_generator.evaluate_quiz(quiz, user_answers)
                            st.session_state.completed_quizzes.append(result)
                            del st.session_state.active_quizzes[skill]
                            
                            if st.session_state.analysis_results:
                                resume_score = st.session_state.analysis_results.get('overall_match_score', 0)
                                true_match = quiz_generator.calculate_true_skill_match(
                                    resume_score, 
                                    st.session_state.completed_quizzes
                                )
                                st.session_state.true_skill_match = true_match
                            
                            st.success(f"🎉 Quiz completed! Score: {result['score_percentage']:.1f}% | Proficiency: {result['proficiency_level']}")
                            st.rerun()
    
    if st.session_state.completed_quizzes:
        st.markdown("---")
        st.markdown("### 📊 Quiz Results")
        
        for result in st.session_state.completed_quizzes:
            with st.expander(f"✅ {result['skill']} - Score: {result['score_percentage']:.1f}% ({result['proficiency_level']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{result['score_percentage']:.1f}%")
                with col2:
                    st.metric("Correct Answers", f"{result['correct_answers']}/{result['total_questions']}")
                with col3:
                    st.metric("Proficiency", result['proficiency_level'])
                
                st.markdown("#### 📝 Detailed Results")
                for detail in result['detailed_results']:
                    icon = "✅" if detail['is_correct'] else "❌"
                    color = "green" if detail['is_correct'] else "red"
                    
                    st.markdown(f"**{icon} Question {detail['question_num']}:** {detail['question']}")
                    st.markdown(f"**Your Answer:** :{color}[{detail['user_answer']}]")
                    
                    if not detail['is_correct']:
                        st.markdown(f"**Correct Answer:** :green[{detail['correct_answer']}]")
                    
                    st.markdown(f"*💡 {detail['explanation']}*")
                    st.markdown("---")

def results_dashboard_page():
    if not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results available. Please analyze your skills first.")
        return
    
    results = st.session_state.analysis_results
    
    st.header("📊 Skills Analysis Results")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.session_state.true_skill_match:
            st.metric(
                "True Skill Match ⭐", 
                f"{st.session_state.true_skill_match['true_skill_match']:.1f}%",
                help="Combined score from resume match and quiz performance"
            )
        else:
            st.metric("Resume Match", f"{results.get('overall_match_score', 0):.1f}%")
    
    with col2:
        st.metric("Matching Skills", len(results.get('matching_skills', [])))
    
    with col3:
        st.metric("Missing Skills", len(results.get('missing_skills', [])))
    
    with col4:
        if st.session_state.completed_quizzes:
            avg_quiz_score = sum(q['score_percentage'] for q in st.session_state.completed_quizzes) / len(st.session_state.completed_quizzes)
            st.metric("Avg Quiz Score", f"{avg_quiz_score:.1f}%")
        else:
            st.metric("Quizzes Taken", "0")
    
    if st.session_state.true_skill_match:
        st.markdown("---")
        st.subheader("🎯 True Skill Match Breakdown")
        
        true_match_data = st.session_state.true_skill_match
        
        col1, col2 = st.columns(2)
        with col1:
            breakdown_df = pd.DataFrame({
                'Component': ['Resume Match', 'Quiz Performance'],
                'Score': [true_match_data['resume_score'], true_match_data['quiz_average']],
                'Weight': [true_match_data['resume_weight'], true_match_data['quiz_weight']]
            })
            
            fig_breakdown = px.bar(
                breakdown_df, 
                x='Component', 
                y='Score',
                title="Score Components",
                color='Component',
                text='Score'
            )
            fig_breakdown.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig_breakdown, use_container_width=True)
        
        with col2:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=true_match_data['true_skill_match'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "True Skill Match"},
                delta={'reference': true_match_data['resume_score']},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 70], 'color': "lightyellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🎯 Skills Breakdown")
    col1, col2 = st.columns(2)
    
    with col1:
        if results.get('matching_skills'):
            matching_df = pd.DataFrame({
                'Skill': results['matching_skills'],
                'Status': ['Verified' if any(q['skill'] == skill for q in st.session_state.completed_quizzes) else 'Claimed' for skill in results['matching_skills']]
            })
            fig1 = px.bar(
                matching_df, 
                x='Skill', 
                y=[1]*len(matching_df),
                title="✅ Skills You Have", 
                color='Status',
                color_discrete_map={'Verified': '#2E8B57', 'Claimed': '#87CEEB'}
            )
            fig1.update_xaxes(tickangle=45)
            fig1.update_yaxes(showticklabels=False, title="")
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        if results.get('missing_skills'):
            missing_df = pd.DataFrame({
                'Skill': results['missing_skills'],
                'Priority': ['High'] * len(results['missing_skills'])
            })
            fig2 = px.bar(
                missing_df, 
                x='Skill', 
                y=[1]*len(missing_df),
                title="❌ Skills You Need", 
                color_discrete_sequence=['#DC143C']
            )
            fig2.update_xaxes(tickangle=45)
            fig2.update_yaxes(showticklabels=False, title="")
            st.plotly_chart(fig2, use_container_width=True)
    
    if st.session_state.completed_quizzes:
        st.markdown("---")
        st.subheader("📈 Quiz Performance")
        
        quiz_df = pd.DataFrame([
            {
                'Skill': q['skill'],
                'Score': q['score_percentage'],
                'Proficiency': q['proficiency_level']
            }
            for q in st.session_state.completed_quizzes
        ])
        
        fig_quiz = px.bar(
            quiz_df,
            x='Skill',
            y='Score',
            title="Quiz Scores by Skill",
            color='Proficiency',
            text='Score'
        )
        fig_quiz.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_quiz, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💡 Recommendations")
    if results.get('recommendations'):
        for i, rec in enumerate(results['recommendations'], 1):
            st.markdown(f"**{i}.** {rec}")
    
    if st.button("📄 Generate PDF Report"):
        try:
            pdf_buffer = generate_results_pdf(results, st.session_state.user_skills)
            st.download_button(
                label="📥 Download Report",
                data=pdf_buffer.getvalue(),
                file_name=f"skill_analysis_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

def learning_paths_page():
    st.header("🎓 Learning Paths")
    
    if not st.session_state.analysis_results:
        st.warning("⚠️ Please analyze your skills first to get personalized learning paths.")
        return
    
    results = st.session_state.analysis_results
    missing_skills = results.get('missing_skills', [])
    
    if not missing_skills:
        st.success("🎉 Congratulations! You have all the required skills for your target role.")
        return
    
    st.markdown("Based on your skill gap analysis, here are recommended learning paths:")
    
    for skill in missing_skills[:5]:
        if skill.lower() in LEARNING_PATHS:
            path = LEARNING_PATHS[skill.lower()]
            
            with st.expander(f"📚 Learn {skill}"):
                st.markdown(f"**Difficulty:** {path['difficulty']}")
                st.markdown(f"**Estimated Time:** {path['duration']}")
                st.markdown(f"**Description:** {path['description']}")
                
                st.markdown("**Learning Steps:**")
                for i, step in enumerate(path['steps'], 1):
                    st.markdown(f"{i}. {step}")
                
                st.markdown("**Recommended Resources:**")
                for resource in path['resources']:
                    st.markdown(f"• {resource}")
    
    st.subheader("📈 Learning Progress")
    
    if 'learning_progress' not in st.session_state:
        st.session_state.learning_progress = {}
    
    for skill in missing_skills[:3]:
        progress = st.slider(
            f"Progress in {skill}",
            0, 100, 
            st.session_state.learning_progress.get(skill, 0),
            key=f"progress_{skill}"
        )
        st.session_state.learning_progress[skill] = progress

def career_advisor_page(career_advisor):
    st.header("🤖 Career Advisor")
    
    if st.session_state.user_skills and st.session_state.analysis_results:
        st.subheader("🎯 Personalized Career Advice")
        
        results = st.session_state.analysis_results
        match_score = st.session_state.true_skill_match['true_skill_match'] if st.session_state.true_skill_match else results.get('overall_match_score', 0)
        
        advice_data = career_advisor.get_career_advice(
            st.session_state.user_skills,
            results.get('target_role', ''),
            match_score
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Career Readiness", advice_data['readiness_level'])
        with col2:
            st.metric("Estimated Timeline", advice_data['timeline'])
        
        st.markdown("### 💼 Career Advice")
        for advice in advice_data['advice']:
            st.info(advice)
        
        st.markdown("### 📋 Recommended Actions")
        for i, action in enumerate(advice_data['recommended_actions'], 1):
            st.markdown(f"**{i}.** {action}")
        
        if results.get('salary_range'):
            st.markdown("---")
            st.subheader("💰 Salary Insights")
            salary_range = results['salary_range']
            st.markdown(f"**Expected Salary Range ({st.session_state.selected_country}):**")
            st.markdown(f"${salary_range['min']:,} - ${salary_range['max']:,}")
    else:
        st.info("📝 Please analyze your skills first to get personalized career advice.")

def market_trends_page():
    st.header("📊 Market Trends")
    
    st.markdown("### 🔥 Top In-Demand Skills 2025")
    
    trend_data = {
        'Skill': ['Python', 'Machine Learning', 'Cloud Computing', 'React', 'Data Analysis', 'Docker', 'TypeScript', 'SQL'],
        'Demand Growth (%)': [25, 35, 40, 22, 28, 30, 20, 18],
        'Avg Salary ($k)': [120, 140, 135, 110, 105, 125, 115, 100]
    }
    
    df_trends = pd.DataFrame(trend_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            df_trends,
            x='Skill',
            y='Demand Growth (%)',
            title='Skill Demand Growth',
            color='Demand Growth (%)',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(
            df_trends,
            x='Skill',
            y='Avg Salary ($k)',
            title='Average Salaries by Skill',
            color='Avg Salary ($k)',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("### 📈 Industry Insights")
    st.markdown("""
    - **AI/ML Skills** are seeing the highest demand growth at 35%
    - **Cloud Computing** remains critical with 40% growth in job postings
    - **Full-Stack Development** (React + Node.js) is highly sought after
    - **DevOps** skills command premium salaries averaging $125k
    """)

def user_profile_page():
    st.header("👤 My Profile")
    
    st.subheader("📝 User Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name", st.session_state.user_profile.get('name', ''))
        st.session_state.user_profile['name'] = name
        
        experience = st.selectbox(
            "Experience Level",
            ['Entry-level', 'Mid-level', 'Senior', 'Lead', 'Executive'],
            index=['Entry-level', 'Mid-level', 'Senior', 'Lead', 'Executive'].index(
                st.session_state.user_profile.get('experience_level', 'Mid-level')
            )
        )
        st.session_state.user_profile['experience_level'] = experience
    
    with col2:
        if st.session_state.analysis_results:
            st.info(f"**Current Target Role:** {st.session_state.analysis_results.get('target_role', 'Not set')}")
            st.info(f"**Skills Count:** {len(st.session_state.user_skills)}")
        else:
            st.info("No analysis completed yet")
    
    if st.session_state.user_skills:
        st.subheader("🎯 Your Skills")
        st.markdown(" • ".join(st.session_state.user_skills))
    
    st.subheader("📊 Profile Summary")
    st.markdown(f"**User ID:** `{st.session_state.user_id}`")
    st.markdown(f"**Analyses Performed:** {len(st.session_state.analysis_history)}")
    st.markdown(f"**Quizzes Completed:** {len(st.session_state.completed_quizzes)}")

def analysis_history_page():
    st.header("📁 Analysis History")
    
    if not st.session_state.analysis_history:
        st.info("📝 No analysis history yet. Start by analyzing your skills!")
        return
    
    st.markdown(f"**Total Analyses:** {len(st.session_state.analysis_history)}")
    
    for i, entry in enumerate(reversed(st.session_state.analysis_history), 1):
        with st.expander(f"Analysis #{len(st.session_state.analysis_history) - i + 1} - {entry['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
            st.markdown(f"**Target Role:** {entry['target_role']}")
            st.markdown(f"**Skills Analyzed:** {entry['skills_count']}")
            st.markdown(f"**Match Score:** {entry['results'].get('overall_match_score', 0):.1f}%")
            
            col1, col2 = st.columns(2)
            with col1:
                if entry['results'].get('matching_skills'):
                    st.markdown("**Matching Skills:**")
                    st.markdown(", ".join(entry['results']['matching_skills']))
            
            with col2:
                if entry['results'].get('missing_skills'):
                    st.markdown("**Missing Skills:**")
                    st.markdown(", ".join(entry['results']['missing_skills'][:5]))

if __name__ == "__main__":
    main()
