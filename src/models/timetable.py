"""
University Timetabling Model implementation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np

@dataclass
class Course:
    id: int
    name: str
    duration: int  # Number of hours (1-4)
    lecturer: int  # Lecturer ID
    required_rooms: List[int]  # List of room IDs

@dataclass
class Lecturer:
    id: int
    name: str
    available_slots: List[List[int]]  # List of [day, period] pairs

@dataclass
class TimeSlot:
    day: int
    period: int
    room: int

class Timetable:
    def __init__(self, 
                 courses: List[Course],
                 lecturers: List[Lecturer],
                 rooms: List[int],
                 days: int = 5,
                 periods_per_day: int = 8):
        self.courses = courses
        self.lecturers = lecturers
        self.rooms = rooms
        self.days = days
        self.periods_per_day = periods_per_day
        self.schedule = {}  # course_id -> list of TimeSlots
        
    def get_fitness(self) -> float:
        """Calculate the fitness of the current timetable (lower is better)."""
        penalties = 0.0
        
        # Check room conflicts
        room_schedule = {}  # (day, period, room) -> course_id
        for course_id, slots in self.schedule.items():
            course = next(c for c in self.courses if c.id == course_id)
            
            # Check if rooms are valid for this course
            for slot in slots:
                if slot.room not in course.required_rooms:
                    penalties += 100  # Major penalty for invalid room
                
                key = (slot.day, slot.period, slot.room)
                if key in room_schedule:
                    penalties += 1000  # Major penalty for room conflict
                room_schedule[key] = course_id
        
        # Check lecturer conflicts
        lecturer_schedule = {}  # (day, period, lecturer_id) -> course_id
        for course_id, slots in self.schedule.items():
            course = next(c for c in self.courses if c.id == course_id)
            lecturer = next(l for l in self.lecturers if l.id == course.lecturer)
            
            # Check lecturer availability
            for slot in slots:
                if not any(avail[0] == slot.day and avail[1] == slot.period 
                          for avail in lecturer.available_slots):
                    penalties += 100  # Major penalty for unavailable slot
                
                key = (slot.day, slot.period, course.lecturer)
                if key in lecturer_schedule:
                    penalties += 1000  # Major penalty for lecturer conflict
                lecturer_schedule[key] = course_id
        
        # Check course continuity (slots should be on same day and consecutive)
        for course_id, slots in self.schedule.items():
            if len(slots) > 1:
                slots.sort(key=lambda x: (x.day, x.period))
                prev_slot = slots[0]
                for slot in slots[1:]:
                    if slot.day != prev_slot.day:
                        penalties += 50  # Penalty for splitting course across days
                    elif slot.period != prev_slot.period + 1:
                        penalties += 30  # Penalty for non-consecutive periods
                    prev_slot = slot
        
        return penalties