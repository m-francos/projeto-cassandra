
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

## Set Up Apache Cassandra

Before running the consumer script, you need to create the **keyspace** and **table** in Cassandra:

1. Start Cassandra:
   ```bash
   cassandra
   ```

2. Open the Cassandra shell:
   ```bash
   cqlsh
   ```

3. Create the keyspace:
   ```sql
   CREATE KEYSPACE IF NOT EXISTS atividade_cassandra
   WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
   ```

4. Use the keyspace:
   ```sql
   USE atividade_cassandra;
   ```

5. Create the table:
   ```sql
   CREATE TABLE IF NOT EXISTS vendas (
       cliente_id TEXT,
       data_compra DATE,
       hora_compra TIME,
       produto TEXT,
       quantidade INT,
       preco_unitario FLOAT,
       valor_total FLOAT,
       forma_pagamento TEXT,
       PRIMARY KEY ((cliente_id), data_compra, hora_compra)
   );
   ```

6. To verify that everything is working:
   ```sql
   SELECT * FROM atividade_cassandra.vendas;
   ```

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

1. Ensure Kafka and Cassandra are up and running.
2. Run the producer script to simulate sales data being sent to Kafka:

    ```bash
    python producer.py
    ```

3. Run the consumer script to consume data from Kafka and store it in Cassandra:

    ```bash
    python consumer.py
    ```

4. Open `cqlsh` and check if the data is being saved:
    ```bash
    cqlsh
    ```
    ```sql
    SELECT * FROM atividade_cassandra.vendas;
    ```

## Project Overview

- **Producer**: Sends fake sales data to Kafka.
- **Kafka Topic**: Receives the data in real-time.
- **Consumer (with Spark)**: Reads the data and saves it into Cassandra.
- **Cassandra**: Stores the data for later use or analysis.

## Notes

- This project uses default settings like `localhost:9092` for Kafka and `localhost` for Cassandra. If you're running them on another machine or port, update the scripts.
- The data is generated randomly with `Faker`, so it’s good for testing and learning.
- The Spark consumer works in streaming mode — it keeps running and listening to new data coming from Kafka.

## Troubleshooting

- If something doesn’t work, check if all services (Kafka, Spark, Cassandra) are running.
- Make sure the topic exists in Kafka before starting the producer.
- Check if you created the Cassandra keyspace and table correctly.

## License

MIT License.
