import jieba.analyse

from app.agent.state import RailwayAgentState


def extract_keywords(
    state: RailwayAgentState,
) -> dict:
    """
    从用户自然语言问题中抽取关键词。

    输入:
        state["query"]: 用户原始问题

    输出:
        {
            "keywords": [...]
        }
    """

    query = state["query"]

    # 允许提取的词性
    allow_pos = (
        "n",      # 名词
        "nr",     # 人名
        "ns",     # 地名
        "nt",     # 机构名
        "nz",     # 其他专有名词
        "v",      # 动词
        "vn",     # 名动词
        "a",      # 形容词
        "an",     # 名形词
        "eng",    # 英文
        "i",      # 成语
        "l",      # 固定短语
    )

    # 使用 TF-IDF 方式抽取关键词
    keywords = jieba.analyse.extract_tags(
        query,
        allowPOS=allow_pos,
    )

    # 原始问题本身也作为一个检索关键词
    # 后面 Qdrant 语义召回时，完整问题通常很有价值
    keywords.append(query)

    # 去重，同时保留原顺序
    keywords = list(dict.fromkeys(keywords))

    return {
        "keywords": keywords
    }