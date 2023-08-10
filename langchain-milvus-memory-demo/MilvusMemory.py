# 导入所需模块
from pymilvus import DataType, FieldSchema, CollectionSchema, Collection, connections, utility
from sentence_transformers import SentenceTransformer
import time


# 连接Milvus服务器
connections.connect(alias="default")

# 定义记忆Stream集合schema、创建记忆Stream集合
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="owner", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="timestamp", dtype=DataType.DOUBLE),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,
                dim=384),  # 文本embedding向量
]
schema = CollectionSchema(fields, "memory stream test=11")
collection = Collection("memory_stream_test11", schema)

# 创建索引
index = {
    "index_type": "IVF_SQ8",
    "metric_type": "L2",
    "params": {"nlist": 384},
}
collection.create_index("embedding", index)


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
current_entity_id = 0


def get_embedding_from_language_model(text):
    embedding = model.encode(text)
    return embedding


def get_importance_score_from_language_model(text):
    return 2


def get_current_entity_id():
    global current_entity_id
    current_entity_id = current_entity_id + 1
    return current_entity_id


def insert_memory(text: str, owner: str):
    '''定义插入记忆对象函数'''
    id = get_current_entity_id()  # auto increment id
    timestamp = time.time()

    # 使用语言模型获得文本embedding向量
    embedding = get_embedding_from_language_model(text)
    data = [[id], [text], [owner], [timestamp], [embedding]]
    collection.insert(data)


def compute_relevance(query_text: str, owner: str):
    '''定义计算相关性分数函数'''

    # 搜索表达式
    search_result = search_memory(query_text, owner)
    hits = []
    for hit in search_result:
        memory = {
            "id": hit.entity.id,
            "text": hit.entity.text,
            "timestamp": hit.entity.timestamp,
            "owner": hit.entity.owner
        }
        memory["relevance"] = 1 - hit.distance
        hits.append(memory)

    return hits


def search_memory(query_text: str, owner: str):

    query_embedding = get_embedding_from_language_model(query_text)
    search_params = {"metric_type": "L2", "params": {"nprobe": 30}}

    # 向量搜索表达式
    vector_hits = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=10,
        expr=f"owner=='{owner}'",
        output_fields=["id", "text", "owner", "timestamp"]
    )

    return vector_hits[0]


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


if __name__ == "__main__":

    # 测试代码
    insert_memory("John ate breakfast this morning", "John")
    insert_memory("Mary is planning a party for Valentine's Day", "John")
    insert_memory("John likes to eat BBQ", "John")
    insert_memory("Alan likes to eat TV", "Alan")
    insert_memory("Alan likes to eat Macbook", "Alan")
    insert_memory("John went to the library in the morning", "John")

    # query_text = "What are John's plans for today?"
    query_text = "What does Alan like?"

    collection.load()

    memories = compute_relevance(query_text, "Alan")
    collection.release()
    compute_importance(memories)
    compute_recency(memories)
    normalize_scores(memories)
    print(memories)

    print("Retrieved memories:")
    for memory in sorted(memories, key=lambda m: m["total_score"], reverse=True)[:5]:
        print(memory["text"], ", total score:", memory["total_score"])

    # 清楚原数据
    utility.drop_collection("memory_stream_test11")
