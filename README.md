# 🛒 FluxCart: Kafka Foundational Pipeline

FluxCart is an event-driven data pipeline that simulates real-time e-commerce user activity. This project demonstrates how to decouple data sources from consumers using a distributed message broker.

## 🛠️ Tech Stack
- **Streaming:** Apache Kafka
- **Language:** Python
- **Format:** JSON
- **Concepts:** Producers, Consumers, Consumer Groups, Partitions

## 🚀 Key Features
- **Real-Time Producer:** Simulates 100+ "Order" and "Click" events per second.
- **Scalable Brokering:** Configured Kafka topics with custom partitioning to handle high throughput.
- **Independent Consumers:** Multi-threaded consumers process data for simulated inventory and analytics targets.

## 📊 Pipeline Flow
`FluxCart App` → `Kafka Producer` → `Kafka Broker (Topics)` → `Real-Time Consumers`

## 📦 How to Run
1. Start your Kafka/Zookeeper environment.
2. Run the Producer: `python producer.py`
3. Run the Consumer: `python consumer.py`
