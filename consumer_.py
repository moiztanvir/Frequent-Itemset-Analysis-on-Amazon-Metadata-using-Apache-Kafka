#!/usr/bin/env python3

import json
from kafka import KafkaConsumer
from collections import defaultdict
from itertools import combinations
from operator import itemgetter

# Kafka configuration
hosts = ['localhost:9092']
topics = ['topic1', 'topic2', 'topic3']

# Apriori parameters
min_supp = 0.04
min_conf = 0.5

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

        if total_records >= 100:
            break

    except KeyboardInterrupt:
        break

# Apriori algorithm
frequent_items = [item for item, count in item_counts.items() if count / total_records >= min_supp]

rules = []
for k in range(2, len(frequent_items) + 1):
    candidate_sets = []
    print(k)
    if k==300:
        break
    for i in range(len(frequent_items) - k + 1):
        if i == 1000:
            break
        itemset = tuple(frequent_items[i:i+k])
        supp = min(item_counts[item] for item in itemset) / total_records
        if supp >= min_supp:
            for i in range(1, len(itemset)):
                left = itemset[:i]
                right = itemset[i:]
                left_supp = item_counts[left[0]] / total_records
                if left_supp > 0:
                    conf = supp / left_supp
                    if conf >= min_conf:
                        rules.append((left, right, supp, conf))

# Print the most frequent items and association rules
print("Most Frequent Items:")
with open('apriori.txt','w') as f:
    f.write('Most Frequent Items\n')
    for item, count in sorted(item_counts.items(), key=itemgetter(1), reverse=True):
        print(f"{item}: {count}")
        f.write(f'{item}: {count}\n')

    print("\nAssociation Rules:")
    f.write('\nAssociation Rules')

    for left, right, supp, conf in sorted(rules, key=itemgetter(2, 3), reverse=True):
        print(f"{', '.join(left)} => {', '.join(right)} (Support: {supp:.2f}, Confidence: {conf:.2f})")
        f.write(f"{', '.join(left)} => {', '.join(right)} (Support: {supp:.2f}, Confidence: {conf:.2f})\n")

print(f"\nTotal Records: {total_records}")