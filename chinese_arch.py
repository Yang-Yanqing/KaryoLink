import streamlit as st

st.set_page_config(page_title="KaryoLink – 架构", layout="centered")

st.title("KaryoLink 平台的建议架构")

st.markdown(
    """
整体思路是将平台视为 **两个主要流程**：

- **输入流程：** 核型图像进入系统，被预处理并由 AI 分析。  
- **输出流程：** AI 的结果经过清洗、验证并转换为结构化报告（JSON / PDF）。

下面的图只是一个用于讨论架构的概念性示意图。
"""
)

dot = r"""
digraph KaryoLink {
    rankdir=TB;
    fontsize=10;
    node [shape=rect, style="rounded,filled", fontname="Helvetica"];

    // ---------- Nodos ----------
    tecnico      [label="技术员\n（用户）", fillcolor="#BBDEFB"];
    frontend     [label="前端\n(React / Streamlit)", fillcolor="#E3F2FD"];
    upload       [label="上传 API\n(FastAPI)", fillcolor="#E3F2FD"];

    preprocess   [label="预处理\n（标准化 / 清理）", fillcolor="#FFF9C4"];

    storage      [label="对象存储 (S3)\n（标准化后的图像）", fillcolor="#FFCCBC"];
    mongo        [label="MongoDB\n（流程元数据\n(task_id / S3_path / 状态)）", fillcolor="#FFCCBC"];

    ia           [label="AI 服务 (GPU)\n（使用 S3 + 元数据）", fillcolor="#FFE082"];

    postprocess  [label="后处理\n（清洗 / 验证）", fillcolor="#FFE0B2"];
    report       [label="报告生成\n(JSON)", fillcolor="#E1BEE7"];

    postgres     [label="PostgreSQL\n（结构化结果）", fillcolor="#C8E6C9"];
    frontend_rep [label="前端\n（报告视图 / PDF 下载）", fillcolor="#D1C4E9"];


    // ---------- Frontend (cluster con línea discontinua) ----------
    subgraph cluster_frontend {
        label="前端区域";
        style="dashed";
        color="#90CAF9";

        tecnico  -> frontend   [label=" 上传图像 "];
        frontend -> upload;
    }

    // ---------- Backend ----------
    upload     -> preprocess;

    // guardar imagen y metadatos
    preprocess -> storage   [label=" 保存标准化图像\n到 S3 "];
    preprocess -> mongo     [label=" 创建 task\n包含 S3_path 与状态 "];

    // IA usa ambas fuentes: metadatos + imagen real
    mongo   -> ia [label=" 读取 S3_path\n/ 元数据 "];
    storage -> ia [label=" 从 S3 读取图像 "];

    // flujo de salida
    ia          -> postprocess [label=" 原始结果 "];
    postprocess -> report      [label=" 清洗后的结果 "];
    report      -> postgres    [label=" 保存报告 "];
    postgres    -> frontend_rep[label=" 查询结果\n用于展示报告 "];

    // actualizar estado del task en Mongo
    report      -> mongo       [style=dashed, label=" 更新 task 状态\n(done) "];
}
"""

st.subheader("高层级示意图（两个流程：输入与输出）")
st.graphviz_chart(dot)

st.caption(
    "用于讨论架构的概念性示意图：输入流程（图像）和输出流程（AI 报告）。具体细节可根据模型和医疗需求进一步调整。"
)
