#!/usr/bin/env python3
"""12-log_stats.py"""
from pymongo import MongoClient


def main():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Total number of logs
    total_logs = nginx_collection.count_documents({})

    # Count logs by methods
    methods_count = {
        "GET": nginx_collection.count_documents({"method": "GET"}),
        "POST": nginx_collection.count_documents({"method": "POST"}),
        "PUT": nginx_collection.count_documents({"method": "PUT"}),
        "PATCH": nginx_collection.count_documents({"method": "PATCH"}),
        "DELETE": nginx_collection.count_documents({"method": "DELETE"})
    }

    # Count logs with method=GET and path=/status
    status_check_count = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"})

    # Output
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods_count:
        print(f"\tmethod {method}: {methods_count[method]}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    main()
