from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
import random

'''连接Milvus'''
connections.connect("default", host="localhost", port="19530")
fields = [
    FieldSchema(name="pk", dtype=DataType.INT64,
                is_primary=True, auto_id=False),
    FieldSchema(name="random", dtype=DataType.DOUBLE),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=8)
]

'''创建集合'''
schema = CollectionSchema(
    fields, "hello_milvus is the simplest demo to introduce the APIs")
hello_milvus = Collection("hello_milvus_2", schema)

'''插入向量变量'''
entities = [
    [i for i in range(10)],  # field pk
    [float(random.randrange(-20, -10)) for _ in range(10)],  # field random
    [[random.random() for _ in range(8)]
     for _ in range(10)],  # field embeddings
]
insert_result = hello_milvus.insert(entities)
hello_milvus.flush()

'''在实体上创建的索引'''
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}
hello_milvus.create_index("embeddings", index)


'''将集合加载到内存中并执行向量相似度搜索'''
hello_milvus.load()
vectors_to_search = entities[-1][-2:]
search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10},
}
result = hello_milvus.search(
    vectors_to_search, "embeddings", search_params, limit=3, output_fields=["random"])
print("resultA:", result)

'''执行向量查询'''
result = hello_milvus.query(
    expr="random > -14", output_fields=["random", "embeddings"])
print("resultB:", result)

'''执行混合搜索'''
result = hello_milvus.search(vectors_to_search, "embeddings", search_params,
                             limit=3, expr="random > -12", output_fields=["random"])
print("resultC:", result)

