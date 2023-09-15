from neo4j import GraphDatabase

# 定义 Neo4j 数据库连接类
class Neo4jConnection:

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

# 创建节点
def create_node(tx, node_type, properties):
    query = f"CREATE (n:{node_type} $properties)"
    tx.run(query, properties=properties)

# 查询节点
def find_nodes(tx, node_type, properties):
    query = f"MATCH (n:{node_type} {properties}) RETURN n"
    result = tx.run(query)
    return [record["n"] for record in result]

# 更新节点
def update_node(tx, node_id, properties):
    query = f"MATCH (n) WHERE ID(n) = {node_id} SET n += $properties"
    tx.run(query, properties=properties)

# 删除节点
def delete_node(tx, node_id):
    query = f"MATCH (n) WHERE ID(n) = {node_id} DELETE n"
    tx.run(query)

# 创建关系
def create_relationship(tx, node_id_1, node_id_2, relation_type, properties=None):
    query = f"MATCH (a), (b) WHERE ID(a) = {node_id_1} AND ID(b) = {node_id_2} CREATE (a)-[r:{relation_type} $properties]->(b)"
    tx.run(query, properties=properties)

# 使用连接执行操作
uri = "bolt://localhost:7687"  # 请替换成您的 Neo4j 数据库的 URI
user = "neo4j"  # 请替换成您的 Neo4j 数据库用户名
password = "your_password"  # 请替换成您的 Neo4j 数据库密码

connection = Neo4jConnection(uri, user, password)

with connection._driver.session() as session:
    # 创建节点
    user_properties = {
        "userID": "3",
        "name": "Eve",
        "gender": "Female",
        "age": 28,
        "occupation": "Designer",
        "labels": ["Art", "Design"]
    }
    session.write_transaction(create_node, "User", user_properties)

    # 查询节点
    search_properties = {"userID": "3"}
    result = session.read_transaction(find_nodes, "User", search_properties)
    print("Found nodes:")
    for record in result:
        print(record)

    # 更新节点
    user_id_to_update = 3
    update_properties = {"name": "Eva", "age": 29}
    session.write_transaction(update_node, user_id_to_update, update_properties)

    # 删除节点
    user_id_to_delete = 3
    session.write_transaction(delete_node, user_id_to_delete)

# 关闭连接
connection.close()
