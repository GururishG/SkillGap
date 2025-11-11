from typing import List, Dict, Any
from data.skills_database import JOB_ROLES

class SkillAnalyzer:
    def __init__(self):
        self.job_roles = JOB_ROLES
    
    def analyze_skills(self, user_skills: List[str], target_role: str, country: str = "United States") -> Dict[str, Any]:
        if target_role not in self.job_roles:
            return {
                'error': f"Role '{target_role}' not found in database",
                'overall_match_score': 0,
                'matching_skills': [],
                'missing_skills': [],
                'recommendations': []
            }
        
        role_data = self.job_roles[target_role]
        required_skills = set(role_data['required_skills'])
        preferred_skills = set(role_data.get('preferred_skills', []))
        all_role_skills = required_skills.union(preferred_skills)
        
        user_skills_set = set(user_skills)
        
        matching_skills = list(user_skills_set.intersection(all_role_skills))
        missing_required = list(required_skills - user_skills_set)
        missing_preferred = list(preferred_skills - user_skills_set)
        missing_skills = missing_required + missing_preferred
        
        required_match_count = len(required_skills.intersection(user_skills_set))
        preferred_match_count = len(preferred_skills.intersection(user_skills_set))
        
        required_weight = 0.7
        preferred_weight = 0.3
        
        required_score = (required_match_count / len(required_skills)) * 100 if required_skills else 100
        preferred_score = (preferred_match_count / len(preferred_skills)) * 100 if preferred_skills else 100
        
        overall_match_score = (required_score * required_weight) + (preferred_score * preferred_weight)
        
        recommendations = self._generate_recommendations(
            missing_required,
            missing_preferred,
            target_role,
            overall_match_score
        )
        
        return {
            'target_role': target_role,
            'target_country': country,
            'overall_match_score': overall_match_score,
            'required_skills_score': required_score,
            'preferred_skills_score': preferred_score,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'missing_required_skills': missing_required,
            'missing_preferred_skills': missing_preferred,
            'total_skills_needed': len(all_role_skills),
            'skills_you_have': len(matching_skills),
            'recommendations': recommendations,
            'salary_range': role_data.get('salary_range', {}),
            'role_description': role_data.get('description', '')
        }
    
    def _generate_recommendations(
        self,
        missing_required: List[str],
        missing_preferred: List[str],
        target_role: str,
        match_score: float
    ) -> List[str]:
        recommendations = []
        
        if match_score >= 80:
            recommendations.append(f"🎉 Excellent match! You're well-qualified for {target_role} positions.")
            if missing_preferred:
                recommendations.append(f"Consider learning {', '.join(missing_preferred[:3])} to stand out even more.")
        elif match_score >= 60:
            recommendations.append(f"✅ Good foundation for {target_role}. Focus on filling critical skill gaps.")
            if missing_required:
                recommendations.append(f"Priority: Learn {', '.join(missing_required[:3])} (required skills).")
        else:
            recommendations.append(f"📚 Significant skill development needed for {target_role}.")
            if missing_required:
                recommendations.append(f"Start with these essential skills: {', '.join(missing_required[:5])}.")
        
        if len(missing_required) == 0 and len(missing_preferred) > 0:
            recommendations.append("💪 You have all required skills! Learning preferred skills will make you more competitive.")
        
        recommendations.append("🎯 Take skill verification quizzes to validate your expertise and improve your True Skill Match score.")
        
        return recommendations
