#!/usr/bin/env python3

import json
from kafka import KafkaProducer


servers = ['localhost:9092']
topics = ['topic1', 'topic2', 'topic3']

producer = KafkaProducer(bootstrap_servers=servers,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

with open('processed_data.json', 'r') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        for topic in topics:
            producer.send(topic, value=data)
        
        if i == 20000:
            break
        if i % 1000 == 0:
            print(f'current line:  {i+1}')
