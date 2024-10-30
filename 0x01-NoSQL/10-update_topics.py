#!/usr/bin/env python3
"""
Script to update the topics of a school document in MongoDB.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document in a
    MongoDB collection based on name.

    Parameters:
    mongo_collection (pymongo.collection.Collection):
    The MongoDB collection object.
    name (str): The name of the school to update.
    topics (list of str): The list of topics to set for the school.

    Returns:
    None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
