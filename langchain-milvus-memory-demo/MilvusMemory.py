# 导入所需模块
from pymilvus import DataType, FieldSchema, CollectionSchema, Collection, connections, utility
from sentence_transformers import SentenceTransformer
from generate_tags import get_tags
import random
import time
import random
import json


# 连接Milvus服务器
connections.connect(alias="default")

# 定义记忆Stream集合schema、创建记忆Stream集合
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="tags", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="timestamp", dtype=DataType.DOUBLE),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,
                dim=384),  # 文本embedding向量
]
schema = CollectionSchema(fields, "memory stream test=8")
collection = Collection("memory_stream_test08", schema)

# 创建索引
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}
collection.create_index("embedding", index)
collection.create_index("tags")


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def get_embedding_from_language_model(text):
    embedding = model.encode(text)
    return embedding


def get_importance_score_from_language_model(text):
    return 2


def insert_memory(text):
    '''定义插入记忆对象函数'''
    id = collection.num_entities  # auto increment id
    tags = json.dumps(get_tags(text))         # generate tages
    timestamp = time.time()
    print("g:", tags)

    # 使用语言模型获得文本embedding向量
    embedding = get_embedding_from_language_model(text)
    data = [[id], [text], [tags], [timestamp], [embedding]]
    collection.insert(data)


def compute_relevance(query_text):
    '''定义计算相关性分数函数'''

    # 搜索表达式
    search_result = search_memory(query_text)
    hits = []
    for hit in search_result:
        memory = {"text": hit.entity.text, "timestamp": hit.entity.timestamp}
        memory["relevance"] = hit.distance
        hits.append(memory)

    return hits


def search_memory(query_text):

    query_embedding = get_embedding_from_language_model(query_text)
    query_tags = get_tags(query_text)
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    # 向量搜索表达式
    vector_hits = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=100,
        output_fields=["id", "text", "timestamp"]
    )[0]

    # 标签搜索
    tag_hits = collection.search(
        data=[query_tags],
        anns_field="tags",
        param=search_params,
        limit=100,
        output_fields=["id", "text", "timestamp"]
    )[0]

    # 合并搜索参数
    merged_hits = []
    added_ids = set()
    for hit in vector_hits:
        if hit.id not in added_ids:
            added_ids.add(hit.id)
            merged_hits.append(hit)
    for hit in tag_hits:
        if hit.id not in added_ids:
            added_ids.add(hit.id)
            merged_hits.append(hit)


def compute_importance(memories):
    '''定义计算重要性分数函数'''
    for memory in memories:
        # 使用语言模型评分文本的重要性
        memory["importance"] = get_importance_score_from_language_model(
            memory["text"])


def compute_recency(memories):
    '''定义计算最近性分数函数'''
    current_time = time.time()
    for memory in memories:
        time_diff = current_time - memory["timestamp"]
        memory["recency"] = 0.99 ** (time_diff / 3600)  # 指数衰减


def normalize_scores(memories):
    for memory in memories:
        memory["total_score"] = memory["relevance"] + \
            memory["importance"] + memory["recency"]


# 测试代码
insert_memory("John ate breakfast this morning")
insert_memory("Mary is planning a party for Valentine's Day")
insert_memory("John likes to eat BBQ")
insert_memory("John likes to eat TV")
insert_memory("John likes to eat Macbook")
insert_memory("John went to the library in the morning")

# query_text = "What are John's plans for today?"
query_text = "What does John?"

collection.load()
memories = compute_relevance(query_text)
collection.release()
compute_importance(memories)
compute_recency(memories)
normalize_scores(memories)
print(memories)

print("Retrieved memories:")
for memory in sorted(memories, key=lambda m: m["total_score"], reverse=True)[:5]:
    print(memory["text"], ", total score:", memory["total_score"])

# 清楚原数据
utility.drop_collection("memory_stream_test08")
