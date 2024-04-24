#!/usr/bin/env python3

import json
from kafka import KafkaConsumer
from collections import defaultdict
from itertools import combinations
from operator import itemgetter
import hashlib
from pymongo import MongoClient

# Kafka configuration
hosts = ['localhost:9092']
topics = ['topic1', 'topic2', 'topic3']

# PCY parameters
min_supp = 0.01
min_conf = 0.3
bucket_size = 100

# MongoDB configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['your_database_name']
collection = db['your_collection_name']

# Create Kafka consumer
consumer = KafkaConsumer(*topics, bootstrap_servers=hosts, auto_offset_reset='earliest', enable_auto_commit=True, value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Frequency dictionary to store item frequencies
item_counts = defaultdict(int)

# Read data from Kafka topics
total_records = 0
while True:
    try:
        records = consumer.poll(timeout_ms=1000)
        if not records:
            continue

        for topic, messages in records.items():
            for message in messages:
                data = message.value
                items = data['sample']
                for item in items:
                    item_counts[item] += 1
                total_records += 1

        if total_records >= 200:
            break

    except KeyboardInterrupt:
        break

# PCY algorithm
frequent_items = [item for item, count in item_counts.items() if count / total_records >= min_supp]

buckets = defaultdict(list)
for item in frequent_items:
    hash_value = int(hashlib.md5(item.encode()).hexdigest(), 16) % bucket_size
    buckets[hash_value].append(item)

frequent_itemsets = [list(buckets[bucket]) for bucket in buckets]

all_frequent_itemsets = frequent_itemsets.copy()
rules = []

for k in range(2, len(frequent_items) + 1):
    candidate_itemsets = []
    for itemset in all_frequent_itemsets:
        if len(itemset) == k - 1:
            candidate_itemsets.extend(list(combinations(itemset, k)))

    frequent_itemsets = []
    for candidate_itemset in candidate_itemsets:
        supp = min(item_counts[item] for item in candidate_itemset) / total_records
        if supp >= min_supp:
            frequent_itemsets.append(candidate_itemset)
            all_frequent_itemsets.append(candidate_itemset)

    for itemset in frequent_itemsets:
        for i in range(1, len(itemset)):
            left = itemset[:i]
            right = itemset[i:]
            left_supp = min(item_counts[item] for item in left) / total_records
            if left_supp > 0:
                conf = supp / left_supp
                if conf >= min_conf:
                    rules.append((left, right, supp, conf))

# Store the data in MongoDB
for item, count in sorted(item_counts.items(), key=itemgetter(1), reverse=True):
    collection.insert_one({'item': item, 'count': count})

for itemset in all_frequent_itemsets:
    supp = min(item_counts[item] for item in itemset) / total_records
    if supp >= min_supp:
        collection.insert_one({'frequent_itemset': ', '.join(itemset), 'support': supp})

for left, right, supp, conf in sorted(rules, key=itemgetter(2, 3), reverse=True):
    collection.insert_one({'left': ', '.join(left), 'right': ', '.join(right), 'support': supp, 'confidence': conf})

print(f"Data stored in MongoDB: {total_records} records")