
# Cassandra Project for Kafka Integration

This project demonstrates how to consume Kafka data streams with PySpark and store the processed data in Apache Cassandra. The goal is to simulate an e-commerce sales system, where sales data is produced to a Kafka topic and consumed to be stored in Cassandra for further analysis.

## Prerequisites

- Apache Kafka
- Apache Cassandra
- Apache Spark
- Python 3.8 or higher

## Installation

1. Clone the repository or download the project files.

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install Apache Kafka, Apache Cassandra, and Apache Spark. Ensure they are running before starting the producer and consumer.

4. Configure the Kafka and Cassandra servers in your environment if necessary (default configurations are set for local setups).

## Files

### `producer.py`

This script generates random sales data using the `Faker` library and sends it to a Kafka topic. Each message represents a sale with products, quantities, and prices.

```bash
python producer.py
```

### `consumer.py`

This script reads from the Kafka topic, processes the sales data using PySpark, and stores the results in Apache Cassandra. It uses Spark’s streaming capabilities to process and insert data in real-time.

```bash
python consumer.py
```

### `requirements.txt`

The required Python libraries are listed in this file. You can install them all with:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure Kafka and Cassandra are up and running locally or on the appropriate server.
2. Run the producer script to simulate sales data being sent to Kafka:

    ```bash
    python producer.py
    ```

3. Run the consumer script to consume data from Kafka and store it in Cassandra:

    ```bash
    python consumer.py
    ```

4. Check Cassandra to verify that the data has been inserted correctly into the specified keyspace and table.
    ```bash
    cqlsh
    ```
    ```sql
    SELECT * FROM atividade_cassandra.vendas;
    ```

## Project Architecture

- **Producer (Kafka)**: Sends generated sales data to the Kafka topic.
- **Consumer (PySpark + Cassandra)**: Consumes data from the Kafka topic, processes it using Spark Structured Streaming, and stores it in Cassandra.

## Notes

- The project assumes you have local installations of Kafka and Cassandra. You might need to configure the connection settings (e.g., `localhost:9092` for Kafka and `localhost` for Cassandra) in case you are using remote servers or different ports.
- The script uses Spark to process and transform the data in real time and then stores it in Cassandra for efficient querying.

## Troubleshooting

- If you encounter issues with Kafka or Cassandra, check the logs for detailed error messages.
- Ensure Kafka is running and the topic exists before running the producer.
- For Cassandra, make sure the keyspace and table are set up correctly before running the consumer.

## License

MIT License.
