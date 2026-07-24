# 肝硬化患者多重用药与营养不良风险分析

本项目读取 `2022.10.14.营养评分数据统计.xlsx` 的“汇总表”，复现参考论文的主要分析结构，并将结局由肌少症替换为高营养不良风险。

## 分析口径

- 多重用药：出院带药中不同药物种类 `≥5`。
- 高营养不良风险：`RFH-NPT≥2`。
- 肝硬化严重程度：`MELD-Na`。
- MELD-Na 沿用原数据库公式：`MELD + 1.59 × (135 − Na)`，其中 Na 限制在 120–135 mmol/L；程序会核验原值与公式结果的一致性。
- 主分析单元：每位成人患者首次有 RFH-NPT 记录的住院；前端可切换末次记录或全部记录。
- 主模型：以高营养不良风险为结局的 Logistic 回归，核心暴露为多重用药，调整年龄、性别、BMI、病因和 MELD-Na。
- “全部住院记录”敏感性分析使用按患者编号聚类的稳健标准误，以处理同一患者重复住院的观测相关性。
- 连续变量报告中位数（四分位距），采用 Mann-Whitney U 检验；分类变量报告 n（%），采用卡方或 Fisher 精确检验。

药物数量来自自由文本自动解析。`outputs/medication_manual_review.csv` 收录中低置信度记录，论文定稿前必须人工复核。项目没有对姓名进行前端展示，导出的分析数据使用不可逆哈希患者编号。

当前数据缺少统一、可靠的末次随访日期，因此未把 Kaplan-Meier/Cox 生存分析作为主结果。仅有死亡日期不足以正确处理存活者的删失时间。

首次与末次住院口径的效应估计存在差异，提示结果对索引住院选择敏感；论文主结果应预先固定首次记录口径，并将其他口径作为敏感性分析报告。

## 目录

```text
src/
  analysis/       统计检验、基线表、Logistic 回归
  data/           Excel 读取、队列构建、药物解析
  services/       分析编排及文件导出
  app.py          Flask 路由
static/           前端样式与原生 SVG 图表
templates/        页面模板
scripts/          离线分析入口
tests/            自动化测试
outputs/          自动生成的匿名化结果
run.py            Web 启动入口
```

## 运行

```powershell
python -m pip install -r requirements.txt
python scripts/run_analysis.py
python run.py
```

浏览器访问 `http://127.0.0.1:5000`。

## 输出

- `analysis_cohort_anonymized.csv`：匿名化主分析队列。
- `medication_manual_review.csv`：需人工核对的出院带药解析。
- `table_polypharmacy.csv`：按多重用药分组的论文式表格。
- `table_malnutrition.csv`：按营养风险分组的论文式表格。
- `logistic_regression.csv`：未调整及多变量调整结果。
- `dashboard_first/latest/all.json`：三种分析单元口径的完整前端数据。
- `主分析摘要.md`：可直接核对的中文结果与统计解释。
