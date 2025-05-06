from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode, lit
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, IntegerType, FloatType, TimestampType

spark = SparkSession.builder \
    .appName("VendasEcommerceParaCassandra") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0") \
    .config("spark.cassandra.connection.host", "localhost") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

kafka_servers = "localhost:9092"
topic = "vendas_ecommerce"
keyspace = "atividade_cassandra"
tabela = "vendas"

schema = StructType([
    StructField("id_ordem", StringType()),
    StructField("documento_cliente", StringType()),
    StructField("produtos_comprados", ArrayType(StructType([
        StructField("nome_produto", StringType()),
        StructField("quantidade", IntegerType()),
        StructField("preco_unitario", FloatType())
    ]))),
    StructField("data_hora_venda", TimestampType())
])

def salvar_no_cassandra(batch_df, batch_id):
    batch_df = batch_df.filter(col("data_hora_venda").isNotNull())
    dados_cassandra = batch_df.withColumn("valor_total", col("quantidade") * col("preco_unitario")) \
        .select(
            col("documento_cliente").alias("cliente_id"),
            col("id_ordem").alias("produto_id"),
            col("data_hora_venda").alias("data_compra"),
            col("produto"),
            col("quantidade"),
            col("preco_unitario"),
            col("valor_total"),
            lit("Cartão").alias("forma_pagamento")
        )
    try:
        dados_cassandra.write \
            .format("org.apache.spark.sql.cassandra") \
            .options(table=tabela, keyspace=keyspace) \
            .mode("append") \
            .save()
    except Exception as e:
        print(f"Erro ao salvar no Cassandra: {str(e)}")

stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_servers) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

dados = stream.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

dados_produtos = dados.select(
    "id_ordem",
    "documento_cliente",
    "data_hora_venda",
    explode("produtos_comprados").alias("produto")
).select(
    "id_ordem",
    "documento_cliente",
    "data_hora_venda",
    col("produto.nome_produto").alias("produto"),
    col("produto.quantidade").alias("quantidade"),
    col("produto.preco_unitario").alias("preco_unitario")
)

query = dados_produtos.writeStream \
    .foreachBatch(salvar_no_cassandra) \
    .outputMode("update") \
    .start()

print("Iniciando o consumo de dados...")
query.awaitTermination()

