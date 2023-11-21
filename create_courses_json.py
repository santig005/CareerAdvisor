import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careeradvisor.settings')

import django
django.setup()

from page.models import Courses
import json

def save_course_names_and_labels(output_file):
    all_courses = Courses.objects.all()
    
    # Extract unique course names and labels
    course_data = [{'name': course.name, 'labels': course.labels} for course in all_courses]
    print(course_data)
    
    # Save to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(course_data, json_file, indent=2)

output_json_file = "output_courses.json"
save_course_names_and_labels(output_json_file)