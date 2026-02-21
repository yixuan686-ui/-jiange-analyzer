"""
健哥竞品分析 - Web应用版本
可以直接部署到云平台，生成可分享的网址
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime
import traceback

# 添加src到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 导入工具
try:
    from tools.brand_search_tool import (
        search_brand_comprehensive,
        search_brand_news,
        search_brand_social_media
    )
    from tools.document_parser import parse_document
    from tools.knowledge_manager import import_text_to_knowledge, search_knowledge
except ImportError as e:
    st.error(f"导入工具失败: {e}")
    st.stop()

# 页面配置
st.set_page_config(
    page_title="健哥竞品分析",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
    }
    .report-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.title("📊 健哥竞品分析")
    st.markdown("---")
    
    st.header("功能说明")
    st.markdown("""
    ### 📋 功能列表
    - **品牌分析**：PEST/3C/SWOT/STP多维度分析
    - **文档上传**：支持PDF、Word、Excel等格式
    - **网址解析**：自动提取网页内容
    - **全网搜索**：收集新闻、社交媒体等信息
    - **报告生成**：自动生成专业竞品分析报告
    
    ### 💡 使用提示
    1. 输入品牌名称
    2. （可选）上传相关资料
    3. （可选）提供参考网址
    4. 点击"开始分析"
    5. 下载生成的报告
    """)

# 主标题
st.markdown('<div class="main-title">📊 健哥竞品分析</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">专业的母婴营养品行业品牌竞品分析工具</div>', unsafe_allow_html=True)

# 用户输入区域
st.markdown("---")
st.header("🎯 开始分析")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    brand_name = st.text_input(
        "品牌名称 *",
        placeholder="请输入要分析的品牌名称",
        help="例如：合生元、飞鹤、伊利金领冠等"
    )

with col2:
    time_range = st.selectbox(
        "数据时间范围",
        options=["1周", "1月", "3月", "全部"],
        index=1,
        help="选择搜索数据的时间范围"
    )

with col3:
    analysis_depth = st.selectbox(
        "分析深度",
        options=["快速分析", "标准分析", "深度分析"],
        index=1,
        help="分析深度影响报告的详细程度"
    )

# 文件上传
st.markdown("### 📎 上传资料（可选）")
uploaded_file = st.file_uploader(
    "上传品牌相关资料",
    type=['txt', 'pdf', 'docx', 'xlsx', 'csv', 'json'],
    help="支持上传品牌简介、产品资料、行业报告等文档",
    accept_multiple_files=False
)

# 网址输入
st.markdown("### 🔗 参考网址（可选）")
url_input = st.text_input(
    "输入品牌相关网址",
    placeholder="https://example.com/brand-info",
    help="可以输入品牌官网、新闻报道等网址"
)

# 分析按钮
st.markdown("---")

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    analyze_button = st.button(
        "🚀 开始分析",
        type="primary",
        use_container_width=True,
        disabled=not brand_name
    )

# 分析结果展示区域
if analyze_button and brand_name:
    with st.spinner("正在分析中，请稍候...这可能需要1-3分钟"):
        try:
            st.markdown("---")
            st.header("📊 分析结果")
            
            # 创建进度条
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 步骤1：处理用户上传的资料
            status_text.text("📄 正在处理上传的资料...")
            progress_bar.progress(10)
            
            uploaded_content = ""
            if uploaded_file:
                # 保存文件到临时目录
                temp_dir = "assets"
                os.makedirs(temp_dir, exist_ok=True)
                temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 解析文档
                status_text.text("📄 正在解析文档...")
                parse_result = parse_document(temp_file_path, "auto")
                uploaded_content = parse_result
                
                # 导入知识库
                status_text.text("💾 正在将资料导入知识库...")
                import_text_to_knowledge(
                    parse_result.split("--- 文件内容 ---")[1] if "--- 文件内容 ---" in parse_result else parse_result,
                    f"{brand_name}_uploaded_file"
                )
            
            progress_bar.progress(30)
            
            # 步骤2：处理网址
            if url_input:
                status_text.text("🌐 正在解析网址内容...")
                try:
                    from tools.document_parser import parse_url_content
                    url_content = parse_url_content(url_input)
                    uploaded_content += f"\n\n--- 网址内容 ---\n{url_content}"
                except Exception as e:
                    st.warning(f"网址解析失败: {e}")
            
            progress_bar.progress(40)
            
            # 步骤3：全网搜索
            status_text.text("🔍 正在进行全网搜索...")
            
            search_results = []
            
            try:
                # 综合搜索
                comprehensive_result = search_brand_comprehensive(
                    brand_name,
                    ["news", "website", "social", "industry", "competitor"]
                )
                search_results.append(("综合搜索", comprehensive_result))
                progress_bar.progress(55)
                
                # 新闻搜索
                status_text.text("📰 正在搜索新闻动态...")
                news_result = search_brand_news(brand_name, "1m")
                search_results.append(("新闻搜索", news_result))
                progress_bar.progress(70)
                
                # 社交媒体搜索
                status_text.text("📱 正在搜索社交媒体...")
                social_result = search_brand_social_media(brand_name)
                search_results.append(("社交媒体", social_result))
                progress_bar.progress(85)
                
            except Exception as e:
                st.error(f"搜索过程中出错: {str(e)}")
                progress_bar.progress(85)
            
            # 步骤4：生成报告
            status_text.text("📝 正在生成分析报告...")
            progress_bar.progress(90)
            
            # 构建报告
            report_content = f"""# {brand_name} 竞品分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、执行摘要

