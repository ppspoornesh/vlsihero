import os
from flask import Flask, render_template, send_from_directory, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime, timedelta
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory('pages', filename)

@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory('js', filename)

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

# Helper function to get current user (demo implementation)
def get_current_user():
    # For demo purposes, create or get a default user
    from models import User
    user = User.query.filter_by(username='demo_user').first()
    if not user:
        user = User(
            username='demo_user',
            email='demo@vlsihero.com'
        )
        user.set_password('demo123')
        db.session.add(user)
        db.session.commit()
    return user

# API endpoints for progress tracking
@app.route('/api/progress', methods=['GET', 'POST'])
def api_progress():
    from models import Progress, LearningSession
    
    user = get_current_user()
    progress = user.get_or_create_progress()
    
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        if action == 'complete_lesson':
            progress.lessons_completed += 1
            progress.add_xp(50)
            progress.update_streak()
            
            # Create learning session
            session_data = LearningSession(
                user_id=user.id,
                module_id=data.get('module_id', 'unknown'),
                module_name=data.get('module_name', 'Unknown Module'),
                lesson_id=data.get('lesson_id'),
                lesson_name=data.get('lesson_name'),
                session_type='lesson'
            )
            session_data.complete_session(50)
            db.session.add(session_data)
            
        elif action == 'complete_module':
            progress.modules_completed += 1
            progress.add_xp(200)
            progress.update_streak()
            
        elif action == 'build_circuit':
            progress.circuits_built += 1
            progress.add_xp(30)
            progress.update_streak()
            
        elif action == 'update_study_time':
            minutes = data.get('minutes', 0)
            progress.study_time_minutes += minutes
            
        db.session.commit()
        return jsonify({"status": "success", "progress": progress.to_dict()})
    
    else:
        return jsonify(progress.to_dict())

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    from models import QuizAttempt, Progress, Achievement
    
    user = get_current_user()
    progress = user.get_or_create_progress()
    data = request.get_json()
    
    # Create quiz attempt record
    quiz_attempt = QuizAttempt(
        user_id=user.id,
        quiz_id=data.get('quiz_id', 'vlsi_fundamentals'),
        quiz_name=data.get('quiz_name', 'VLSI Fundamentals Quiz'),
        score=data.get('score', 0),
        total_questions=data.get('total_questions', 25),
        correct_answers=data.get('correct_answers', 0),
        time_taken=data.get('time_taken', 0)
    )
    
    if 'answers' in data:
        quiz_attempt.set_answers(data['answers'])
    
    db.session.add(quiz_attempt)
    
    # Update progress
    progress.quizzes_taken += 1
    old_avg = progress.average_score
    total_attempts = progress.quizzes_taken
    progress.average_score = ((old_avg * (total_attempts - 1)) + quiz_attempt.get_percentage()) / total_attempts
    
    # Award XP based on score
    xp_earned = max(10, quiz_attempt.score * 2)
    leveled_up = progress.add_xp(xp_earned)
    progress.update_streak()
    
    # Check for achievements
    achievements_earned = []
    if quiz_attempt.get_percentage() == 100 and not Achievement.query.filter_by(
        user_id=user.id, achievement_id='perfect_score'
    ).first():
        achievement = Achievement(
            user_id=user.id,
            achievement_id='perfect_score',
            name='Perfect Score',
            description='Scored 100% on a quiz',
            icon='fa-star'
        )
        db.session.add(achievement)
        achievements_earned.append(achievement.to_dict())
    
    if data.get('time_taken', 0) < 300 and not Achievement.query.filter_by(
        user_id=user.id, achievement_id='speed_runner'
    ).first():
        achievement = Achievement(
            user_id=user.id,
            achievement_id='speed_runner',
            name='Speed Runner',
            description='Completed quiz in under 5 minutes',
            icon='fa-lightning-bolt'
        )
        db.session.add(achievement)
        achievements_earned.append(achievement.to_dict())
    
    # Create learning session
    learning_session = LearningSession(
        user_id=user.id,
        module_id=data.get('quiz_id', 'vlsi_fundamentals'),
        module_name=data.get('quiz_name', 'VLSI Fundamentals Quiz'),
        session_type='quiz'
    )
    learning_session.complete_session(xp_earned)
    db.session.add(learning_session)
    
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "quiz_attempt": quiz_attempt.to_dict(),
        "progress": progress.to_dict(),
        "leveled_up": leveled_up,
        "achievements_earned": achievements_earned,
        "xp_earned": xp_earned
    })

@app.route('/api/achievements')
def api_achievements():
    from models import Achievement
    
    user = get_current_user()
    achievements = Achievement.query.filter_by(user_id=user.id).all()
    
    return jsonify({
        "achievements": [achievement.to_dict() for achievement in achievements]
    })

@app.route('/api/learning-sessions')
def api_learning_sessions():
    from models import LearningSession
    
    user = get_current_user()
    
    # Get recent sessions (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    sessions = LearningSession.query.filter(
        LearningSession.user_id == user.id,
        LearningSession.started_at >= thirty_days_ago
    ).order_by(LearningSession.started_at.desc()).all()
    
    return jsonify({
        "sessions": [session.to_dict() for session in sessions]
    })

@app.route('/api/circuit-designs', methods=['GET', 'POST'])
def api_circuit_designs():
    from models import CircuitDesign
    
    user = get_current_user()
    
    if request.method == 'POST':
        data = request.get_json()
        
        circuit = CircuitDesign(
            user_id=user.id,
            name=data.get('name', 'Untitled Circuit'),
            description=data.get('description', ''),
            is_public=data.get('is_public', False)
        )
        circuit.set_design_data(data.get('design_data', {}))
        
        if 'simulation_results' in data:
            circuit.set_simulation_results(data['simulation_results'])
        
        db.session.add(circuit)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "circuit": circuit.to_dict()
        })
    
    else:
        circuits = CircuitDesign.query.filter_by(user_id=user.id).order_by(
            CircuitDesign.updated_at.desc()
        ).all()
        
        return jsonify({
            "circuits": [circuit.to_dict() for circuit in circuits]
        })

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    from models import Progress, QuizAttempt, LearningSession, Achievement
    
    user = get_current_user()
    progress = user.get_or_create_progress()
    
    # Get quiz stats
    quiz_attempts = QuizAttempt.query.filter_by(user_id=user.id).all()
    best_score = max([attempt.get_percentage() for attempt in quiz_attempts]) if quiz_attempts else 0
    
    # Get recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_sessions = LearningSession.query.filter(
        LearningSession.user_id == user.id,
        LearningSession.started_at >= week_ago
    ).all()
    
    # Calculate daily activity for chart
    daily_activity = {}
    for i in range(7):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        daily_activity[date.isoformat()] = 0
    
    for session in recent_sessions:
        date_key = session.started_at.date().isoformat()
        if date_key in daily_activity:
            daily_activity[date_key] += session.xp_earned
    
    # Get achievements count
    achievements_count = Achievement.query.filter_by(user_id=user.id).count()
    
    return jsonify({
        "progress": progress.to_dict(),
        "quiz_stats": {
            "total_attempts": len(quiz_attempts),
            "average_score": progress.average_score,
            "best_score": best_score
        },
        "activity_chart": daily_activity,
        "achievements_count": achievements_count,
        "total_study_time": progress.study_time_minutes
    })

if __name__ == '__main__':
    with app.app_context():
        # Import models to ensure they're registered
        import models
        db.create_all()
        print("Database tables created successfully!")
    app.run(host='0.0.0.0', port=5000, debug=True)