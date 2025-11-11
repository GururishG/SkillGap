from typing import List, Dict, Any
import random

class CareerAdvisor:
    def __init__(self):
        self.advice_templates = {
            'high_match': [
                "You're in an excellent position! Consider applying to senior roles or specialized positions.",
                "With your skill set, you could mentor others or lead technical initiatives.",
                "Look for opportunities that challenge you and expand your expertise in emerging technologies."
            ],
            'medium_match': [
                "Focus on practical projects to strengthen your existing skills.",
                "Consider contributing to open-source projects to gain real-world experience.",
                "Network with professionals in your target role to learn about industry expectations."
            ],
            'low_match': [
                "Create a structured learning plan focusing on the most critical missing skills.",
                "Start with foundational skills before moving to advanced topics.",
                "Consider bootcamps, online courses, or mentorship programs to accelerate your learning."
            ]
        }
    
    def get_career_advice(self, user_skills: List[str], target_role: str, match_score: float) -> Dict[str, Any]:
        if match_score >= 75:
            category = 'high_match'
            readiness = "Ready to apply"
        elif match_score >= 50:
            category = 'medium_match'
            readiness = "Almost ready - focus on key gaps"
        else:
            category = 'low_match'
            readiness = "Significant development needed"
        
        advice = random.sample(self.advice_templates[category], min(2, len(self.advice_templates[category])))
        
        return {
            'readiness_level': readiness,
            'advice': advice,
            'recommended_actions': self._get_recommended_actions(match_score),
            'timeline': self._estimate_timeline(match_score)
        }
    
    def _get_recommended_actions(self, match_score: float) -> List[str]:
        if match_score >= 75:
            return [
                "Update your resume highlighting your verified skills",
                "Start applying to positions",
                "Prepare for technical interviews",
                "Build a portfolio showcasing your projects"
            ]
        elif match_score >= 50:
            return [
                "Complete 2-3 significant projects using missing skills",
                "Take online courses for skill gaps",
                "Contribute to open-source projects",
                "Network with industry professionals"
            ]
        else:
            return [
                "Enroll in comprehensive training program",
                "Build foundational projects",
                "Study computer science fundamentals",
                "Join coding communities and forums"
            ]
    
    def _estimate_timeline(self, match_score: float) -> str:
        if match_score >= 75:
            return "Ready now - start applying immediately"
        elif match_score >= 50:
            return "3-6 months of focused learning"
        else:
            return "6-12 months of intensive study and practice"
