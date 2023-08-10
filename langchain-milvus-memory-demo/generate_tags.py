import paddlehub as hub

lac = hub.Module(name="lac")


def get_tags(text):

    # 使用LAC模型进行分词和词性标注
    results = lac.cut(text, use_gpu=False)

    # 提取词性标注结果
    tags = []
    for item in results:
        if item != ' ' and item != '?':
            tags.append(item)
    return tags
