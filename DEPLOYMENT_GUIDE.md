# 🚀 健哥竞品分析 - 部署指南

## 📋 前言

本指南将帮助你将"健哥竞品分析"部署到云平台，生成一个可以分享给朋友的网址。

## 🎯 推荐的部署平台

### 方案1：Docker Compose（最简单）⭐推荐
**适合人群**：有服务器或VPS的用户
**优点**：配置简单，一键部署
**预计时间**：10分钟

### 方案2：Railway.app（最快速）⭐⭐推荐
**适合人群**：不想自己管理服务器的用户
**优点**：免费额度，自动HTTPS，一键部署
**预计时间**：5分钟

### 方案3：腾讯云函数/阿里云函数
**适合人群**：需要按量付费的用户
**优点**：按需付费，无需维护
**预计时间**：15分钟

---

## 📦 方案1：Docker Compose 部署

### 步骤1：准备服务器
你需要一台云服务器（阿里云、腾讯云、华为云等），推荐配置：
- CPU: 2核
- 内存: 4GB
- 系统: Ubuntu 20.04 或 CentOS 7+

### 步骤2：安装Docker和Docker Compose
```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 步骤3：上传代码
将项目文件上传到服务器，例如上传到 `/opt/jiange-analyzer` 目录

### 步骤4：创建docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    container_name: jiange-analyzer
    ports:
      - "8501:8501"
    environment:
      - COZE_WORKLOAD_IDENTITY_API_KEY=${COZE_WORKLOAD_IDENTITY_API_KEY}
      - COZE_INTEGRATION_MODEL_BASE_URL=${COZE_INTEGRATION_MODEL_BASE_URL}
    volumes:
      - ./assets:/app/assets
    restart: unless-stopped
```

### 步骤5：配置环境变量
创建 `.env` 文件：
```bash
COZE_WORKLOAD_IDENTITY_API_KEY=你的API密钥
COZE_INTEGRATION_MODEL_BASE_URL=你的模型API地址
```

### 步骤6：启动服务
```bash
docker-compose up -d --build
```

### 步骤7：配置域名（可选）
配置Nginx反向代理，添加SSL证书，获得HTTPS访问：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 完成！
访问 `http://你的服务器IP:8501` 或 `https://你的域名.com`

---

## 🚀 方案2：Railway.app 部署（推荐新手）

### 步骤1：注册账号
1. 访问 https://railway.app
2. 使用GitHub账号登录

### 步骤2：创建新项目
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"

### 步骤3：连接代码仓库
1. 将代码上传到GitHub（或使用Git）
2. 在Railway中选择你的仓库

### 步骤4：配置项目
1. Railway会自动检测Python项目
2. 设置启动命令：`streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0`
3. 设置环境变量（Variables）：
   - `COZE_WORKLOAD_IDENTITY_API_KEY`: 你的API密钥
   - `COZE_INTEGRATION_MODEL_BASE_URL`: 你的模型API地址

### 步骤5：部署
点击 "Deploy" 按钮，等待3-5分钟

### 完成！
Railway会自动生成一个访问网址，例如：`https://jiange-analyzer.up.railway.app`

---

## ☁️ 方案3：腾讯云/阿里云函数

### 步骤1：准备代码
将代码打包成ZIP文件

### 步骤2：创建函数
在云平台创建HTTP触发器函数

### 步骤3：配置环境
设置内存：512MB
设置超时：60秒
配置环境变量

### 步骤4：部署
上传ZIP文件，部署函数

### 完成！
获得函数访问网址

---

## 🔑 获取API密钥

### 方式1：使用Coze平台
1. 访问 Coze 控制台
2. 创建应用或使用已有应用
3. 获取 API Key 和 Base URL

### 方式2：使用其他LLM服务
- **豆包**: https://www.volcengine.com/
- **文心一言**: https://cloud.baidu.com/
- **通义千问**: https://tongyi.aliyun.com/

---

## 🌐 获得HTTPS域名

### 方式1：使用Railway.app
自动提供HTTPS域名，无需额外配置

### 方式2：使用Cloudflare（免费CDN）
1. 注册 Cloudflare 账号
2. 添加你的域名
3. 配置DNS指向你的服务器IP
4. 启用SSL/TLS加密

### 方式3：使用Let's Encrypt（免费SSL）
```bash
# 安装Certbot
sudo apt-get install certbot

# 获取SSL证书
sudo certbot certonly --standalone -d your-domain.com

# 配置Nginx使用证书
```

---

## 📝 分享网址

### 方法1：直接分享
部署成功后，直接将网址发给朋友即可

### 方法2：使用短网址服务
- https://dwz.cn/（百度短网址）
- https://t.cn/（新浪短网址）

### 方法3：使用二维码生成器
将网址生成二维码，朋友扫码即可访问

---

## 🔧 常见问题

### Q1: 部署后无法访问？
**A**: 检查防火墙设置，确保8501端口开放

### Q2: 分析时出错？
**A**: 检查API密钥是否正确，检查网络连接

### Q3: 如何更新代码？
**A**: 重新部署即可：
- Docker: `docker-compose up -d --build`
- Railway: 推送代码到GitHub，自动部署

### Q4: 如何查看日志？
**A**:
- Docker: `docker-compose logs -f`
- Railway: 在控制台查看Logs

---

## 💡 使用建议

1. **推荐使用Railway.app**：最简单，免费额度够用
2. **设置域名**：使用自定义域名更专业
3. **定期备份**：定期备份重要数据
4. **监控使用**：关注访问量和资源使用

---

## 📞 技术支持

如遇到问题，可以：
1. 查看日志文件
2. 检查配置是否正确
3. 确认API密钥有效
4. 联系云平台客服

---

## 🎉 开始部署吧！

选择一个方案，按照步骤操作，几分钟后你就能获得一个可以分享的网址了！

祝你使用愉快！🚀
