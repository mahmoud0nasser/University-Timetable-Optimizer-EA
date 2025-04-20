# University Timetable Optimizer Documentation

## 1. System Overview

The University Timetable Optimizer is a sophisticated web-based application that leverages evolutionary algorithms to generate optimal course schedules. It addresses the complex challenge of creating conflict-free timetables while satisfying multiple constraints and preferences.

### 1.1 Key Features

- Automated timetable generation using PSO and GA
- Constraint-based scheduling
- Interactive web interface
- Real-time conflict detection
- Flexible data management
- Schedule visualization and statistics

## 2. Technical Architecture

### 2.1 Core Components

#### Data Models (`src/models/timetable.py`)
- **Course**
  ```python
  class Course:
      id: int
      name: str
      duration: int
      required_rooms: List[int]
      lecturer: int
  ```
- **Lecturer**
  ```python
  class Lecturer:
      id: int
      name: str
      available_slots: List[List[int]]  # [day, period] pairs
  ```
- **TimeSlot**
  ```python
  class TimeSlot:
      day: int        # 0-4 (Mon-Fri)
      period: int     # 0-7 (8 periods/day)
      room: int       # 0-7 (8 rooms)
  ```
- **Timetable**
  - Manages scheduling logic
  - Handles constraint validation
  - Calculates fitness scores

### 2.2 Optimization Algorithms

#### 2.2.1 Particle Swarm Optimization (`src/algorithms/pso.py`)
- **Features**:
  - Population-based optimization
  - Adaptive inertia weight
  - Velocity clamping
  - Global and local best memory
- **Parameters**:
  - Number of particles (20-100)
  - Number of iterations (50-200)
  - Inertia weight (0.4-0.9)
  - Cognitive/social weights (1.5-2.5)

#### 2.2.2 Genetic Algorithm (`src/algorithms/genetic.py`)
- **Features**:
  - Tournament selection
  - Uniform crossover
  - Adaptive mutation
  - Elitism preservation
- **Parameters**:
  - Population size (50-200)
  - Number of generations (100-500)
  - Mutation rate (0.1-0.3)
  - Tournament size (3-5)
  - Elite size (2-5)

### 2.3 Data Management

#### 2.3.1 JSON Storage
- **courses.json**
  ```json
  {
    "id": 1,
    "name": "Computer Science 101",
    "duration": 2,
    "required_rooms": [0, 2],
    "lecturer": 1
  }
  ```
- **lecturers.json**
  ```json
  {
    "id": 1,
    "name": "Dr. Hossam",
    "available_slots": [[0,1], [0,2], [1,3]]
  }
  ```

## 3. Implementation Details

### 3.1 Constraint Handling

#### Hard Constraints
1. **Room Conflicts**
   - No double-booking of rooms
   - Room type requirements must be met

2. **Lecturer Conflicts**
   - No overlapping schedules
   - Respect availability preferences

3. **Course Requirements**
   - Duration must be respected
   - All sessions must be scheduled

#### Soft Constraints
1. **Optimization Goals**
   - Minimize travel time between rooms
   - Balance room utilization
   - Maximize preferred time slots

### 3.2 Solution Encoding

- **Format**: Array of real numbers
- **Structure**: [day₁, period₁, room₁, day₂, period₂, room₂, ...]
- **Decoding**:
  - Values rounded to integers
  - day mod 5 (0-4)
  - period mod 8 (0-7)
  - room based on requirements

### 3.3 Fitness Function

```python
def fitness_function(solution):
    # Hard constraints
    conflicts = check_conflicts(solution)
    if conflicts > 0:
        return float('inf')
    
    # Soft constraints
    score = 0
    score += calculate_travel_time(solution)
    score += calculate_room_balance(solution)
    score += calculate_time_preferences(solution)
    return score
```

## 4. User Interface

### 4.1 Main Components
1. **Data Management**
   - Course creation/editing
   - Lecturer management
   - Room configuration

2. **Algorithm Settings**
   - Algorithm selection
   - Parameter configuration
   - Constraint weighting

3. **Timetable View**
   - Interactive grid display
   - Filtering options
   - Conflict highlighting

### 4.2 Workflow
1. **Setup Phase**
   - Add/edit courses
   - Configure lecturer availability
   - Set room constraints

2. **Optimization Phase**
   - Select algorithm
   - Adjust parameters
   - Run optimization

3. **Review Phase**
   - View generated timetable
   - Check statistics
   - Make manual adjustments

## 5. Performance Considerations

### 5.1 Optimizations
- Efficient data structures for conflict checking
- Parallel fitness evaluation
- Caching of intermediate results
- Early termination for invalid solutions

### 5.2 Scalability
- Handles up to 100 courses
- Supports 50+ lecturers
- 8 time periods per day
- 5 working days
- 8 different rooms

## 6. Future Enhancements

### 6.1 Planned Features
1. Multi-objective optimization
2. Machine learning for parameter tuning
3. Real-time collaborative editing
4. Advanced visualization options
5. Integration with university systems

### 6.2 Potential Improvements
- Enhanced constraint customization
- Additional optimization algorithms
- Mobile-responsive design
- Export to various formats
- API integration capabilities

## 7. Troubleshooting

### 7.1 Common Issues
1. **No Valid Solution Found**
   - Check constraint strictness
   - Increase iteration count
   - Adjust room availability

2. **Poor Quality Solutions**
   - Tune algorithm parameters
   - Review constraint weights
   - Increase population size

3. **Performance Issues**
   - Reduce problem size
   - Optimize constraint checking
   - Use parallel processing

## 8. References

1. Kennedy, J., & Eberhart, R. (1995). Particle Swarm Optimization.
2. Holland, J. H. (1992). Genetic Algorithms.
3. Burke, E. K., & Petrovic, S. (2002). Recent research directions in automated timetabling.

---

*Documentation maintained by Mahmoud Nasser*
*Last updated: April 2025*