本报告通过全网搜索和用户提供的资料，对{brand_name}品牌进行了全面的竞品分析。

## 二、数据来源说明

1. **用户上传资料**: {uploaded_file.name if uploaded_file else '无'}
2. **参考网址**: {url_input if url_input else '无'}
3. **全网搜索**: 新闻动态、官网信息、社交媒体内容等

## 三、搜索结果摘要

"""
            
            # 添加搜索结果
            for search_name, result in search_results:
                report_content += f"\n### {search_name}\n\n"
                report_content += f"{result}\n\n---\n\n"
            
            progress_bar.progress(100)
            status_text.text("✅ 分析完成！")
            
            # 显示报告
            st.markdown('<div class="report-container">', unsafe_allow_html=True)
            st.markdown(report_content)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 下载按钮
            st.markdown("---")
            st.header("💾 下载报告")
            
            # 提供Markdown下载
            st.download_button(
                label="📥 下载Markdown格式报告",
                data=report_content,
                file_name=f"{brand_name}_竞品分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"分析过程中出现错误: {str(e)}")
            st.error(traceback.format_exc())

# 使用说明
st.markdown("---")
with st.expander("❓ 使用说明"):
    st.markdown("""
    ### 如何使用本工具？
    
    1. **输入品牌名称**：在上方输入框中填写要分析的品牌名称（必填）
    2. **上传资料**（可选）：如果手头有品牌相关资料，可以上传
    3. **提供网址**（可选）：如果有相关的网页链接，可以输入
    4. **点击开始分析**：等待1-3分钟，系统会自动生成报告
    5. **下载报告**：分析完成后，可以下载Markdown格式的报告
    
    ### 支持的文件格式
    - 文本文件: .txt, .md
    - 文档文件: .pdf, .docx
    - 数据文件: .xlsx, .csv, .json
    
    ### 分析维度
    - **PEST分析**: 政治、经济、社会、技术环境
    - **3C分析**: 企业、客户、竞争对手
    - **SWOT分析**: 优势、劣势、机会、威胁
    - **STP分析**: 市场细分、目标市场、定位
    
    ### 注意事项
    - 分析过程需要1-3分钟，请耐心等待
    - 搜索结果可能受网络状况影响
    - 建议上传详细资料以获得更准确的分析
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; padding: 2rem;'>
    <p>📊 健哥竞品分析 | 专业的母婴营养品行业品牌竞品分析工具</p>
    <p>Powered by Coze Coding</p>
</div>
""", unsafe_allow_html=True)
