#!/bin/bash

# Start Zookeeper
echo "Starting Zookeeper..."
zookeeper-server-start.sh /config/zookeeper.properties &

# Start Kafka Server
echo "Starting Kafka Server..."
kafka-server-start.sh /config/server.properties &

# Create Kafka Topic
echo "Creating Kafka Topics..."
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic topic1
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic topic2
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic topic3

# Run Producer
echo "Running Producer..."
python producer1.py &

# Run Consumer1 (Apriori)
echo "Running Consumer1 (Apriori)..."
python consumer1.py &

# Run Consumer2 (PCY)
echo "Running Consumer2 (PCY)..."
python consumer2.py &

# Wait for all processes to finish
wait

echo "All processes have finished."