# Frequent-Itemset-Analysis-on-Amazon-Metadata-using-Apache-Kafka
## Group members:

Moiz Tanvir (i221932@nu.edu.pk)

Talha Ali (i221971@nu.edu.pk)

Irtaza Ahmed (i221975@nu.edu.pk)

## Introduction

This report outlines the development and implementation of a real-time frequent itemset mining pipeline using the Amazon Metadata dataset. The project involves several stages including dataset downloading and sampling, pre-processing, setting up a streaming pipeline, implementing frequent itemset mining algorithms which includes (apriori algorithm, pcy algorithm and son algorithm), integrating with a database, and providing necessary documentation.

## Dependencies

- [JSON](https://www.json.org/json-en.html)
- [Kafka Producer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html)
- [Kafka Consumer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)
- [MongoDB](https://www.mongodb.com/docs/atlas/)

## Our Approach

### 1. Dataset Downloading and Sampling

The Amazon Metadata dataset was downloaded and sampled to ensure manageable data size for processing. The dataset was originally 12 GB in size, which increased to 105 GB after extraction. A sample size of at least 15 GB was ensured to maintain data integrity.

### 2. Pre-Processing

The sampled dataset was pre-processed to clean and format it for analysis. This involved loading the data, cleaning it of any inconsistencies or errors, and formatting it appropriately for subsequent analysis. A new JSON file containing the preprocessed data was generated. Additionally, batch processing was implemented to execute pre-processing in real-time, ensuring efficient data handling.

### 3. Streaming Pipeline Setup

A producer application was developed to stream the preprocessed data in real-time. Three consumer applications were created to subscribe to the producer's data stream, ensuring efficient distribution and processing of data.

### 4. Frequent Itemset Mining

Three different frequent itemset mining algorithms were implemented in the consumer applications. The Apriori algorithm and the PCY algorithm were implemented in two consumers, with real-time insights and associations displayed through print statements. In the third consumer, we have used SON algorithm to analyze the data, utilizing techniques such as sliding window approach, approximation techniques, and incremental processing to adapt the algorithms to the streaming environment.

### 5. Database Integration

Non-relational or NoSQL databases such as MongoDB were chosen for database integration, as they are well-suited for this project. Each consumer was modified to connect to one of the databases and store the results, ensuring data persistence and scalability.

### 6. Enhancing Project Execution with a Bash Script

A bash script was set up to automate the execution of the producer and consumer applications, as well as initialize all Kafka components such as Kafka Connect and Zookeeper. This enhances project execution by simplifying setup and deployment processes, making it easier for users to run the pipeline.

## Conclusion

The real-time frequent itemset mining pipeline developed for the Amazon Metadata dataset demonstrates effective data handling, processing, and analysis techniques. By employing appropriate sampling, pre-processing, streaming, and mining methodologies, valuable insights can be derived from large-scale datasets in real-time. The integration with non-relational databases ensures data persistence and scalability, while automation through bash scripting enhances project execution efficiency. Overall, the project showcases the application of advanced data mining techniques in a streaming environment, with potential for various real-world applications such as market basket analysis and recommendation systems.

## References

- Apriori ALgorithm Technique for Frequent Itemset Mining: https://www.geeksforgeeks.org/apriori-algorithm/
- Frequent Pattern Mining Algorithms for Finding Associated Frequent Patterns for Data Streams: https://www.researchgate.net/publication/265788733_Frequent_Pattern_Mining_Algorithms_for_Finding_Associated_Frequent_Patterns_for_Data_Streams_A_Survey
- Database (MongoDB): https://en.wikipedia.org/wiki/MongoDB
- SON Algorithm: https://www.geeksforgeeks.org/the-son-algorithm-and-map-reduce/
- The assignment was assisted by ChatGPT to certain extent
