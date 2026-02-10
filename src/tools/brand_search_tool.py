"""
品牌信息检索工具
用于搜索品牌的新闻、官网、社交媒体等多维度信息
"""

from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from typing import Literal
import json


@tool
def search_brand_comprehensive(
    brand_name: str,
    search_dimensions: list[Literal["news", "website", "social", "industry", "competitor"]] = ["news", "website", "social"],
    runtime: ToolRuntime = None
) -> str:
    """
    全网搜索品牌的多维度信息，包括新闻、官网、社交媒体、行业信息和竞品信息
    
    Args:
        brand_name: 品牌名称
        search_dimensions: 搜索维度，可选值：
            - news: 新闻源
            - website: 品牌官网
            - social: 社交媒体（抖音、小红书等）
            - industry: 行业信息
            - competitor: 竞品信息
        runtime: 工具运行时上下文
    
    Returns:
        搜索结果的JSON格式字符串，包含各个维度的信息汇总
    """
    ctx = runtime.context if runtime else new_context(method="brand_search")
    client = SearchClient(ctx=ctx)
    
    results = {
        "brand_name": brand_name,
        "search_dimensions": search_dimensions,
        "data": {}
    }
    
    # 构建搜索查询映射
    search_queries = {
        "news": f"{brand_name} 新闻 动态",
        "website": f"{brand_name} 官网",
        "social": f"{brand_name} 抖音 小红书",
        "industry": f"{brand_name} 母婴营养品 行业",
        "competitor": f"{brand_name} 竞品 竞争对手"
    }
    
    # 执行搜索
    for dimension in search_dimensions:
        if dimension not in search_queries:
            continue
        
        query = search_queries[dimension]
        try:
            response = client.web_search_with_summary(
                query=query,
                count=10
            )
            
            dimension_results = {
                "query": query,
                "summary": response.summary if response.summary else "",
                "results": []
            }
            
            for item in response.web_items:
                dimension_results["results"].append({
                    "title": item.title,
                    "url": item.url,
                    "site_name": item.site_name,
                    "snippet": item.snippet,
                    "publish_time": item.publish_time,
                    "authority": item.auth_info_des
                })
            
            results["data"][dimension] = dimension_results
            
        except Exception as e:
            results["data"][dimension] = {
                "error": f"搜索失败: {str(e)}",
                "query": query,
                "results": []
            }
    
    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def search_brand_news(
    brand_name: str,
    time_range: str = "1m",
    runtime: ToolRuntime = None
) -> str:
    """
    搜索品牌的最新新闻动态
    
    Args:
        brand_name: 品牌名称
        time_range: 时间范围，例如 "1d"（1天）、"1w"（1周）、"1m"（1月）
        runtime: 工具运行时上下文
    
    Returns:
        新闻搜索结果的JSON格式字符串
    """
    ctx = runtime.context if runtime else new_context(method="brand_news_search")
    client = SearchClient(ctx=ctx)
    
    try:
        response = client.search(
            query=f"{brand_name} 新闻 动态 资讯",
            search_type="web",
            count=15,
            time_range=time_range,
            need_summary=True
        )
        
        results = {
            "brand_name": brand_name,
            "time_range": time_range,
            "summary": response.summary if response.summary else "",
            "news_count": len(response.web_items),
            "news": []
        }
        
        for item in response.web_items:
            results["news"].append({
                "title": item.title,
                "url": item.url,
                "source": item.site_name,
                "snippet": item.snippet,
                "publish_time": item.publish_time
            })
        
        return json.dumps(results, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"新闻搜索失败: {str(e)}"}, ensure_ascii=False)


@tool
def search_brand_social_media(
    brand_name: str,
    platforms: str = "抖音,小红书,微博",
    runtime: ToolRuntime = None
) -> str:
    """
    搜索品牌在社交媒体平台的相关内容
    
    Args:
        brand_name: 品牌名称
        platforms: 社交媒体平台名称，多个平台用逗号分隔
        runtime: 工具运行时上下文
    
    Returns:
        社交媒体内容的JSON格式字符串
    """
    ctx = runtime.context if runtime else new_context(method="brand_social_search")
    client = SearchClient(ctx=ctx)
    
    try:
        response = client.web_search_with_summary(
            query=f"{brand_name} {platforms}",
            count=12
        )
        
        results = {
            "brand_name": brand_name,
            "platforms": platforms,
            "summary": response.summary if response.summary else "",
            "content_count": len(response.web_items),
            "contents": []
        }
        
        for item in response.web_items:
            results["contents"].append({
                "title": item.title,
                "url": item.url,
                "platform": item.site_name,
                "snippet": item.snippet,
                "publish_time": item.publish_time
            })
        
        return json.dumps(results, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"社交媒体搜索失败: {str(e)}"}, ensure_ascii=False)
