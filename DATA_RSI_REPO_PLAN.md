# DataRSI 仓库建立与规划记录 (DATA_RSI_REPO_PLAN)

本文件记录了基于 `DataEvolver` 工程基础设施建立面向 ICASSP 2027 论文的独立公开研究仓库 `DataRSI` 的完整规划与复用清单。

---

## 1. 核心定位与背景关系

- **DataEvolver**：我们此前开发并持续维护的实际工程项目，包含更广泛的合成数据构建基础设施（T2I/T2V 生成管道、3D 渲染、VLM 审查闭环、场景工具与世界模型等）。保持原貌，独立维护。
- **DataRSI**：ICASSP 2027 论文中的研究框架与方法名称，研究对象为明确的**有界数据修订协议（bounded supervision revision protocol）**。
- **关系表述**：
  > “DataRSI is the research framework introduced in our ICASSP 2027 work. It builds on the synthetic-data construction infrastructure developed in DataEvolver and formalizes failure-driven dataset evolution as an auditable bounded revision process.”

---

## 2. 复用与新增详细清单

### A. 原 DataEvolver 中被复用的内容
1. **视觉呈现资产**：
   - 论文 Figure 1 矢量方法图（渲染为 `assets/datarsi_framework.png`）。
   - 论文 Figure 2 定性结果对比图（`assets/qualitative_results.png`）。
   - 论文 Figure 3 核心 3-seed 误差棒柱状图（`assets/matched_budget_results.png`）。
2. **核心实验数据与裁决底册**：
   - `same_budget_multiseed_admission.json`：多种子准入裁决数据。
   - `same_budget_multiseed_contrasts.csv`：配对差值统计。
   - `same_budget_multiseed_summary.csv`：均值与样本标准差统计。
   - `same_budget_rotation_calibration.json`：诊断与几何评估器的校准证据（$\rho=0.779$）。
   - `table1_full_metrics.json`：历史检查点适配指标（Base, fal, Data-Ev, DataRSI）。
3. **结构化生成空间**：
   - 96 视角结构化空间规范（8 方位角 $\times$ 4 仰角 $\times$ 3 距离）。
4. **算法实现提炼**：
   - 确定性样本契约判定逻辑（BBox 边界 $\ge 5\%$、Mask 覆盖 $\ge 1\%$、光线网格比 $\ge 0.80$、零网格穿插）。
   - 弱切片定位算法与 72-request 结构化请求编译逻辑。
   - 有界环境修复策略（曝光与支撑面抬升微调，$\le 2$ 轮）。
   - 回归感知模型准入规则（Weak-4 改善 $\ge 5\%$，硬红线 $(0^\circ, 0^\circ) < 5.0^\circ$）。

### B. 属于 DataEvolver 大工程、未复用的内容
1. **多阶段文生图/图生 3D 通用管道**：
   - `pipeline/stage1_text_expansion.py`、`stage2_t2i_generate.py`、`stage2_5_sam2_segment.py`、`stage3_image_to_3d.py` 等。
2. **世界模型与全景生成系统**：
   - `HY-World`、`SeeThrough3D`、全景缝合与多视角渲染后台。
3. **网络搜索与前置研究工具**：
   - `stage0_web_research.py` 及相关数据。
4. **运维与可观测性套件**：
   - Superlog 遥测接入、监控守护进程及测试脚本。
5. **无关的子项目与二进制归档**：
   - OpenRSI、DataFlow-WebUI、aDSL、大体积 zip 包。
6. **面向工程的旧官网**：
   - 原 `web/index.html`（含大量 T2I/T2V 营销与世界模型展示）。

### C. 为 DataRSI 论文全新增设的内容
1. **面向 ICASSP 审稿人的学术基础设施**：
   - 规范的 `pyproject.toml`、`requirements.txt`、`LICENSE` (Apache 2.0)、`CITATION.cff`。
2. **完整的论文文档集**：
   - `README.md`：30 秒速查审稿人索引、论文架构与主结果一览。
   - `docs/PROTOCOL.md`：形式化有界修订协议 $\Gamma$ 完整规范。
   - `docs/REPRODUCTION.md`：极速评测重现（< 30 秒）与全量重现双层指南。
   - `docs/REPAIR_AUDIT.md`：72 候选集诊断、2 例真实修复 Trace 审计及独立渲染边界说明。
   - `docs/RESULTS.md`：详细实验指标底册与配对差值。
   - `docs/DATAEVOLVER_RELATION.md`：严谨的学术与工程关系定位。
3. **自包含极速重现脚本**：
   - `scripts/reproduce_tables.py` / `.sh`：一键直接复现 Table 1 和 Table 3。
   - `scripts/reproduce_admission.py` / `.sh`：一键验算 3/3 PROMOTE 准入结论。
   - `scripts/reproduce_repair_audit.py` / `.sh`：一键查看修复审计数据与两例真实修复 Trace。
   - `scripts/reproduce_diagnosis.py` / `.sh`：一键展示因子空间与 Weak-4 切片。
4. **轻量、安全、无敏感信息的结构化科研产物**：
   - `artifacts/icassp2027/requests/`：Weak-4 切片与 72-request 结构化清单。
   - `artifacts/icassp2027/repair_traces/`：两例成功修复过程的机器可读 JSON Trace。
   - `artifacts/icassp2027/admission_records/`：准入裁决记录与 Schema。
   - `artifacts/icassp2027/seed42/`, `seed43/`, `seed44/`：3 种子明细指标。
5. **纯粹的学术 Project Page**：
   - `web/index.html`：基于现代响应式学术排版，聚焦于 ICASSP 2027 论文本身。
