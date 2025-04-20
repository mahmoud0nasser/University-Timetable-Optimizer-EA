"""
Test cases for the timetable model.
"""
import pytest
import numpy as np
from src.models.timetable import Timetable, Course, Lecturer, TimeSlot

def test_timetable_creation():
    """Test timetable creation with sample data."""
    # Create sample data
    courses = [
        Course(id=0, name="Math", duration=2, required_rooms=[0, 1], lecturer=0),
        Course(id=1, name="Physics", duration=1, required_rooms=[1, 2], lecturer=1)
    ]
    
    lecturers = [
        Lecturer(id=0, name="Dr. Smith", available_slots=[(0, 0), (0, 1), (1, 0)]),
        Lecturer(id=1, name="Dr. Jones", available_slots=[(0, 2), (1, 1), (1, 2)])
    ]
    
    rooms = [0, 1, 2]
    
    # Create timetable
    timetable = Timetable(courses, lecturers, rooms)
    
    # Test initial state
    assert len(timetable.schedule) == 0
    assert len(timetable.courses) == 2
    assert len(timetable.lecturers) == 2
    assert len(timetable.rooms) == 3

def test_timetable_validation():
    """Test timetable validation with various scenarios."""
    # Create sample data
    courses = [
        Course(id=0, name="Math", duration=2, required_rooms=[0, 1], lecturer=0),
        Course(id=1, name="Physics", duration=1, required_rooms=[1, 2], lecturer=1)
    ]
    
    lecturers = [
        Lecturer(id=0, name="Dr. Smith", available_slots=[(0, 0), (0, 1), (1, 0)]),
        Lecturer(id=1, name="Dr. Jones", available_slots=[(0, 2), (1, 1), (1, 2)])
    ]
    
    rooms = [0, 1, 2]
    
    # Create timetable
    timetable = Timetable(courses, lecturers, rooms)
    
    # Test valid schedule
    timetable.schedule = {
        0: [
            TimeSlot(day=0, period=0, room=0),
            TimeSlot(day=0, period=1, room=0)
        ],
        1: [
            TimeSlot(day=0, period=2, room=1)
        ]
    }
    
    is_valid, message = timetable.is_valid()
    assert is_valid
    assert message == "Valid timetable"
    
    # Test room conflict
    timetable.schedule = {
        0: [
            TimeSlot(day=0, period=0, room=0),
            TimeSlot(day=0, period=1, room=0)
        ],
        1: [
            TimeSlot(day=0, period=0, room=0)  # Room conflict
        ]
    }
    
    is_valid, message = timetable.is_valid()
    assert not is_valid
    assert "Room conflict" in message
    
    # Test lecturer conflict
    timetable.schedule = {
        0: [
            TimeSlot(day=0, period=0, room=0),
            TimeSlot(day=0, period=1, room=0)
        ],
        1: [
            TimeSlot(day=0, period=0, room=1)  # Lecturer conflict
        ]
    }
    
    is_valid, message = timetable.is_valid()
    assert not is_valid
    assert "Lecturer conflict" in message

def test_fitness_calculation():
    """Test fitness calculation for different schedules."""
    # Create sample data
    courses = [
        Course(id=0, name="Math", duration=2, required_rooms=[0, 1], lecturer=0),
        Course(id=1, name="Physics", duration=1, required_rooms=[1, 2], lecturer=1)
    ]
    
    lecturers = [
        Lecturer(id=0, name="Dr. Smith", available_slots=[(0, 0), (0, 1), (1, 0)]),
        Lecturer(id=1, name="Dr. Jones", available_slots=[(0, 2), (1, 1), (1, 2)])
    ]
    
    rooms = [0, 1, 2]
    
    # Create timetable
    timetable = Timetable(courses, lecturers, rooms)
    
    # Test perfect schedule (consecutive slots, same room)
    timetable.schedule = {
        0: [
            TimeSlot(day=0, period=0, room=0),
            TimeSlot(day=0, period=1, room=0)
        ],
        1: [
            TimeSlot(day=0, period=2, room=1)
        ]
    }
    
    fitness = timetable.get_fitness()
    assert fitness == 0.0  # Perfect schedule
    
    # Test schedule with non-consecutive slots
    timetable.schedule = {
        0: [
            TimeSlot(day=0, period=0, room=0),
            TimeSlot(day=1, period=0, room=0)  # Different day
        ],
        1: [
            TimeSlot(day=0, period=2, room=1)
        ]
    }
    
    fitness = timetable.get_fitness()
    assert fitness > 0.0  # Penalty for non-consecutive slots 