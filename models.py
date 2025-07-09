from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    progress = db.relationship('Progress', backref='user', uselist=False, cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='user', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='user', cascade='all, delete-orphan')
    learning_sessions = db.relationship('LearningSession', backref='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_or_create_progress(self):
        if not self.progress:
            self.progress = Progress(user_id=self.id)
            db.session.add(self.progress)
            db.session.commit()
        return self.progress
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    total_modules = db.Column(db.Integer, default=12)
    modules_completed = db.Column(db.Integer, default=0)
    lessons_completed = db.Column(db.Integer, default=0)
    quizzes_taken = db.Column(db.Integer, default=0)
    circuits_built = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)
    streak_days = db.Column(db.Integer, default=0)
    study_time_minutes = db.Column(db.Integer, default=0)
    last_active_date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def add_xp(self, amount):
        old_level = self.level
        self.xp += amount
        new_level = self.calculate_level()
        
        if new_level > old_level:
            self.level = new_level
            return True  # Level up occurred
        return False
    
    def calculate_level(self):
        # Simple level calculation: 1000 XP per level
        return max(1, (self.xp // 1000) + 1)
    
    def get_xp_for_next_level(self):
        return self.level * 1000
    
    def get_progress_percentage(self):
        if self.total_modules == 0:
            return 0
        return min(100, (self.modules_completed / self.total_modules) * 100)
    
    def update_streak(self):
        today = datetime.utcnow().date()
        if self.last_active_date:
            days_diff = (today - self.last_active_date).days
            if days_diff == 1:
                # Consecutive day
                self.streak_days += 1
            elif days_diff > 1:
                # Streak broken
                self.streak_days = 1
            # If days_diff == 0, same day, no change
        else:
            # First time
            self.streak_days = 1
        
        self.last_active_date = today
    
    def to_dict(self):
        return {
            'level': self.level,
            'xp': self.xp,
            'total_modules': self.total_modules,
            'modules_completed': self.modules_completed,
            'lessons_completed': self.lessons_completed,
            'quizzes_taken': self.quizzes_taken,
            'circuits_built': self.circuits_built,
            'average_score': round(self.average_score, 1),
            'streak_days': self.streak_days,
            'study_time_minutes': self.study_time_minutes,
            'progress_percentage': round(self.get_progress_percentage(), 1),
            'xp_for_next_level': self.get_xp_for_next_level(),
            'last_active': self.last_active_date.isoformat() if self.last_active_date else None,
            'updated_at': self.updated_at.isoformat()
        }

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.achievement_id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'unlocked_at': self.unlocked_at.isoformat()
        }

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.String(50), nullable=False)
    quiz_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)  # in seconds
    answers = db.Column(db.Text)  # JSON string of user answers
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_answers(self, answers_list):
        self.answers = json.dumps(answers_list)
    
    def get_answers(self):
        return json.loads(self.answers) if self.answers else []
    
    def get_percentage(self):
        if self.total_questions == 0:
            return 0
        return (self.correct_answers / self.total_questions) * 100
    
    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'quiz_name': self.quiz_name,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'percentage': round(self.get_percentage(), 1),
            'time_taken': self.time_taken,
            'completed_at': self.completed_at.isoformat()
        }

class LearningSession(db.Model):
    __tablename__ = 'learning_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.String(50), nullable=False)
    module_name = db.Column(db.String(100), nullable=False)
    lesson_id = db.Column(db.String(50))
    lesson_name = db.Column(db.String(100))
    session_type = db.Column(db.String(20), nullable=False)  # 'lesson', 'quiz', 'circuit', 'practice'
    duration_minutes = db.Column(db.Integer, default=0)
    xp_earned = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def complete_session(self, xp_earned=0):
        self.completed = True
        self.completed_at = datetime.utcnow()
        self.xp_earned = xp_earned
        
        # Calculate duration
        if self.started_at:
            duration = (self.completed_at - self.started_at).total_seconds() / 60
            self.duration_minutes = max(1, int(duration))
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'module_name': self.module_name,
            'lesson_id': self.lesson_id,
            'lesson_name': self.lesson_name,
            'session_type': self.session_type,
            'duration_minutes': self.duration_minutes,
            'xp_earned': self.xp_earned,
            'completed': self.completed,
            'started_at': self.started_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class CircuitDesign(db.Model):
    __tablename__ = 'circuit_designs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    design_data = db.Column(db.Text, nullable=False)  # JSON string of circuit components
    is_public = db.Column(db.Boolean, default=False)
    simulation_results = db.Column(db.Text)  # JSON string of simulation data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='circuit_designs')
    
    def set_design_data(self, data):
        self.design_data = json.dumps(data)
    
    def get_design_data(self):
        return json.loads(self.design_data) if self.design_data else {}
    
    def set_simulation_results(self, results):
        self.simulation_results = json.dumps(results)
    
    def get_simulation_results(self):
        return json.loads(self.simulation_results) if self.simulation_results else {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'design_data': self.get_design_data(),
            'is_public': self.is_public,
            'simulation_results': self.get_simulation_results(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }