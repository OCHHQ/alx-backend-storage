# 11-schools_by_topic.py


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools having a specific topic.

    Parameters:
    mongo_collection (pymongo collection): The pymongo collection object.
    topic (str): The topic searched for.

    Returns:
    list: A list of schools with the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))
