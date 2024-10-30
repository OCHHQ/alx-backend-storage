#!/usr/bin/env python3
"""A script that fetches and displays log statistics from MongoDB."""

from pymongo import MongoClient


def log_stats():
    """Fetch and display log statistics from the MongoDB 'logs' database."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count the HTTP methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count status check occurrences
    status_count = collection.count_documents({"path": "/status"})
    print(f"{status_count} status check")

    # Top 10 most common IPs
    print("IPs:")
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
