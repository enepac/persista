from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128)
]
schema = CollectionSchema(fields, "Test Collection")

# Create collection
collection = Collection("test_collection", schema)

# Insert data
import random
data = [
    [i for i in range(10)],  # IDs
    [[random.random() for _ in range(128)] for _ in range(10)]  # Embeddings
]
collection.insert(data)

# Create an index on the vector field
index_params = {
    "index_type": "IVF_FLAT",  # Inverted File with Flat
    "metric_type": "L2",       # Euclidean distance
    "params": {"nlist": 128}   # Number of clusters
}
collection.create_index("embedding", index_params)

# Load the collection into memory
collection.load()

# Verify data
results = collection.query(expr="id > 0", output_fields=["id", "embedding"])
print(results)