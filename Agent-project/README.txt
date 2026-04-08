智能扫地机器人 AI 客服系统
==============================

基于 LangChain Agent + RAG 的智能客服，使用阿里云通义千问模型，Streamlit 作为前端界面。


项目结构
--------
Agent-project/
├── app.py                        # Streamlit 前端主程序，Web 入口
├── requirements.txt              # 依赖列表
├── md5.text                      # 已处理知识库文件的 MD5 记录（去重用）
│
├── agent/
│   ├── react_agent.py            # ReactAgent 核心类，封装 create_agent 调用
│   └── tools/
│       ├── agent_tools.py        # 所有 @tool 工具定义（7个工具）
│       └── middleware.py         # 3个中间件：工具监控、模型前日志、动态提示词切换
│
├── rag/
│   ├── rag_service.py            # RAG 总结服务，LCEL chain 实现
│   └── vector_store.py           # ChromaDB 向量存储，含文档加载/MD5去重
│
├── model/
│   └── factory.py                # 模型工厂，提供 chat_model 和 embedding_model
│
├── utils/
│   ├── config_handler.py         # YAML 配置加载
│   ├── prompt_loader.py          # 提示词文件加载
│   ├── file_handler.py           # 文件工具：MD5计算、目录遍历、PDF/TXT加载
│   ├── logger_handler.py         # 日志工具，双输出（控制台+文件）
│   └── path_tool.py              # 路径工具，统一提供绝对路径
│
├── config/
│   ├── rag.yml                   # 模型配置（chat/embedding 模型名）
│   ├── chroma.yml                # 向量库配置（分片、检索参数等）
│   ├── prompt.yml                # 提示词文件路径配置
│   └── agent.yml                 # Agent 配置（外部数据路径）
│
├── prompts/
│   ├── main_prompt.txt           # 主系统提示词（ReAct 客服角色）
│   ├── rag_summarize.txt         # RAG 总结提示词模板
│   └── report_prompt.txt         # 报告生成提示词
│
└── data/
    ├── 扫地机器人100问.pdf
    ├── 扫地机器人100问2.txt
    ├── 扫拖一体机器人100问.txt
    ├── 维护保养.txt
    ├── 故障排除.txt
    ├── 选购指南.txt
    └── external/
        └── records.csv           # 用户使用记录外部数据


环境准备
--------
1. 安装依赖：
   pip install -r requirements.txt

2. 配置阿里云 DashScope API Key（通义千问）：
   Windows:
     set DASHSCOPE_API_KEY=your_api_key



加载知识库（首次运行）
----------------------
将知识文档（txt/pdf）放入 data/ 目录，然后运行：

   python -m rag.vector_store

文档会被分片向量化存入 ChromaDB，已处理文件通过 MD5 去重，不会重复入库。


启动应用
--------
   streamlit run app.py

浏览器访问 http://localhost:8501


架构说明
--------
- ReAct Agent：模型先思考需要调用哪个工具，调用后再判断是否完成任务，循环直至完成
- RAG 检索：用户提问时从向量库检索相关知识，结合上下文让模型回答
- 动态提示词切换：调用 fill_context_for_report 工具后，中间件自动将系统提示词切换为报告写手模式
- 流式输出：逐字打印，提升交互体验
- MD5 去重：知识库文件入库前计算 MD5，避免重复向量化


模块说明
--------
app.py               Streamlit 聊天界面，session 状态管理，流式逐字输出
react_agent.py       封装 create_agent，ReAct 流式推理
agent_tools.py       7个工具：rag_summarize / get_weather / get_user_location /
                     get_user_id / get_current_month / fetch_external_data /
                     fill_context_for_report
middleware.py        工具调用监控日志、模型调用前日志、动态提示词切换
rag_service.py       LCEL chain：PromptTemplate -> model -> StrOutputParser
vector_store.py      ChromaDB 存取，文档分片，MD5去重防重复入库
factory.py           工厂模式，提供 ChatTongyi 和 DashScopeEmbeddings 实例
config_handler.py    加载4个 YAML，暴露 rag_conf/chroma_conf/prompt_conf/agent_conf
