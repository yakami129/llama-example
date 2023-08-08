# 导入所需模块
from pymilvus import DataType, FieldSchema, CollectionSchema, Collection, connections, utility
from sentence_transformers import SentenceTransformer
import random
import time
import random
import json


# 连接Milvus服务器
connections.connect(alias="default")

# 定义记忆Stream集合schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR,max_length=2000),
    FieldSchema(name="timestamp", dtype=DataType.DOUBLE),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,
                dim=128),  # 文本embedding向量
]
schema = CollectionSchema(fields, "memory stream")

# 创建记忆Stream集合
collection = Collection("memory_stream", schema)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
def get_embedding_from_language_model(text):
    embedding = model.encode(text)
    return embedding

# 定义插入记忆对象函数


def insert_memory(text):
    id = collection.num_entities  # auto increment id
    timestamp = time.time()

    # 使用语言模型获得文本embedding向量
    embedding = get_embedding_from_language_model(text)

    data = [id, text, timestamp, embedding]
    print("b:",data)
    collection.insert([data])

# 定义计算相关性分数函数


def compute_relevance(query_text):
    query_embedding = get_embedding_from_language_model(query_text)

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    query_expr = f"id in range(0, {collection.num_entities})"

    search_result = collection.search(
        [query_embedding], "embedding", search_params, expr=query_expr)[0]

    hits = search_result.hits
    for hit in hits:
        memory = hit.entity
        memory["relevance"] = 1 - hit.distance  # 余弦相似度

    return hits

# 定义计算重要性分数函数


def compute_importance(memories):
    for memory in memories:
        # 使用语言模型评分文本的重要性
        memory["importance"] = get_importance_score_from_language_model(
            memory["text"])

# 定义计算最近性分数函数


def compute_recency(memories):
    current_time = time.time()
    for memory in memories:
        time_diff = current_time - memory["timestamp"]
        memory["recency"] = 0.99 ** (time_diff / 3600)  # 指数衰减

# 整体归一化得分函数


def normalize_scores(memories):
    max_relevance = max(memory["relevance"] for memory in memories)
    max_importance = max(memory["importance"] for memory in memories)
    max_recency = max(memory["recency"] for memory in memories)

    for memory in memories:
        memory["relevance"] /= max_relevance
        memory["importance"] /= max_importance
        memory["recency"] /= max_recency

        memory["total_score"] = memory["relevance"] + \
            memory["importance"] + memory["recency"]


# 测试代码
insert_memory("John ate breakfast this morning")
insert_memory("Mary is planning a party for Valentine's Day")

query_text = "What are John's plans for today?"

memories = compute_relevance(query_text)
compute_importance(memories)
compute_recency(memories)
normalize_scores(memories)

print("Retrieved memories:")
for memory in sorted(memories, key=lambda m: m["total_score"], reverse=True)[:5]:
    print(memory["text"], ", total score:", memory["total_score"])
