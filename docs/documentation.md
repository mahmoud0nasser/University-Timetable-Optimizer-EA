# University Timetable Optimizer Documentation

## Overview

The University Timetable Optimizer is a web-based application that uses evolutionary algorithms to automatically generate optimal course timetables. The system considers various constraints such as room availability, lecturer schedules, and course durations to create conflict-free timetables.

## System Architecture

### 1. Core Components

#### Data Models (src/models/timetable.py)
- **Course**: Represents a university course
  - Properties: id, name, duration, required_rooms, lecturer
- **Lecturer**: Represents a teaching staff member
  - Properties: id, name, available_slots
- **TimeSlot**: Represents a scheduled time slot
  - Properties: day, period, room
- **Timetable**: Main class for timetable management
  - Handles scheduling logic and constraint checking

#### Optimization Algorithms (src/algorithms/)

1. **Particle Swarm Optimization (pso.py)**
   - Population-based optimization technique
   - Each particle represents a potential timetable solution
   - Parameters:
     - Number of particles
     - Number of iterations
     - Inertia weight
     - Cognitive and social weights
     - Maximum velocity

2. **Genetic Algorithm (genetic.py)**
   - Evolutionary optimization approach
   - Uses natural selection principles
   - Features:
     - Tournament selection
     - Uniform crossover
     - Adaptive mutation
     - Elitism

### 2. Data Management

#### JSON Data Storage
- **courses.json**: Stores course information
  ```json
  {
    "id": 9,
    "name": "Machine Learning",
    "duration": 2,
    "required_rooms": [0, 2],
    "lecturer": 5
  }
  ```
- **lecturers.json**: Stores lecturer information
  ```json
  {
    "id": 1,
    "name": "Dr. Hossam",
    "available_slots": [[0,1], [0,2], [1,3]]  // [day, period] pairs
  }
  ```

### 3. User Interface (app.py)

#### Main Features
1. **Data Management**
   - Add/remove courses and lecturers
   - Set course requirements
   - Define lecturer availability

2. **Algorithm Settings**
   - Choose optimization algorithm (PSO or GA)
   - Configure algorithm parameters
   - Set optimization constraints

3. **Timetable Display**
   - Interactive timetable view
   - Filter by days and rooms
   - Clear visualization of course and lecturer assignments

## 🖼️ Application Screens

Below are key screens illustrating the application UI and workflow:

- **Home Page**  
  ![Home Page](../Misc/home.png)

- **Manage Courses**  
  ![Manage Courses](../Misc/ManageCourses.png)

- **Existing Courses View**  
  ![Existing Courses View](../Misc/Existing_Courses.png)

- **Manage Lecturers**  
  ![Manage Lecturers](../Misc/Manage_Lectures.png)

- **Existing Lecturers View**  
  ![Existing Lecturers View](../Misc/Existing_Lectures.png)

- **Algorithm Settings**  
  ![Algorithm Settings](../Misc/Algorithm_Setting.png)

- **Algorithm Choosing & Parameters**  
  ![Algorithm Choosing & Parameters](../Misc/Algorithm_Choosing_Parameters.png)

- **Timetable Before Optimization**  
  ![Timetable Before Optimization](../Misc/Timetable_before_Applied_Algoirthm.png)

- **Timetable After PSO**  
  ![Timetable After PSO](../Misc/Timetable_after_applying_pso.png)

- **Timetable After GA**  
  ![Timetable After GA](../Misc/Timetable_after_applying_genetic.png)

- **Schedule Statistics**  
  ![Schedule Statistics](../Misc/Scheduled_Stat.png)


## Current Faculty and Courses

### Faculty Members
The current faculty members in the system include:
- Dr. Wael (ID: 0) - Physics Department
- Dr. Hossam (ID: 1) - Computer Science Department
- Dr. Islam (ID: 2) - Mathematics Department
- Dr. Khaled (ID: 3) - Chemistry Department
- Dr. Ahmed Ali (ID: 4) - Biology Department

### Featured Courses
The system currently includes the following courses:
- Physics 101 & 102 (Dr. Wael)
- Computer Science 101 & 102 (Dr. Hossam)
- Mathematics 101 (Dr. Islam)
- Chemistry 101 (Dr. Khaled)
- Biology 101 (Dr. Ahmed Ali)
- Engineering 101
- Art 101
- Machine Learning (New addition to the curriculum)

## Implementation Details

### 1. Constraint Handling

The system enforces several constraints:
- No room double-booking
- No lecturer schedule conflicts
- Courses must be in required rooms
- Respect lecturer availability
- Maintain course duration requirements

### 2. Solution Encoding

Both algorithms use a similar solution encoding:
- Each solution is an array of values
- Values are grouped in triplets: [day, period, room]
- Day ranges: 0-4 (Monday to Friday)
- Period ranges: 0-7 (8 periods per day)
- Room ranges: 0-7 (8 available rooms)

### 3. Fitness Evaluation

The fitness function considers:
1. Hard constraints (must be satisfied):
   - No scheduling conflicts
   - Room availability
   - Lecturer availability

2. Soft constraints (preferences):
   - Preferred time slots
   - Room preferences
   - Continuous scheduling

## Usage Guide

### 1. Initial Setup
1. Start the application: `streamlit run app.py`
2. Add courses and lecturers in the "Manage Data" tab
3. Set up course requirements and lecturer availability

### 2. Generating Timetables
1. Select optimization algorithm (PSO or GA)
2. Configure algorithm parameters
3. Click "Generate Timetable"
4. View and filter results

### 3. Managing Data
1. Add new courses with:
   - Course name
   - Duration (hours)
   - Required rooms
   - Assigned lecturer

2. Add new lecturers with:
   - Lecturer name
   - Available days

## Performance Optimization

The system includes several optimizations:
1. Efficient data structures for constraint checking
2. Parallel fitness evaluation
3. Caching of intermediate results
4. Early termination for invalid solutions

## Future Enhancements

Potential improvements include:
1. Multi-objective optimization
2. Machine learning for parameter tuning
3. Real-time collaborative editing
4. Advanced visualization options
5. Integration with university systems
