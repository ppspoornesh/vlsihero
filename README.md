# VLSI Hero - Interactive Digital Design Learning Platform

A gamified educational platform for learning VLSI (Very Large Scale Integration) and digital design concepts through interactive modules, quizzes, circuit simulations, and progress tracking.

## Features

- **Interactive Learning Modules**: Comprehensive lessons on VLSI fundamentals, digital design, and circuit simulation
- **Gamified Progress System**: XP points, levels, achievements, and learning streaks
- **Circuit Simulator**: Canvas-based circuit drawing and simulation environment
- **Quiz System**: Timed quizzes with detailed analytics and explanations
- **Progress Tracking**: Real-time analytics with charts and performance metrics
- **Database Integration**: PostgreSQL backend for persistent user data
- **Responsive Design**: Mobile-friendly interface with dark theme

## Technology Stack

### Backend
- **Flask**: Web framework with SQLAlchemy ORM
- **PostgreSQL**: Database for user management and progress tracking
- **Python 3.11**: Backend language with comprehensive data models

### Frontend
- **HTML5/CSS3/JavaScript**: Vanilla web technologies
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive data visualization
- **Canvas API**: Circuit simulation and drawing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vlsi-hero.git
cd vlsi-hero
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Set up PostgreSQL database:
```bash
# Create database and set DATABASE_URL environment variable
export DATABASE_URL="postgresql://username:password@localhost/vlsi_hero"
```

5. Initialize the database:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. Build CSS:
```bash
npm run build:css
```

## Usage

1. Start the Flask application:
```bash
python main.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Begin your VLSI learning journey!

## Project Structure

```
vlsi-hero/
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── models.py             # Database models
├── pages/                # HTML pages
│   ├── homepage_gamified_ed_tech_platform.html
│   ├── vlsi_fundamentals.html
│   ├── digital_design.html
│   ├── circuit_simulation.html
│   ├── quiz_challenge.html
│   └── progress_tracking.html
├── js/                   # JavaScript modules
│   ├── main.js
│   ├── progress.js
│   ├── quiz.js
│   └── circuit-simulator.js
├── css/                  # Stylesheets
│   └── main.css
├── assets/               # Static assets
├── package.json          # Node.js dependencies
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## API Endpoints

- `GET /api/progress` - Get user progress data
- `POST /api/progress` - Update user progress
- `POST /api/quiz/submit` - Submit quiz results
- `GET /api/achievements` - Get user achievements
- `GET /api/learning-sessions` - Get learning session history
- `GET /api/dashboard-stats` - Get dashboard statistics

## Database Schema

- **users**: User accounts with secure authentication
- **progress**: XP, levels, modules completed, study time
- **achievements**: Unlockable badges and milestones
- **quiz_attempts**: Detailed quiz performance analytics
- **learning_sessions**: Session tracking and duration
- **circuit_designs**: Saved circuit designs and simulations

## Features in Detail

### Learning Modules
- **VLSI Fundamentals**: Introduction to digital design concepts
- **Digital Design**: Logic gates, Boolean algebra, and circuit design
- **Circuit Simulation**: Interactive circuit builder and simulator
- **Quiz Challenges**: Comprehensive knowledge testing

### Gamification
- **XP System**: Earn experience points for learning activities
- **Achievements**: Unlock badges for milestones and perfect scores
- **Streaks**: Daily learning streak tracking
- **Levels**: Progressive difficulty with level-based rewards

### Analytics
- **Progress Tracking**: Real-time progress visualization
- **Performance Metrics**: Quiz scores, completion rates, study time
- **Learning Charts**: Visual progress over time

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with modern web technologies for optimal performance
- Responsive design for desktop and mobile devices
- Educational content focused on practical VLSI learning
- Gamification elements to enhance learning engagement