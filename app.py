"""
University Timetable Optimizer - Main Application
"""
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta
from src.models.timetable import Timetable, Course, Lecturer, TimeSlot
from src.algorithms.pso import PSO
from src.algorithms.genetic import GeneticAlgorithm, GeneticAlgorithmConfig

# Set page config
st.set_page_config(
    page_title="University Timetable Optimizer",
    page_icon="📚",
    layout="wide"
)

# Time slots configuration
START_TIME = datetime.strptime("08:00", "%H:%M")
SLOT_DURATION = 60  # minutes

def get_time_for_period(period):
    """Convert period number to actual time"""
    time = START_TIME + timedelta(minutes=period * SLOT_DURATION)
    return time.strftime("%H:%M")

def load_data():
    """Load courses and lecturers from JSON files"""
    try:
        with open('data/courses.json', 'r') as f:
            courses_data = json.load(f)
        with open('data/lecturers.json', 'r') as f:
            lecturers_data = json.load(f)
        try:
            with open('results/best_timetable.json', 'r') as f:
                saved_timetable = json.load(f)
        except FileNotFoundError:
            saved_timetable = {}
    except FileNotFoundError:
        courses_data = []
        lecturers_data = []
        saved_timetable = {}
    
    courses = [Course(id=c["id"], name=c["name"], duration=c["duration"], 
                     required_rooms=c["required_rooms"], lecturer=c["lecturer"]) 
               for c in courses_data]
    lecturers = [Lecturer(id=l["id"], name=l["name"], available_slots=l["available_slots"]) 
                 for l in lecturers_data]
    rooms = list(range(8))
    
    if "saved_timetable" in st.session_state:
        saved_timetable = st.session_state.saved_timetable
    else:
        st.session_state.saved_timetable = saved_timetable
    
    return courses, lecturers, rooms

def save_data(courses, lecturers, saved_timetable=None):
    """Save courses and lecturers to JSON files"""
    courses_data = [{"id": c.id, "name": c.name, "duration": c.duration,
                     "required_rooms": c.required_rooms, "lecturer": c.lecturer}
                    for c in courses]
    lecturers_data = [{"id": l.id, "name": l.name, "available_slots": l.available_slots}
                      for l in lecturers]
    
    os.makedirs('data', exist_ok=True)
    with open('data/courses.json', 'w') as f:
        json.dump(courses_data, f, indent=4)
    with open('data/lecturers.json', 'w') as f:
        json.dump(lecturers_data, f, indent=4)
    if saved_timetable:
        os.makedirs('results', exist_ok=True)
        with open('results/best_timetable.json', 'w') as f:
            json.dump(saved_timetable, f, indent=4)

def create_fitness_function(timetable):
    """Create a fitness function for the optimization algorithms"""
    def fitness_function(solution):
        if len(solution) != sum(course.duration * 3 for course in timetable.courses):
            raise ValueError(f"Solution array length ({len(solution)}) does not match required length")
        try:
            timetable.schedule = decode_solution(solution, timetable.courses)
            return timetable.get_fitness()
        except Exception as e:
            st.error(f"Error in fitness calculation: {str(e)}")
            return float('inf')
    return fitness_function

def decode_solution(solution, courses):
    """Decode the solution array into a timetable"""
    if len(solution) != sum(course.duration * 3 for course in courses):
        raise ValueError(f"Solution array length ({len(solution)}) does not match required length")
    
    timetable = {}
    current_index = 0
    
    for course in courses:
        slots = []
        for _ in range(course.duration):
            if current_index + 2 >= len(solution):
                raise ValueError(f"Solution array too short for course {course.id}")
            
            day = int(round(solution[current_index])) % 5
            period = int(round(solution[current_index + 1])) % 8
            room = int(round(solution[current_index + 2])) % 8
            
            slot = TimeSlot(day=day, period=period, room=room)
            slots.append(slot)
            current_index += 3
        
        slots.sort(key=lambda x: (x.day, x.period))
        timetable[course.id] = slots
    
    return timetable

