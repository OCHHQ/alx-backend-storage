#!/usr/bin/env python3
"""
Script to insert a new document into a MongoDB collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into a collection based on kwargs.

    Parameters:
    mongo_collection (pymongo.collection.Collection):
    The MongoDB collection object.
    **kwargs: Arbitrary keyword arguments representing
    the document's fields.

    Returns:
    ObjectId: The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
