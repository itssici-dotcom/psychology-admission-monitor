# 心理学调剂监控后端

这是一个用于监控心理学专业硕士调剂信息的后端服务，基于Python和Flask构建。

## 功能特性

- 院校数据管理：存储和提供院校信息
- 智能检索系统：根据规则爬取院校网站并过滤调剂信息
- 检索结果管理：存储、更新和提供检索结果
- 收藏功能：管理用户收藏的院校
- 导出功能：生成并提供Excel格式的检索结果

## 技术栈

- Python 3.8+
- Flask 2.0.1
- SQLAlchemy 1.4.23
- Requests 2.26.0
- BeautifulSoup 4.10.0
- Pandas 1.3.3
- Celery 5.1.2 (可选)

## 安装和运行

1. 克隆项目到本地

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用
   ```bash
   python app.py
   ```

4. 访问API
   - 院校列表：http://localhost:5000/api/schools
   - 执行检索：POST http://localhost:5000/api/search
   - 检索结果：http://localhost:5000/api/search-results
   - 管理收藏：POST http://localhost:5000/api/collection
   - 导出Excel：http://localhost:5000/api/export

## 检索规则

1. 必须同时满足（缺一不可）
   - 必须包含年份：2026
   - 必须包含词（任一即可）：调剂、接收、征集、补录、心理、0454、心理专硕、应用心理

2. 必须排除（任一即弃）
   - 包含以下任一年份：2020、2021、2022、2023、2024、2025

3. 严禁排除
   - 绝对不能因为出现了 学硕 就排除
   - 绝对不能因为出现了 推免、保研、免试 就排除

## 项目结构

```
psychology-admission-backend/
├── app.py              # 主应用文件
├── models.py           # 数据库模型
├── data.py             # 初始化数据
├── search.py           # 检索功能
├── export.py           # 导出功能
├── requirements.txt    # 依赖包
├── .env                # 环境变量
└── README.md           # 项目说明
```

## 注意事项

- 首次运行时会自动初始化院校数据
- 检索功能会爬取目标网站，请注意请求频率，避免被封禁
- 导出的Excel文件会保存在exports目录中

## 前端集成

前端可以通过以下API与后端交互：

1. 获取院校列表：GET /api/schools
2. 执行检索：POST /api/search (可指定school_ids，为空则检索所有)
3. 获取检索结果：GET /api/search-results
4. 管理收藏：POST /api/collection (action: 'add' 或 'remove')
5. 导出Excel：GET /api/export

## 许可证

MIT