# AI 股票预测平台

这是一个基于 Django 的 AI 股票预测平台，集成了多个 LLM 智能体进行股票分析和预测。

## 功能特点

- **股票数据可视化**：展示股票价格历史、交易量和波动率
- **多智能体分析**：
  - 技术分析智能体：分析价格趋势和技术指标
  - 基本面分析智能体：分析公司财务数据
  - 情绪分析智能体：分析市场情绪
  - 新闻分析智能体：分析相关新闻
- **交易决策系统**：综合各智能体分析结果，提供交易建议

## 技术栈

- Django 5.2
- Python 3.11
- Pandas
- Chart.js
- Bootstrap 5

## 项目结构

```
Money/
├── companies/          # 主要应用
│   ├── models.py      # 数据模型
│   ├── views.py       # 视图函数
│   ├── urls.py        # URL 路由
│   └── templates/     # 模板文件
├── trading_agents.py  # 交易智能体
├── main.py           # 数据获取脚本
└── Moneytest/        # 项目配置
```

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Money.git
cd Money
```

2. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行数据库迁移：
```bash
python manage.py migrate
```

5. 启动开发服务器：
```bash
python manage.py runserver
```

## 使用说明

1. 访问主页：http://localhost:8000/
2. 查看股票仪表盘：http://localhost:8000/stocks/dashboard/
3. 查看交易预测：http://localhost:8000/stocks/predictions/

## 待完成功能

- [ ] 集成 LLM API 密钥
- [ ] 实现实时数据更新
- [ ] 添加更多技术指标
- [ ] 优化预测算法
- [ ] 添加用户认证系统

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 