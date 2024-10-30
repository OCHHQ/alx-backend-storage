#!/usr/bin/env python3
"""Module to handle student records in a MongoDB collection.

This module provides functionality to retrieve and process student
information from a MongoDB collection.
"""

from pymongo import MongoClient


def top_students(mongo_collection):
    """Returns all students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of dictionaries containing student information sorted by
        average score in descending order.
    """
    result = []
    students = mongo_collection.find()

    for student in students:
        total_score = 0
        total_topics = len(student.get('topics', []))

        for topic in student.get('topics', []):
            total_score += topic.get('score', 0)

        average_score = total_score / total_topics if total_topics > 0 else 0

        result.append({
            '_id': student['_id'],
            'name': student['name'],
            'averageScore': average_score
        })

    return sorted(result, key=lambda x: x['averageScore'], reverse=True)


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(
            student.get('_id'),
            student.get('name'),
            student.get('averageScore')))
