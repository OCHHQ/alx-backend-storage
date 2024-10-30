#!/usr/bin/env python3
"""
Module for MongoDB operations - listing all documents in a collection
"""
from typing import List
from pymongo.collection import Collection


def list_all(mongo_collection: Collection) -> List:
    """
    Lists all documents in a MongoDB collection.

    Args:
        mongo_collection: PyMongo collection object to query from

    Returns:
        List of all documents in the collection
        Empty list if no documents are found or if collection is invalid
    """
    if mongo_collection is None:
        return []
    
    try:
        # Find all documents in the collection and convert cursor to list
        documents = list(mongo_collection.find())
        return documents
    except Exception:
        # Return empty list if any error occurs
        return []
