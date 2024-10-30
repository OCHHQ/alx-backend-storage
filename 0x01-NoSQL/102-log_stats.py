#!/usr/bin/env python3
"""A script that fetches and displays log statistics from MongoDB.
"""

from pymongo import MongoClient
from collections import Counter


def log_stats():
    """Fetch and display log statistics from the MongoDB 'logs' database."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count the HTTP methods
    methods = Counter()
    for log in collection.find():
        method = log.get("method")
        methods[method] += 1

    print("Methods:")
    for method, count in methods.most_common():
        print(f"\tmethod {method}: {count}")

    # Count status codes
    status_count = Counter()
    for log in collection.find():
        status_code = log.get("status")
        status_count[status_code] += 1

    print(f"{sum(status_count.values())} status check")

    # Count IPs
    ip_count = Counter()
    for log in collection.find():
        ip = log.get("ip")
        ip_count[ip] += 1

    print("IPs:")
    for ip, count in ip_count.most_common(10):
        print(f"\t{ip}: {count}")


if __name__ == "__main__":
    log_stats()
