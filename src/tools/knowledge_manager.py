"""
知识库管理工具
用于管理用户上传的文档资料，支持导入和搜索
"""

from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context
from typing import Literal, Optional
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType, ChunkConfig


@tool
def import_text_to_knowledge(
    text: str,
    document_name: str = "用户上传文档",
    runtime: ToolRuntime = None
) -> str:
    """
    将文本内容导入到知识库，便于后续分析和引用
    
    Args:
        text: 要导入的文本内容
        document_name: 文档名称（用于标识）
        runtime: 工具运行时上下文
    
    Returns:
        导入结果，包含文档ID和状态
    """
    try:
        ctx = runtime.context if runtime else new_context(method="import_text")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=text,
            metadata={"document_name": document_name}
        )
        
        response = client.add_documents(
            documents=[doc],
            table_name="brand_analysis_documents"
        )
        
        if response.code == 0:
            return f"文档导入成功\n文档名称: {document_name}\n文档ID: {response.doc_ids[0] if response.doc_ids else 'N/A'}"
        else:
            return f"文档导入失败: {response.msg}"
            
    except Exception as e:
        return f"文档导入异常: {str(e)}"


@tool
def search_knowledge(
    query: str,
    top_k: int = 5,
    min_score: float = 0.0,
    runtime: ToolRuntime = None
) -> str:
    """
    在知识库中搜索相关内容
    
    Args:
        query: 搜索查询文本
        top_k: 返回结果数量
        min_score: 最小相似度阈值（0.0-1.0）
        runtime: 工具运行时上下文
    
    Returns:
        搜索结果，包含相关内容和相似度分数
    """
    try:
        ctx = runtime.context if runtime else new_context(method="search_knowledge")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        response = client.search(
            query=query,
            table_names=None,  # 搜索所有数据集
            top_k=top_k,
            min_score=min_score
        )
        
        if response.code != 0:
            return f"知识库搜索失败: {response.msg}"
        
        if not response.chunks:
            return f"未找到与\"{query}\"相关的内容"
        
        results = [f"搜索查询: {query}", f"找到 {len(response.chunks)} 条相关内容\n", "--- 搜索结果 ---\n"]
        
        for i, chunk in enumerate(response.chunks, 1):
            results.append(f"\n结果 {i} (相似度: {chunk.score:.4f}):")
            results.append(chunk.content)
            results.append(f"来源文档ID: {chunk.doc_id}")
        
        return '\n'.join(results)
        
    except Exception as e:
        return f"知识库搜索异常: {str(e)}"


@tool
def import_url_to_knowledge(
    url: str,
    document_name: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    将网页URL内容导入到知识库
    
    Args:
        url: 网页URL
        document_name: 文档名称（可选，默认使用URL）
        runtime: 工具运行时上下文
    
    Returns:
        导入结果
    """
    try:
        ctx = runtime.context if runtime else new_context(method="import_url")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        if document_name is None:
            document_name = url
        
        doc = KnowledgeDocument(
            source=DataSourceType.URL,
            url=url,
            metadata={"document_name": document_name}
        )
        
        response = client.add_documents(
            documents=[doc],
            table_name="brand_analysis_documents"
        )
        
        if response.code == 0:
            return f"网页导入成功\n网页URL: {url}\n文档名称: {document_name}\n文档ID: {response.doc_ids[0] if response.doc_ids else 'N/A'}"
        else:
            return f"网页导入失败: {response.msg}"
            
    except Exception as e:
        return f"网页导入异常: {str(e)}"


@tool
def clear_analysis_knowledge(
    runtime: ToolRuntime = None
) -> str:
    """
    清空品牌分析知识库（用于重新导入资料）
    
    Args:
        runtime: 工具运行时上下文
    
    Returns:
        清空结果
    """
    try:
        # 注意：知识库SDK可能没有直接清空的API
        # 这里我们提供一个提示信息
        return "知识库清空功能：当前版本不支持直接清空知识库。建议为每个分析会话创建新的文档ID，或使用不同的数据集名称。"
    except Exception as e:
        return f"清空操作异常: {str(e)}"
