#!/usr/bin/env python3

import json
from kafka import KafkaConsumer
from collections import defaultdict
from itertools import combinations
from operator import itemgetter

# Kafka configuration
hosts = ['localhost:9092']
topics = ['topic1', 'topic2', 'topic3']

# SON parameters
min_supp = 0.04
sample_size = 1000

# Create Kafka consumer
consumer = KafkaConsumer(*topics, bootstrap_servers=hosts, auto_offset_reset='earliest', enable_auto_commit=True, value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Frequency dictionary to store item frequencies
item_counts = defaultdict(int)
sample_counts = defaultdict(int)

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
                    sample_counts[item] += 1
                total_records += 1

        if total_records >= 1000:
            break

    except KeyboardInterrupt:
        break

# SON algorithm
frequent_items_pass1 = [item for item, count in sample_counts.items() if count >= min_supp * sample_size]

frequent_items_pass2 = [item for item, count in item_counts.items() if count >= min_supp * total_records]

# Find all possible frequent itemsets
all_frequent_itemsets = []
for k in range(1, len(frequent_items_pass2) + 1):
    for itemset in combinations(frequent_items_pass2, k):
        supp = min(item_counts[item] for item in itemset) / total_records
        if supp >= min_supp:
            all_frequent_itemsets.append(itemset)

# Print the most frequent items and frequent itemsets
print("Most Frequent Items:")
with open('son.txt', 'w') as f:
    f.write('Most Frequent Items\n')
    for item, count in sorted(item_counts.items(), key=itemgetter(1), reverse=True):
        print(f"{item}: {count}")
        f.write(f"{item}: {count}\n")

    print("\nFrequent Itemsets:")
    f.write('\nFrequent Itemsets\n')
    for itemset in sorted(all_frequent_itemsets, key=lambda x: (len(x), x)):
        supp = min(item_counts[item] for item in itemset) / total_records
        print(f"Frequent Itemset: {', '.join(itemset)} (Support: {supp:.2f})")
        f.write(f"Frequent Itemset: {', '.join(itemset)} (Support: {supp:.2f})\n")

print(f"\nTotal Records: {total_records}")