def convert_schedule_to_json(schedule):
    """Convert schedule with TimeSlot objects to JSON-serializable format"""
    json_schedule = {}
    for course_id, slots in schedule.items():
        json_schedule[course_id] = [
            {
                'day': slot.day,
                'period': slot.period,
                'room': slot.room
            }
            for slot in slots
        ]
    return json_schedule

def display_timetable(timetable_data, courses, lecturers, selected_days=None, selected_rooms=None):
    """Display the timetable in a nice format"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if selected_days is None:
        selected_days = days
    if selected_rooms is None:
        selected_rooms = [f'Room {i}' for i in range(8)]
    
    # Create empty DataFrame
    df = pd.DataFrame(
        index=[get_time_for_period(i) for i in range(8)],
        columns=pd.MultiIndex.from_product([selected_days, selected_rooms])
    )
    
    # Fill timetable
    for course_id, slots in timetable_data.items():
        course = next((c for c in courses if c.id == course_id), None)
        if course is None:
            continue  # Skip if course not found
            
        lecturer = next((l for l in lecturers if l.id == course.lecturer), None)
        if lecturer is None:
            continue  # Skip if lecturer not found
        
        for slot in slots:
            day = days[slot.day]
            room = f'Room {slot.room}'
            if day in selected_days and room in selected_rooms:
                cell_content = (
                    f"{course.name}\n"
                    f"Dr. {lecturer.name}"
                )
                df.loc[get_time_for_period(slot.period), (day, room)] = cell_content
    
    # Apply custom styling
    st.dataframe(
        df.fillna(''),
        use_container_width=True,
        height=400
    )

def manage_data():
    """Manage courses and lecturers data"""
    st.write("### Manage Data")
    
    tab1, tab2 = st.tabs(["Courses", "Lecturers"])
    
    courses, lecturers, _ = load_data()  
    
    with tab1:
        st.write("#### Add New Course")
        with st.form("add_course"):
            course_name = st.text_input("Course Name")
            duration = st.number_input("Duration (hours)", min_value=1, max_value=4, value=2)
            lecturer_id = st.selectbox(
                "Lecturer",
                options=[l.id for l in lecturers],
                format_func=lambda x: next(l.name for l in lecturers if l.id == x)
            )
            required_rooms = st.multiselect(
                "Required Rooms",
                options=list(range(8)),
                default=[0, 1, 2],
                format_func=lambda x: f"Room {x}"
            )
            
            if st.form_submit_button("Add Course"):
                new_id = max([c.id for c in courses], default=-1) + 1
                new_course = Course(
                    id=new_id,
                    name=course_name,
                    duration=duration,
                    required_rooms=required_rooms,
                    lecturer=lecturer_id
                )
                courses.append(new_course)
                save_data(courses, lecturers, st.session_state.saved_timetable)
                st.success("Course added successfully!")
                st.rerun()
        
        st.write("#### Existing Courses")
        for course in courses:
            try:
                lecturer = next(l for l in lecturers if l.id == course.lecturer)
                with st.expander(f"{course.name}"):
                    st.write(f"Duration: {course.duration} hours")
                    st.write(f"Lecturer: {lecturer.name}")
                    st.write(f"Required Rooms: {', '.join(f'Room {r}' for r in course.required_rooms)}")
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("🗑️", key=f"del_course_{course.id}", help="Delete Course"):
                            if "confirm_delete_course" not in st.session_state:
                                st.session_state.confirm_delete_course = None
                            if st.session_state.confirm_delete_course == course.id:
                                courses.remove(course)
                                if st.session_state.saved_timetable and str(course.id) in st.session_state.saved_timetable:
                                    del st.session_state.saved_timetable[str(course.id)]
                                save_data(courses, lecturers, st.session_state.saved_timetable)
                                st.success("Course deleted successfully!")
                                st.rerun()
                            else:
                                st.session_state.confirm_delete_course = course.id
                                st.warning(f"Click again to confirm deleting {course.name}")
            except StopIteration:
                st.error(f"Course {course.name} (ID: {course.id}) has an invalid lecturer ID: {course.lecturer}")
                if st.button(f"Delete Invalid Course", key=f"del_invalid_course_{course.id}"):
                    courses.remove(course)
                    if st.session_state.saved_timetable and str(course.id) in st.session_state.saved_timetable:
                        del st.session_state.saved_timetable[str(course.id)]
                    save_data(courses, lecturers, st.session_state.saved_timetable)
                    st.success("Invalid course deleted successfully!")
                    st.rerun()
    
    with tab2:
        st.write("#### Add New Lecturer")
        with st.form("add_lecturer"):
            lecturer_name = st.text_input("Lecturer Name")
            availability = st.multiselect(
                "Available Days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                default=["Monday", "Tuesday", "Wednesday"]
            )
            
            if st.form_submit_button("Add Lecturer"):
                new_id = max([l.id for l in lecturers], default=-1) + 1
                # Convert days to slots
                available_slots = []
                for day_name in availability:
                    day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(day_name)
                    available_slots.extend([[day, period] for period in range(8)])
                
                new_lecturer = Lecturer(
                    id=new_id,
                    name=lecturer_name,
                    available_slots=available_slots
                )
                lecturers.append(new_lecturer)
                save_data(courses, lecturers, st.session_state.saved_timetable)
                st.success("Lecturer added successfully!")
                st.rerun()
        
        st.write("#### Existing Lecturers")
        for lecturer in lecturers:
            with st.expander(f"{lecturer.name}"):
                lecturer_courses = [c for c in courses if c.lecturer == lecturer.id]
                if lecturer_courses:
                    st.write("Teaching:")
                    for course in lecturer_courses:
                        st.write(f"- {course.name}")
                else:
                    st.write("No assigned courses")
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("🗑️", key=f"del_lecturer_{lecturer.id}", help="Delete Lecturer"):
                        if lecturer_courses:
                            st.error("Cannot delete lecturer with assigned courses. Please reassign or delete their courses first.")
                        else:
                            if "confirm_delete_lecturer" not in st.session_state:
                                st.session_state.confirm_delete_lecturer = None
                            if st.session_state.confirm_delete_lecturer == lecturer.id:
                                lecturers.remove(lecturer)
                                save_data(courses, lecturers, st.session_state.saved_timetable)
                                st.success("Lecturer deleted successfully!")
                                st.rerun()
                            else:
                                st.session_state.confirm_delete_lecturer = lecturer.id
                                st.warning(f"Click again to confirm deleting Dr. {lecturer.name}")
    
    return courses, lecturers

def main():
    st.title("University Timetable Optimizer 📚")
    
    # Add tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📅 Timetable", "⚙️ Algorithm Settings", "📝 Manage Data"])
    
    courses, lecturers, rooms = load_data()
    
    if not courses or not lecturers:
        st.warning("Please add some courses and lecturers in the Manage Data tab first!")
        return
    
    # Create timetable instance
    timetable = Timetable(courses=courses, lecturers=lecturers, rooms=rooms)
    solution_size = sum(course.duration * 3 for course in courses)  # 3 values per slot: day, period, room
    
    with tab1:
        st.write("### Current Timetable")
        
        # Add filters for better visualization
        col1, col2 = st.columns(2)
        with col1:
            selected_days = st.multiselect(
                "Filter Days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            )
        with col2:
            selected_rooms = st.multiselect(
                "Filter Rooms",
                [f"Room {i}" for i in range(8)],
                default=[f"Room {i}" for i in range(8)]
            )
        
        # Load and display existing timetable
        try:
            # Convert back to TimeSlot objects
            schedule = {}
            for course_id_str, slots in st.session_state.saved_timetable.items():
                course_id = int(course_id_str)
                schedule[course_id] = [TimeSlot(**slot) for slot in slots]
                
                # Verify that the course exists
                course = next((c for c in courses if c.id == course_id), None)
                if course is None:
                    st.error(f"Course with ID {course_id} not found in the database!")
                    continue
            
            display_timetable(schedule, courses, lecturers, selected_days, selected_rooms)
            
            # Display statistics
            st.write("### Schedule Statistics")
            total_slots = sum(len(slots) for slots in schedule.values())
            total_rooms = len(set(slot.room for slots in schedule.values() for slot in slots))
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Courses", len(courses))
            with col2:
                st.metric("Total Time Slots", total_slots)
            with col3:
                st.metric("Rooms Used", total_rooms)
            with col4:
                st.metric("Solution Size", solution_size)
            
        except Exception as e:
            st.error(f"Error loading saved timetable: {str(e)}")
    
    with tab2:
        st.write("### Algorithm Settings")
        st.info(f"Problem size: {len(courses)} courses, requiring {solution_size} variables (3 per time slot: day, period, room)")
        
        algorithm = st.selectbox(
            "Select Optimization Algorithm",
            ["PSO", "Genetic Algorithm"],
            help="Choose between Particle Swarm Optimization (PSO) or Genetic Algorithm"
        )
        
        # Algorithm-specific parameters
        if algorithm == "PSO":
            with st.expander("PSO Parameters", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    n_particles = st.slider(
                        "Number of Particles",
                        20, 200, 50,
                        help="More particles = better exploration but slower computation"
                    )
                    n_iterations = st.slider(
                        "Number of Iterations",
                        50, 500, 100,
                        help="More iterations = better solution but longer runtime"
                    )
                    w_start = st.slider(
                        "Initial Inertia Weight",
                        0.1, 1.0, 0.9,
                        help="Controls the influence of previous velocity"
                    )
                with col2:
                    w_end = st.slider(
                        "Final Inertia Weight",
                        0.1, 1.0, 0.4,
                        help="Final influence of previous velocity"
                    )
                    c1 = st.slider(
                        "Cognitive Weight",
                        0.1, 4.0, 2.0,
                        help="Influence of particle's best position"
                    )
                    c2 = st.slider(
                        "Social Weight",
                        0.1, 4.0, 2.0,
                        help="Influence of swarm's best position"
                    )
        else:
            with st.expander("Genetic Algorithm Parameters", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    population_size = st.slider(
                        "Population Size",
                        20, 200, 50,
                        help="More individuals = better exploration but slower computation"
                    )
                    n_generations = st.slider(
                        "Number of Generations",
                        50, 500, 100,
                        help="More generations = better solution but longer runtime"
                    )
                    mutation_rate = st.slider(
                        "Mutation Rate",
                        0.0, 1.0, 0.1,
                        help="Higher rate = more exploration but less stability"
                    )
                with col2:
                    tournament_size = st.slider(
                        "Tournament Size",
                        2, 10, 3,
                        help="Larger tournament = stronger selection pressure"
                    )
                    elite_size = st.slider(
                        "Elite Size",
                        1, 10, 2,
                        help="Number of best solutions to preserve"
                    )
        
        # Progress bar placeholder
        progress_placeholder = st.empty()
        
        if st.button("Generate Timetable", type="primary", use_container_width=True):
            progress_bar = progress_placeholder.progress(0)
            
            with st.spinner("Optimizing timetable..."):
                try:
                    if algorithm == "PSO":
                        optimizer = PSO(
                            n_particles=n_particles,
                            n_iterations=n_iterations,
                            w_start=w_start,
                            w_end=w_end,
                            c1=c1,
                            c2=c2
                        )
                        best_solution = optimizer.optimize(create_fitness_function(timetable), solution_size)
                    else:
                        config = GeneticAlgorithmConfig(
                            population_size=population_size,
                            n_generations=n_generations,
                            mutation_rate=mutation_rate,
                            tournament_size=tournament_size,
                            elite_size=elite_size
                        )
                        optimizer = GeneticAlgorithm(
                            config=config,
                            fitness_func=create_fitness_function(timetable)
                        )
                        best_solution = optimizer.optimize(solution_size)
                    
                    if best_solution is not None:
                        timetable.schedule = decode_solution(best_solution, courses)
                        
                        # Save the best timetable
                        st.session_state.saved_timetable = convert_schedule_to_json(timetable.schedule)
                        save_data(courses, lecturers, st.session_state.saved_timetable)
                        
                        st.success("✨ Timetable generated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to find a valid solution. Try adjusting the algorithm parameters.")
                except Exception as e:
                    st.error(f"Error during optimization: {str(e)}")
    
    with tab3:
        courses, lecturers = manage_data()

if __name__ == '__main__':
    main()
