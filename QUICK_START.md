# 🚀 快速获得可分享的网址

## 最快方案（推荐新手）⭐⭐⭐

### 5分钟获得免费网址（Railway.app）

#### 步骤：
1. 访问 https://railway.app，用GitHub账号登录
2. 将代码上传到GitHub
3. 在Railway创建新项目，选择你的GitHub仓库
4. 设置启动命令：`streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0`
5. 添加环境变量：
   - `COZE_WORKLOAD_IDENTITY_API_KEY`: 你的API密钥
   - `COZE_INTEGRATION_MODEL_BASE_URL`: 你的模型API地址
6. 点击Deploy，等待3-5分钟
7. 完成！获得可分享的网址

### 详细说明
查看 `DEPLOYMENT_GUIDE.md` 文件，里面有详细的部署步骤和多种方案。

---

## 🎯 本地快速测试

如果你想先本地测试，运行：

```bash
# Linux/Mac
bash start_web.sh

# Windows
python web_app.py
```

然后访问：http://localhost:8501

---

## 📁 文件说明

```
workspace/projects/
├── web_app.py              # Web应用主程序 ⭐
├── Dockerfile.web          # Docker配置
├── start_web.sh            # 快速启动脚本
├── requirements_web.txt    # Web应用依赖
├── requirements.txt        # 完整依赖
├── DEPLOYMENT_GUIDE.md     # 详细部署指南
├── QUICK_START.md          # 本文件
├── src/                    # 源代码
│   ├── agents/
│   ├── tools/
│   └── storage/
├── config/
│   └── agent_llm_config.json
└── assets/                 # 上传文件存放目录
```

---

## 🔑 获取API密钥

如果你还没有API密钥，需要先获取：

1. 访问 [Coze控制台](https://www.coze.cn)
2. 创建应用或使用已有应用
3. 在应用设置中获取 API Key 和 Base URL

---

## ✨ 功能特点

- ✅ 文件上传（支持PDF、Word、Excel等）
- ✅ 网址解析
- ✅ 全网搜索
- ✅ PEST/3C/SWOT/STP多维度分析
- ✅ 自动生成专业报告
- ✅ 报告下载（Markdown格式）

---

## 💡 三种部署方案对比

| 方案 | 难度 | 时间 | 费用 | HTTPS | 推荐 |
|------|------|------|------|-------|------|
| Railway.app | ⭐ | 5分钟 | 免费（有额度） | ✅ 自动 | ⭐⭐⭐ |
| Docker Compose | ⭐⭐ | 10分钟 | 需要服务器 | 需配置 | ⭐⭐ |
| 云函数 | ⭐⭐⭐ | 15分钟 | 按量付费 | ✅ 自动 | ⭐ |

---

## 🌐 部署后的网址示例

- Railway: `https://jiange-analyzer.up.railway.app`
- 自定义域名: `https://analyzer.yourdomain.com`

---

## 📞 需要帮助？

查看 `DEPLOYMENT_GUIDE.md` 里面有详细的：
- 部署步骤
- 常见问题
- 故障排查

---

## 🎉 开始吧！

选择 **Railway.app** 方案，5分钟后你就能获得一个可以分享给朋友的网址了！
