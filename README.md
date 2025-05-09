# University Timetable Optimizer

A Python-based application that uses evolutionary algorithms (PSO and Genetic Algorithm) to generate optimal university course timetables. This project helps universities automatically create conflict-free schedules while considering various constraints like room availability, lecturer preferences, and course requirements.

## 🌟 Features

### Optimization Algorithms
- **Particle Swarm Optimization (PSO)**
  - Population-based optimization
  - Adaptive inertia weight
  - Configurable parameters
- **Genetic Algorithm (GA)**
  - Tournament selection
  - Uniform crossover
  - Adaptive mutation rate
  - Elitism preservation

### Course Management
- Add/remove courses with:
  - Course name and duration
  - Required room types
  - Assigned lecturers
  - Schedule constraints

### Lecturer Management
- Manage lecturer profiles:
  - Set availability by day/time
  - View assigned courses
  - Track teaching load
  - Prevent scheduling conflicts

### Current Data
- **Faculty**: Dr. Wael, Dr. Hossam, Dr. Islam, Dr. Khaled, Dr. Ahmed Ali
- **Courses**: Physics, Computer Science, Mathematics, Chemistry, Biology, Engineering, Art, Machine Learning

### Timetable Generation
- **Constraint Handling**:
  - No room double-booking
  - No lecturer conflicts
  - Course duration respect
  - Room type requirements
- **Optimization Goals**:
  - Minimize travel time
  - Balance room utilization
  - Maximize preferred slots

### Interactive UI
- **Real-time Updates**:
  - Dynamic timetable view
  - Instant conflict detection
  - Schedule modifications
- **Filtering Options**:
  - By day/time
  - By room
  - By lecturer
  - By course

## 🖼️ Application Screens

Below is an overview of the key screens in the University Timetable Optimizer UI:

### Home Page
![Home Page](Misc/Home.PNG)

### Course Management
![Manage Courses](Misc/ManageCourses.PNG)
![Existing Courses](Misc/Existing_Courses.PNG)

### Lecturer Management
![Manage Lecturers](Misc/Manage_Lectures.PNG)
![Existing Lecturers](Misc/Existing_Lectures.PNG)

### Algorithm Configuration
![Algorithm Settings](Misc/Algorithm_Setting.PNG)
![Algorithm Parameters](Misc/Algorithm_Choosing_Parameters.PNG)

### Timetable Views
![Before Optimization](Misc/Timetable_before_Applied_Algoirthm.PNG)
![After PSO](Misc/Timetable_after_applying_PSO.PNG)
![After GA](Misc/Timetable_after_applying_Genetic.PNG)

### Statistics
![Schedule Statistics](Misc/Scheduled_Stat.PNG)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
1. Clone the repository:
```bash
git clone https://github.com/mahmoud0nasser/University-Timetable-Optimizer-EA.git
cd University-Timetable-Optimizer-EA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
1. Start the web interface:
```bash
streamlit run app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## 📁 Project Structure
```
EA Project/
├── app.py                 # Main application & UI (Streamlit)
├── src/
│   ├── algorithms/        # Optimization algorithms
│   │   ├── pso.py        # Particle Swarm Optimization
│   │   └── genetic.py    # Genetic Algorithm
│   └── models/           # Data models
│       └── timetable.py  # Core timetable classes
├── data/                 # Data storage
│   ├── courses.json     # Course information
│   └── lecturers.json   # Lecturer information
├── results/             # Generated timetables
│   └── best_timetable.json  # Optimized timetable
└── docs/                # Documentation
    └── documentation.md # Detailed technical docs
```

## 🛠️ Dependencies
- **Streamlit**: Web interface framework
- **NumPy**: Numerical computations
- **Pandas**: Data manipulation
- **JSON**: Data storage

## 📊 Example Usage
1. **Data Setup**:
   - Add courses with their requirements
   - Define lecturer availability
   - Set room constraints

2. **Algorithm Configuration**:
   - Choose PSO or GA
   - Adjust optimization parameters
   - Set constraints priority

3. **Timetable Generation**:
   - Run optimization
   - Review generated schedule
   - Make manual adjustments
   - Export final timetable

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors
- Mahmoud Nasser - Initial work and maintenance

## 🙏 Acknowledgments
- Faculty of Computer and Artificial Intelligence Helwan University
- All contributors who helped with testing and feedback