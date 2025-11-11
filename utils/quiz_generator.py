import uuid
import random
from typing import Dict, List, Any

class QuizGenerator:
    def __init__(self):
        self.question_bank = self._initialize_question_bank()
    
    def _initialize_question_bank(self) -> Dict[str, List[Dict]]:
        return {
            'python': [
                {
                    'question': 'What is the output of: print(type([]) is list)?',
                    'options': ['True', 'False', 'None', 'TypeError'],
                    'correct_answer': 0,
                    'explanation': 'The `is` operator checks for object identity. type([]) returns the list class, which is identical to list.'
                },
                {
                    'question': 'Which of the following is used to define a block of code in Python?',
                    'options': ['Brackets', 'Indentation', 'Parentheses', 'Semicolons'],
                    'correct_answer': 1,
                    'explanation': 'Python uses indentation to define code blocks, unlike other languages that use brackets.'
                },
                {
                    'question': 'What does the enumerate() function return?',
                    'options': ['List of values', 'Tuple of (index, value)', 'Dictionary', 'Set'],
                    'correct_answer': 1,
                    'explanation': 'enumerate() returns an iterator of tuples containing indices and values.'
                },
                {
                    'question': 'Which keyword is used to create a function in Python?',
                    'options': ['function', 'def', 'func', 'define'],
                    'correct_answer': 1,
                    'explanation': 'The `def` keyword is used to define functions in Python.'
                },
                {
                    'question': 'What is a list comprehension in Python?',
                    'options': ['A way to read lists', 'A concise way to create lists', 'A list sorting method', 'A debugging tool'],
                    'correct_answer': 1,
                    'explanation': 'List comprehensions provide a concise way to create lists based on existing iterables.'
                },
                {
                    'question': 'What is the correct way to create a dictionary in Python?',
                    'options': ['dict = []', 'dict = {}', 'dict = ()', 'dict = <>'],
                    'correct_answer': 1,
                    'explanation': 'Curly braces {} are used to create dictionaries in Python.'
                },
                {
                    'question': 'Which method is used to add an element to the end of a list?',
                    'options': ['add()', 'append()', 'insert()', 'push()'],
                    'correct_answer': 1,
                    'explanation': 'The append() method adds an element to the end of a list.'
                },
                {
                    'question': 'What is the purpose of the "self" parameter in Python class methods?',
                    'options': ['Optional decoration', 'Refers to the instance', 'Global variable', 'Error handler'],
                    'correct_answer': 1,
                    'explanation': 'self refers to the instance of the class and is used to access instance variables and methods.'
                },
                {
                    'question': 'How do you handle exceptions in Python?',
                    'options': ['if-else', 'try-except', 'catch-throw', 'handle-error'],
                    'correct_answer': 1,
                    'explanation': 'Python uses try-except blocks to handle exceptions.'
                },
                {
                    'question': 'What does the len() function return for a string?',
                    'options': ['Size in bytes', 'Number of characters', 'Number of words', 'Memory address'],
                    'correct_answer': 1,
                    'explanation': 'len() returns the number of characters in a string.'
                }
            ],
            'javascript': [
                {
                    'question': 'What is the correct syntax to declare a variable in JavaScript?',
                    'options': ['var x = 5;', 'variable x = 5;', 'v x = 5;', 'int x = 5;'],
                    'correct_answer': 0,
                    'explanation': 'var, let, or const are used to declare variables in JavaScript. var is one of the valid options.'
                },
                {
                    'question': 'Which operator is used to check both value and type?',
                    'options': ['==', '===', '=', '!='],
                    'correct_answer': 1,
                    'explanation': 'The === operator checks for both value and type equality (strict equality).'
                },
                {
                    'question': 'What is a closure in JavaScript?',
                    'options': ['A loop structure', 'A function with access to parent scope', 'A class method', 'An error type'],
                    'correct_answer': 1,
                    'explanation': 'A closure is a function that has access to variables in its outer (parent) scope, even after the parent function has returned.'
                },
                {
                    'question': 'How do you create an arrow function?',
                    'options': ['function => {}', '() => {}', '-> {}', 'func() => {}'],
                    'correct_answer': 1,
                    'explanation': 'Arrow functions use the syntax () => {} for concise function expressions.'
                },
                {
                    'question': 'What does JSON stand for?',
                    'options': ['JavaScript Object Notation', 'Java Serialized Object Notation', 'JavaScript Oriented Network', 'None of the above'],
                    'correct_answer': 0,
                    'explanation': 'JSON stands for JavaScript Object Notation, a lightweight data interchange format.'
                },
                {
                    'question': 'Which method is used to add elements to the end of an array?',
                    'options': ['add()', 'push()', 'append()', 'insert()'],
                    'correct_answer': 1,
                    'explanation': 'The push() method adds one or more elements to the end of an array.'
                },
                {
                    'question': 'What is the DOM?',
                    'options': ['Data Object Model', 'Document Object Model', 'Dynamic Object Management', 'Database Object Model'],
                    'correct_answer': 1,
                    'explanation': 'DOM stands for Document Object Model, a programming interface for HTML and XML documents.'
                },
                {
                    'question': 'How do you write a comment in JavaScript?',
                    'options': ['# comment', '// comment', '<!-- comment -->', '/* comment'],
                    'correct_answer': 1,
                    'explanation': '// is used for single-line comments in JavaScript. /* */ is used for multi-line comments.'
                },
                {
                    'question': 'What is the purpose of the async keyword?',
                    'options': ['Create synchronous code', 'Define asynchronous functions', 'Import modules', 'Export functions'],
                    'correct_answer': 1,
                    'explanation': 'The async keyword is used to define asynchronous functions that return promises.'
                },
                {
                    'question': 'Which method converts JSON string to JavaScript object?',
                    'options': ['JSON.parse()', 'JSON.stringify()', 'JSON.convert()', 'JSON.toObject()'],
                    'correct_answer': 0,
                    'explanation': 'JSON.parse() converts a JSON string into a JavaScript object.'
                }
            ],
            'machine learning': [
                {
                    'question': 'What is supervised learning?',
                    'options': ['Learning without labels', 'Learning with labeled data', 'Reinforcement learning', 'Unsupervised learning'],
                    'correct_answer': 1,
                    'explanation': 'Supervised learning uses labeled training data where both input and output are known.'
                },
                {
                    'question': 'What is overfitting?',
                    'options': ['Model too simple', 'Model memorizes training data', 'Perfect model', 'Underfitting'],
                    'correct_answer': 1,
                    'explanation': 'Overfitting occurs when a model learns the training data too well, including noise, and performs poorly on new data.'
                },
                {
                    'question': 'Which algorithm is used for classification?',
                    'options': ['Linear Regression', 'Logistic Regression', 'K-means', 'PCA'],
                    'correct_answer': 1,
                    'explanation': 'Logistic Regression is commonly used for binary classification tasks.'
                },
                {
                    'question': 'What is a neural network?',
                    'options': ['Database structure', 'Network of interconnected nodes', 'Cloud service', 'Programming language'],
                    'correct_answer': 1,
                    'explanation': 'A neural network is a computational model inspired by biological neural networks, consisting of interconnected nodes (neurons).'
                },
                {
                    'question': 'What is the purpose of a validation set?',
                    'options': ['Train the model', 'Tune hyperparameters', 'Final testing', 'Data collection'],
                    'correct_answer': 1,
                    'explanation': 'A validation set is used to tune hyperparameters and evaluate model performance during training.'
                },
                {
                    'question': 'What is gradient descent?',
                    'options': ['Data preprocessing', 'Optimization algorithm', 'Classification method', 'Clustering technique'],
                    'correct_answer': 1,
                    'explanation': 'Gradient descent is an optimization algorithm used to minimize the loss function by iteratively adjusting parameters.'
                },
                {
                    'question': 'What is precision in classification?',
                    'options': ['Total correct predictions', 'True positives / (True positives + False positives)', 'True negatives / Total', 'Accuracy measure'],
                    'correct_answer': 1,
                    'explanation': 'Precision measures the proportion of true positive predictions among all positive predictions.'
                },
                {
                    'question': 'What is feature scaling?',
                    'options': ['Adding features', 'Normalizing feature ranges', 'Removing features', 'Feature selection'],
                    'correct_answer': 1,
                    'explanation': 'Feature scaling normalizes the range of features to improve model performance and training speed.'
                },
                {
                    'question': 'What is cross-validation?',
                    'options': ['Single train-test split', 'Multiple train-test splits', 'Data cleaning', 'Feature engineering'],
                    'correct_answer': 1,
                    'explanation': 'Cross-validation uses multiple train-test splits to better evaluate model performance and reduce variance.'
                },
                {
                    'question': 'What is the purpose of dropout in neural networks?',
                    'options': ['Increase speed', 'Prevent overfitting', 'Add layers', 'Reduce data'],
                    'correct_answer': 1,
                    'explanation': 'Dropout randomly disables neurons during training to prevent overfitting and improve generalization.'
                }
            ],
            'data analysis': [
                {
                    'question': 'What is the purpose of exploratory data analysis (EDA)?',
                    'options': ['Clean data', 'Understand data patterns', 'Build models', 'Deploy solutions'],
                    'correct_answer': 1,
                    'explanation': 'EDA is used to analyze and understand data characteristics, patterns, and relationships before modeling.'
                },
                {
                    'question': 'What is a histogram used for?',
                    'options': ['Show relationships', 'Display distribution', 'Compare categories', 'Show trends'],
                    'correct_answer': 1,
                    'explanation': 'A histogram displays the distribution of a continuous variable by grouping values into bins.'
                },
                {
                    'question': 'What is correlation?',
                    'options': ['Causation', 'Statistical relationship', 'Mean value', 'Standard deviation'],
                    'correct_answer': 1,
                    'explanation': 'Correlation measures the statistical relationship between two variables, not causation.'
                },
                {
                    'question': 'What does a p-value indicate?',
                    'options': ['Effect size', 'Statistical significance', 'Mean value', 'Variance'],
                    'correct_answer': 1,
                    'explanation': 'A p-value indicates the probability of obtaining results at least as extreme as observed, assuming the null hypothesis is true.'
                },
                {
                    'question': 'What is data normalization?',
                    'options': ['Removing duplicates', 'Scaling data to standard range', 'Sorting data', 'Filtering outliers'],
                    'correct_answer': 1,
                    'explanation': 'Data normalization scales features to a standard range, typically 0 to 1 or -1 to 1.'
                },
                {
                    'question': 'What is an outlier?',
                    'options': ['Missing value', 'Value far from others', 'Average value', 'Mode'],
                    'correct_answer': 1,
                    'explanation': 'An outlier is a data point that differs significantly from other observations in the dataset.'
                },
                {
                    'question': 'What does SQL stand for?',
                    'options': ['Structured Query Language', 'Simple Question Language', 'System Query Logic', 'Standard Quality Language'],
                    'correct_answer': 0,
                    'explanation': 'SQL stands for Structured Query Language, used for managing and querying databases.'
                },
                {
                    'question': 'What is the median?',
                    'options': ['Average value', 'Middle value', 'Most frequent value', 'Range'],
                    'correct_answer': 1,
                    'explanation': 'The median is the middle value when data is sorted, less sensitive to outliers than the mean.'
                },
                {
                    'question': 'What is a pivot table?',
                    'options': ['Database table', 'Data summarization tool', 'Chart type', 'Query language'],
                    'correct_answer': 1,
                    'explanation': 'A pivot table is a data summarization tool that groups and aggregates data for analysis.'
                },
                {
                    'question': 'What is the purpose of data visualization?',
                    'options': ['Store data', 'Communicate insights', 'Clean data', 'Collect data'],
                    'correct_answer': 1,
                    'explanation': 'Data visualization communicates insights and patterns through visual representations like charts and graphs.'
                }
            ],
            'default': [
                {
                    'question': 'What are the core principles of this skill?',
                    'options': ['Theory only', 'Practical application and theory', 'Memorization', 'Trial and error'],
                    'correct_answer': 1,
                    'explanation': 'Most professional skills require both theoretical understanding and practical application.'
                },
                {
                    'question': 'How do you stay updated with this skill?',
                    'options': ['Never update', 'Continuous learning and practice', 'One-time training', 'Avoid changes'],
                    'correct_answer': 1,
                    'explanation': 'Professional skills require continuous learning to stay current with industry developments.'
                },
                {
                    'question': 'What is best practice for applying this skill?',
                    'options': ['Follow standards', 'Random approach', 'Copy others', 'Guess'],
                    'correct_answer': 0,
                    'explanation': 'Following industry standards and best practices ensures quality and consistency.'
                },
                {
                    'question': 'How important is documentation for this skill?',
                    'options': ['Not important', 'Very important', 'Sometimes useful', 'Waste of time'],
                    'correct_answer': 1,
                    'explanation': 'Documentation is crucial for knowledge transfer, maintenance, and collaboration.'
                },
                {
                    'question': 'What role does problem-solving play in this skill?',
                    'options': ['No role', 'Critical role', 'Minor role', 'Optional'],
                    'correct_answer': 1,
                    'explanation': 'Problem-solving is a critical component of most professional skills.'
                },
                {
                    'question': 'How do you measure proficiency in this skill?',
                    'options': ['Years of experience only', 'Projects completed and quality', 'Certificates only', 'Self-assessment'],
                    'correct_answer': 1,
                    'explanation': 'Proficiency is best measured by the quality and complexity of completed projects.'
                },
                {
                    'question': 'What is the importance of collaboration in this skill?',
                    'options': ['Work alone', 'Essential for success', 'Rarely needed', 'Avoid teamwork'],
                    'correct_answer': 1,
                    'explanation': 'Collaboration is essential in most professional environments for project success.'
                },
                {
                    'question': 'How should you approach learning this skill?',
                    'options': ['Rush through basics', 'Build strong foundation first', 'Skip fundamentals', 'Learn randomly'],
                    'correct_answer': 1,
                    'explanation': 'Building a strong foundation in fundamentals is crucial for long-term skill development.'
                },
                {
                    'question': 'What is the role of feedback in skill development?',
                    'options': ['Ignore feedback', 'Use feedback to improve', 'Feedback is criticism', 'Avoid reviews'],
                    'correct_answer': 1,
                    'explanation': 'Constructive feedback is essential for identifying areas of improvement and growth.'
                },
                {
                    'question': 'How do you demonstrate expertise in this skill?',
                    'options': ['Talk about it', 'Deliver results and solve problems', 'Collect certificates', 'Attend events'],
                    'correct_answer': 1,
                    'explanation': 'True expertise is demonstrated through consistent delivery of results and problem-solving ability.'
                }
            ]
        }
    
    def generate_quiz(self, skill: str, num_questions: int = 7) -> Dict[str, Any]:
        skill_lower = skill.lower()
        questions = self.question_bank.get(skill_lower, self.question_bank['default'])
        
        selected_questions = random.sample(questions, min(num_questions, len(questions)))
        
        quiz = {
            'quiz_id': str(uuid.uuid4()),
            'skill': skill,
            'total_questions': len(selected_questions),
            'questions': selected_questions,
            'created_at': None
        }
        
        return quiz
    
    def evaluate_quiz(self, quiz: Dict[str, Any], user_answers: List[int]) -> Dict[str, Any]:
        correct_count = 0
        detailed_results = []
        
        for i, (question, user_answer) in enumerate(zip(quiz['questions'], user_answers)):
            is_correct = user_answer == question['correct_answer']
            if is_correct:
                correct_count += 1
            
            detailed_results.append({
                'question_num': i + 1,
                'question': question['question'],
                'user_answer': question['options'][user_answer],
                'correct_answer': question['options'][question['correct_answer']],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
        
        score_percentage = (correct_count / quiz['total_questions']) * 100
        
        if score_percentage >= 90:
            proficiency = 'Expert'
        elif score_percentage >= 75:
            proficiency = 'Advanced'
        elif score_percentage >= 60:
            proficiency = 'Intermediate'
        elif score_percentage >= 40:
            proficiency = 'Beginner'
        else:
            proficiency = 'Novice'
        
        return {
            'quiz_id': quiz['quiz_id'],
            'skill': quiz['skill'],
            'total_questions': quiz['total_questions'],
            'correct_answers': correct_count,
            'score_percentage': score_percentage,
            'proficiency_level': proficiency,
            'detailed_results': detailed_results
        }
    
    def calculate_true_skill_match(self, resume_score: float, completed_quizzes: List[Dict]) -> Dict[str, Any]:
        if not completed_quizzes:
            return {
                'true_skill_match': resume_score,
                'resume_score': resume_score,
                'quiz_average': 0,
                'resume_weight': 1.0,
                'quiz_weight': 0.0
            }
        
        quiz_average = sum(q['score_percentage'] for q in completed_quizzes) / len(completed_quizzes)
        
        resume_weight = 0.4
        quiz_weight = 0.6
        
        true_skill_match = (resume_score * resume_weight) + (quiz_average * quiz_weight)
        
        return {
            'true_skill_match': true_skill_match,
            'resume_score': resume_score,
            'quiz_average': quiz_average,
            'resume_weight': resume_weight,
            'quiz_weight': quiz_weight,
            'quizzes_taken': len(completed_quizzes)
        }
