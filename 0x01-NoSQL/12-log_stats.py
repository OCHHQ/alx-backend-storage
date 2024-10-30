#!/usr/bin/env python3
"""
A script to display log statistics from the 'nginx' collection within the 'logs' database in MongoDB.
It outputs the total log count, counts of each HTTP method, and the count of status checks.
"""
from pymongo import MongoClient


def main():
    """
    Connect to the MongoDB 'logs' database, access the 'nginx' collection, 
    and print statistics on HTTP methods and status checks.
    """
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # Get the total count of documents in the collection
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Display counts for each HTTP method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count documents where method is GET and path is /status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    main();
