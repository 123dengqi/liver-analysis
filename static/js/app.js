const I18N = {
  zh: {
    page_title: "肝硬化多重用药与营养不良分析",
    skip_link: "跳到主要内容",
    brand_title: "肝硬化临床分析",
    brand_subtitle: "多重用药与营养不良风险",
    nav_label: "页面导航",
    tab_overview: "研究概览",
    tab_comparison: "分组比较",
    tab_model: "回归模型",
    tab_quality: "数据质量",
    strategy_label: "分析单元",
    strategy_first: "首次住院记录",
    strategy_latest: "末次住院记录",
    strategy_all: "全部住院记录（每行独立）",
    strategy_feedback_default: "正在载入分析结果...",
    retry: "重新载入",
    eyebrow_study: "回顾性队列分析",
    headline: "多重用药与高营养不良风险的关系",
    definitions_loading: "正在载入分析口径...",
    status_ready: "数据就绪",
    status_error: "连接异常",
    figure_1: "图 1",
    figure_1_title: "不同年龄组的用药与营养风险",
    chart_medications: "用药数量",
    chart_polypharmacy: "多重用药率",
    chart_malnutrition: "高营养不良风险率",
    cohort_flow_eyebrow: "样本流程",
    cohort_flow_title: "队列构建与完整性",
    table_2: "表 2",
    table_2_title: "按多重用药及营养风险分组的临床特征",
    grouping_label: "分组方式",
    segment_polypharmacy: "按多重用药分组",
    segment_malnutrition: "按营养风险分组",
    search_label: "筛选指标",
    search_placeholder: "例如：MELD-Na",
    table_empty: "没有匹配的指标，请调整筛选词。",
    table_note: "连续变量为中位数（四分位距），分类变量为 n（%）。连续变量采用 Mann-Whitney U 检验，分类变量采用卡方或 Fisher 精确检验。",
    table_3: "表 3",
    table_3_title: "高营养不良风险的 Logistic 回归",
    primary_estimate: "主要效应估计",
    model_explanation_title: "模型说明",
    model_explanation: "结局变量为 RFH-NPT≥2；暴露变量为出院药物种类≥5。效应量为优势比（OR）及95%置信区间。",
    quality_eyebrow: "数据审计",
    quality_title: "数据质量与可复核输出",
    downloads_title: "分析文件",
    downloads_note: "输出均不包含姓名，药物复核表使用哈希化患者编号。",
    dl_cohort: "分析数据",
    dl_review: "药物复核表",
    dl_poly: "多重用药表",
    dl_mal: "营养风险表",
    dl_logistic: "回归结果",
    dl_comorbidity: "合并症抽取表",
    warning_summary: "解释边界与使用提示",
    warning_body: "本研究为回顾性观察性分析，回归结果表示关联而非因果。药物数量由出院带药自由文本自动解析，低/中置信度记录应在论文定稿前人工核对。",
    loading: "正在更新统计结果",
    severity_prefix: "肝硬化严重程度：",
    metric_sample: "分析样本",
    metric_polypharmacy: "多重用药",
    metric_malnutrition: "高营养不良风险",
    metric_med_count: "用药数量",
    metric_meld: "MELD-Na",
    patients: "位患者",
    cases: "例",
    median_types: "中位种数",
    median_score: "中位评分",
    figure_note: "当前口径：{strategy}",
    model_note: "调整因素：{adjustment} · {variance}",
    loading_strategy: "正在载入“{strategy}”结果...",
    updated: "已更新：{strategy} · {n} 条分析记录",
    load_error: "无法载入统计结果",
    retry_hint: "，请检查服务状态后重试。",
    flow_source: "原始住院记录 · {patients} 位患者",
    flow_age: "排除年龄不合格记录 · 未满18岁 {under18}，年龄缺失 {missing}",
    flow_rfh: "排除RFH-NPT缺失记录",
    flow_included: "纳入主分析 · 完整病例 {n}",
    table_feature: "特征",
    table_overall: "总体",
    table_p: "P值",
    table_caption: "临床特征分组比较",
    model_col_model: "模型",
    model_col_term: "变量",
    model_col_or: "OR",
    model_col_ci: "95% CI",
    model_col_p: "P值",
    model_unavailable: "模型不可用",
    complete_case: "多变量模型完整病例 n={n}。",
    forest_unavailable: "模型未能收敛，请检查数据完整性。",
    forest_axis: "优势比（对数刻度）",
    forest_aria: "多变量Logistic回归森林图",
    chart_aria: "年龄分组柱状图",
    chart_unit_types: "种",
    quality_source: "原始记录数",
    quality_patients: "唯一患者数",
    quality_duplicates: "当前口径去除的重复记录",
    quality_missing_bmi: "分析队列BMI缺失",
    quality_missing_meld: "分析队列MELD-Na缺失",
    quality_manual_review: "药物文本需人工复核",
    quality_conf_high: "药物解析高置信度",
    quality_conf_medium: "药物解析中置信度",
    quality_conf_low: "药物解析低置信度",
    quality_meld_mismatch: "MELD-Na公式不一致 · 已核验 {n} 条",
    quality_ascites: "腹水",
    quality_varices: "静脉曲张",
    quality_he: "肝性脑病",
    quality_infection: "感染",
    quality_diabetes: "糖尿病（出院诊断）",
    quality_hypertension: "高血压（出院诊断）",
    quality_chd: "冠状动脉性心脏病（出院诊断）",
  },
  en: {
    page_title: "Cirrhosis Polypharmacy & Malnutrition Analysis",
    skip_link: "Skip to main content",
    brand_title: "Cirrhosis Clinical Analysis",
    brand_subtitle: "Polypharmacy & Malnutrition Risk",
    nav_label: "Page navigation",
    tab_overview: "Overview",
    tab_comparison: "Comparison",
    tab_model: "Regression",
    tab_quality: "Data Quality",
    strategy_label: "Analysis unit",
    strategy_first: "First admission",
    strategy_latest: "Latest admission",
    strategy_all: "All admissions (row-independent)",
    strategy_feedback_default: "Loading analysis results...",
    retry: "Reload",
    eyebrow_study: "Retrospective cohort study",
    headline: "Polypharmacy and High Malnutrition Risk",
    definitions_loading: "Loading analysis definitions...",
    status_ready: "Data ready",
    status_error: "Connection error",
    figure_1: "Figure 1",
    figure_1_title: "Medications and nutrition risk by age group",
    chart_medications: "Medication count",
    chart_polypharmacy: "Polypharmacy rate",
    chart_malnutrition: "High malnutrition risk rate",
    cohort_flow_eyebrow: "Sample flow",
    cohort_flow_title: "Cohort construction and completeness",
    table_2: "Table 2",
    table_2_title: "Clinical characteristics by polypharmacy and nutrition risk",
    grouping_label: "Grouping",
    segment_polypharmacy: "By polypharmacy",
    segment_malnutrition: "By nutrition risk",
    search_label: "Filter variables",
    search_placeholder: "e.g. MELD-Na",
    table_empty: "No matching variables. Adjust your search.",
    table_note: "Continuous variables: median (IQR); categorical: n (%). Mann-Whitney U for continuous; chi-square or Fisher's exact for categorical.",
    table_3: "Table 3",
    table_3_title: "Logistic regression for high malnutrition risk",
    primary_estimate: "Primary effect estimate",
    model_explanation_title: "Model notes",
    model_explanation: "Outcome: RFH-NPT ≥2; exposure: ≥5 discharge medication types. Effect size: odds ratio (OR) with 95% CI.",
    quality_eyebrow: "Data audit",
    quality_title: "Data quality and reproducible outputs",
    downloads_title: "Analysis files",
    downloads_note: "Outputs exclude patient names; medication review uses hashed patient IDs.",
    dl_cohort: "Analysis data",
    dl_review: "Medication review",
    dl_poly: "Polypharmacy table",
    dl_mal: "Nutrition risk table",
    dl_logistic: "Regression results",
    dl_comorbidity: "Comorbidity extraction",
    warning_summary: "Interpretation limits",
    warning_body: "This is a retrospective observational study; regression results indicate association, not causation. Medication counts are parsed from free text; low/medium confidence records should be manually verified before publication.",
    loading: "Updating statistics",
    severity_prefix: "Cirrhosis severity: ",
    metric_sample: "Analysis sample",
    metric_polypharmacy: "Polypharmacy",
    metric_malnutrition: "High malnutrition risk",
    metric_med_count: "Medication count",
    metric_meld: "MELD-Na",
    patients: "patients",
    cases: "cases",
    median_types: "median types",
    median_score: "median score",
    figure_note: "Current unit: {strategy}",
    model_note: "Adjusted for: {adjustment} · {variance}",
    loading_strategy: "Loading “{strategy}” results...",
    updated: "Updated: {strategy} · {n} records",
    load_error: "Failed to load statistics",
    retry_hint: ". Check the service and try again.",
    flow_source: "Source admissions · {patients} patients",
    flow_age: "Excluded age-ineligible · under 18: {under18}, missing age: {missing}",
    flow_rfh: "Excluded missing RFH-NPT",
    flow_included: "Included in main analysis · complete cases {n}",
    table_feature: "Variable",
    table_overall: "Overall",
    table_p: "P value",
    table_caption: "Clinical characteristics by group",
    model_col_model: "Model",
    model_col_term: "Term",
    model_col_or: "OR",
    model_col_ci: "95% CI",
    model_col_p: "P value",
    model_unavailable: "Model unavailable",
    complete_case: "Multivariable complete cases n={n}.",
    forest_unavailable: "Model did not converge. Check data completeness.",
    forest_axis: "Odds ratio (log scale)",
    forest_aria: "Multivariable logistic regression forest plot",
    chart_aria: "Age group bar chart",
    chart_unit_types: "types",
    quality_source: "Source records",
    quality_patients: "Unique patients",
    quality_duplicates: "Duplicate records removed (current unit)",
    quality_missing_bmi: "Missing BMI in cohort",
    quality_missing_meld: "Missing MELD-Na in cohort",
    quality_manual_review: "Medications need manual review",
    quality_conf_high: "High-confidence medication parsing",
    quality_conf_medium: "Medium-confidence medication parsing",
    quality_conf_low: "Low-confidence medication parsing",
    quality_meld_mismatch: "MELD-Na formula mismatch · checked {n}",
    quality_ascites: "Ascites",
    quality_varices: "Varices",
    quality_he: "Hepatic encephalopathy",
    quality_infection: "Infection",
    quality_diabetes: "Diabetes (from diagnosis)",
    quality_hypertension: "Hypertension (from diagnosis)",
    quality_chd: "Coronary heart disease (from diagnosis)",
  },
};

const state = {
  data: null,
  activeTable: "polypharmacy",
  strategy: "all",
  lang: "zh",
  activeView: "overview",
  requestId: 0,
};

const tr = (key, vars = {}) => {
  let text = I18N[state.lang]?.[key] ?? I18N.zh[key] ?? key;
  Object.entries(vars).forEach(([name, value]) => {
    text = text.replace(`{${name}}`, value);
  });
  return text;
};

const pLabel = value => value === "NA" ? "P=NA" : value.startsWith("<") ? `P${value}` : `P=${value}`;

function applyStaticI18n() {
  document.documentElement.lang = state.lang === "zh" ? "zh-CN" : "en";
  document.title = tr("page_title");
  document.querySelectorAll("[data-i18n]").forEach(el => {
    el.textContent = tr(el.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    el.placeholder = tr(el.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-aria]").forEach(el => {
    el.setAttribute("aria-label", tr(el.dataset.i18nAria));
  });
  document.querySelectorAll(".lang-btn").forEach(btn => {
    const active = btn.dataset.lang === state.lang;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-pressed", String(active));
  });
  const strategySelect = document.querySelector("#strategy");
  [...strategySelect.options].forEach(option => {
    const key = `strategy_${option.value}`;
    if (I18N[state.lang][key]) option.textContent = tr(key);
  });
}

async function loadDashboard(strategy) {
  const requestId = ++state.requestId;
  const strategySelect = document.querySelector("#strategy");
  const loading = document.querySelector("#loading");
  const feedback = document.querySelector("#feedback");
  const retry = document.querySelector("#retry");
  state.strategy = strategy;
  strategySelect.disabled = true;
  loading.classList.remove("hidden");
  feedback.classList.remove("error");
  retry.hidden = true;
  setFeedback(tr("loading_strategy", { strategy: strategySelect.options[strategySelect.selectedIndex].text }));
  try {
    const response = await fetch(`/api/dashboard?strategy=${strategy}&lang=${state.lang}`);
    if (!response.ok) throw new Error(tr("load_error"));
    const payload = await response.json();
    if (requestId !== state.requestId) return;
    state.data = payload;
    renderAll();
    setFeedback(tr("updated", { strategy: payload.meta.strategies[strategy], n: payload.summary.n }));
    updateUrl();
  } catch (error) {
    if (requestId !== state.requestId) return;
    feedback.classList.add("error");
    retry.hidden = false;
    setFeedback(`${error.message}${tr("retry_hint")}`);
    document.querySelector("#connection-status").classList.add("error");
    document.querySelector("#connection-status").innerHTML = `<span></span> ${tr("status_error")}`;
    return;
  } finally {
    if (requestId === state.requestId) {
      strategySelect.disabled = false;
      loading.classList.add("hidden");
    }
  }
}

function setFeedback(message) {
  document.querySelector("#strategy-feedback").textContent = message;
}

function updateUrl() {
  const url = new URL(window.location.href);
  url.searchParams.set("strategy", state.strategy);
  url.searchParams.set("lang", state.lang);
  url.hash = state.activeView;
  window.history.replaceState(null, "", url);
}

function setLanguage(lang) {
  state.lang = lang === "en" ? "en" : "zh";
  applyStaticI18n();
  loadDashboard(state.strategy);
}

function renderAll() {
  const { meta, summary, age_groups, logistic } = state.data;
  document.querySelector("#definitions").textContent =
    `${meta.polypharmacy_definition} · ${meta.malnutrition_definition} · ${tr("severity_prefix")}${meta.severity_measure} · ${meta.analysis_unit_note}`;
  document.querySelector("#connection-status").classList.remove("error");
  document.querySelector("#connection-status").innerHTML = `<span></span> ${tr("status_ready")}`;
  const metrics = [
    [tr("metric_sample"), summary.n, `${summary.unique_patients} ${tr("patients")}`, ""],
    [tr("metric_polypharmacy"), `${summary.polypharmacy_pct}%`, `${summary.polypharmacy_n} ${tr("cases")}`, ""],
    [tr("metric_malnutrition"), `${summary.malnutrition_pct}%`, `${summary.malnutrition_n} ${tr("cases")}`, "amber"],
    [tr("metric_med_count"), summary.medication_median, tr("median_types"), ""],
    [tr("metric_meld"), summary.meld_na_median, tr("median_score"), ""],
  ];
  document.querySelector("#metrics").innerHTML = metrics.map(([label, value, detail, cls]) =>
    `<article class="metric ${cls}"><span class="metric-label">${label}</span><strong class="metric-value">${value}</strong><span class="metric-detail">${detail}</span></article>`
  ).join("");
  document.querySelector("#figure-note").textContent = tr("figure_note", { strategy: meta.strategies[meta.strategy] });
  document.querySelector("#p-medications").textContent = pLabel(age_groups.p_values.medications);
  document.querySelector("#p-polypharmacy").textContent = pLabel(age_groups.p_values.polypharmacy);
  document.querySelector("#p-malnutrition").textContent = pLabel(age_groups.p_values.malnutrition);
  renderBarChart("chart-medications", age_groups.rows, "medication_median", tr("chart_unit_types"), false);
  renderBarChart("chart-polypharmacy", age_groups.rows, "polypharmacy_pct", "%", false);
  renderBarChart("chart-malnutrition", age_groups.rows, "malnutrition_pct", "%", true);
  renderFlow();
  renderComparison();
  renderModel();
  renderQuality();
  document.querySelector("#model-note").textContent = tr("model_note", {
    adjustment: logistic.adjustment,
    variance: logistic.variance_estimator,
  });
}

function renderBarChart(target, rows, key, suffix, alternate) {
  const width = 360, height = 235, left = 42, right = 12, top = 18, bottom = 40;
  const values = rows.map(row => Number(row[key] || 0));
  const maxValue = suffix === "%" ? 100 : Math.max(8, Math.ceil(Math.max(...values) / 2) * 2);
  const plotHeight = height - top - bottom;
  const plotWidth = width - left - right;
  const slot = plotWidth / rows.length;
  const grid = [0, .25, .5, .75, 1].map(ratio => {
    const y = top + plotHeight * (1 - ratio);
    return `<line class="grid" x1="${left}" y1="${y}" x2="${width-right}" y2="${y}"/><text class="axis-label" x="${left-7}" y="${y+4}" text-anchor="end">${Math.round(maxValue*ratio)}</text>`;
  }).join("");
  const bars = rows.map((row, index) => {
    const value = values[index];
    const barHeight = maxValue ? value / maxValue * plotHeight : 0;
    const x = left + index * slot + slot * .22;
    const y = top + plotHeight - barHeight;
    return `<rect class="bar ${alternate ? "alt" : ""}" x="${x}" y="${y}" width="${slot*.56}" height="${barHeight}" rx="2"><title>${row.age_group}: ${value}${suffix} (n=${row.n})</title></rect><text class="value-label" x="${x+slot*.28}" y="${Math.max(12,y-7)}" text-anchor="middle">${value}${suffix}</text><text class="axis-label" x="${x+slot*.28}" y="${height-16}" text-anchor="middle">${row.age_group}</text>`;
  }).join("");
  document.querySelector(`#${target}`).innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${tr("chart_aria")}">${grid}${bars}</svg>`;
}

function renderFlow() {
  const q = state.data.quality, s = state.data.summary;
  const items = [
    [q.source_records, tr("flow_source", { patients: q.source_patients })],
    [q.excluded_age_ineligible, tr("flow_age", { under18: q.under_18, missing: q.missing_age })],
    [q.missing_rfh_npt, tr("flow_rfh")],
    [s.n, tr("flow_included", { n: s.complete_case_n })],
  ];
  document.querySelector("#cohort-flow").innerHTML = items.map(([value, label]) =>
    `<div class="flow-item"><strong>${value}</strong><span>${label}</span></div>`
  ).join("");
}

function renderComparison() {
  const sourceRows = state.activeTable === "polypharmacy" ? state.data.polypharmacy_table : state.data.malnutrition_table;
  const query = document.querySelector("#table-search").value.trim().toLowerCase();
  const rows = sourceRows.filter(row => row.variable.toLowerCase().includes(query));
  const first = sourceRows[0];
  const table = document.querySelector("#comparison-table");
  const empty = document.querySelector("#table-empty");
  table.hidden = rows.length === 0;
  empty.hidden = rows.length !== 0;
  table.innerHTML = `<caption class="sr-only">${tr("table_caption")}</caption><thead><tr><th scope="col">${tr("table_feature")}</th><th scope="col">${tr("table_overall")}</th><th scope="col">${first.group0_label}</th><th scope="col">${first.group1_label}</th><th scope="col">${tr("table_p")}</th></tr></thead><tbody>${rows.map(row => `<tr><td>${row.variable}</td><td>${row.overall}</td><td>${row.group0}</td><td>${row.group1}</td><td class="${isSignificant(row.p_value) ? "significant" : ""}">${row.p_value}</td></tr>`).join("")}</tbody>`;
}

function isSignificant(p) { return p.startsWith("<") || (!Number.isNaN(Number(p)) && Number(p) < .05); }

function renderModel() {
  const model = state.data.logistic;
  const rows = model.adjusted;
  document.querySelector("#model-table").innerHTML = `<thead><tr><th>${tr("model_col_model")}</th><th>${tr("model_col_term")}</th><th>${tr("model_col_or")}</th><th>${tr("model_col_ci")}</th><th>${tr("model_col_p")}</th><th>n</th></tr></thead><tbody>${[...model.unadjusted, ...rows].map(row => `<tr><td>${row.model}</td><td>${row.term}</td><td>${row.or}</td><td>${row.ci_low}-${row.ci_high}</td><td class="${isSignificant(row.p_value) ? "significant" : ""}">${row.p_value}</td><td>${row.n}</td></tr>`).join("")}</tbody>`;
  const primary = rows.find(row => row.term_key === "polypharmacy") || model.unadjusted[0];
  document.querySelector("#primary-estimate").innerHTML = primary
    ? `<span class="estimate">OR ${primary.or}</span><span class="estimate-ci">95% CI ${primary.ci_low}-${primary.ci_high} · ${pLabel(primary.p_value)}</span>`
    : `<span class="estimate">${tr("model_unavailable")}</span>`;
  document.querySelector("#complete-case-note").textContent = tr("complete_case", { n: model.adjusted_n });
  renderForest(rows);
}

function renderForest(rows) {
  const target = document.querySelector("#forest-plot");
  if (!rows.length) { target.textContent = tr("forest_unavailable"); return; }
  const width = 720, rowHeight = 48, top = 42, bottom = 45, left = 210, right = 70;
  const height = top + bottom + rows.length * rowHeight;
  const minLog = Math.log(.25), maxLog = Math.log(8);
  const x = value => left + (Math.log(Math.max(.25, Math.min(8, value))) - minLog) / (maxLog-minLog) * (width-left-right);
  const ticks = [.25,.5,1,2,4,8].map(tick => `<line class="grid" x1="${x(tick)}" y1="${top-10}" x2="${x(tick)}" y2="${height-bottom}"/><text x="${x(tick)}" y="${height-16}" text-anchor="middle">${tick}</text>`).join("");
  const marks = rows.map((row, i) => {
    const y = top + i*rowHeight + 14;
    return `<text x="4" y="${y+4}">${row.term}</text><line class="ci" x1="${x(row.ci_low)}" y1="${y}" x2="${x(row.ci_high)}" y2="${y}"/><line class="ci" x1="${x(row.ci_low)}" y1="${y-5}" x2="${x(row.ci_low)}" y2="${y+5}"/><line class="ci" x1="${x(row.ci_high)}" y1="${y-5}" x2="${x(row.ci_high)}" y2="${y+5}"/><circle class="point" cx="${x(row.or)}" cy="${y}" r="5"><title>OR ${row.or} (95% CI ${row.ci_low}-${row.ci_high})</title></circle><text x="${width-5}" y="${y+4}" text-anchor="end">${row.or} (${row.ci_low}-${row.ci_high})</text>`;
  }).join("");
  target.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${tr("forest_aria")}">${ticks}<line class="null" x1="${x(1)}" y1="${top-10}" x2="${x(1)}" y2="${height-bottom}"/>${marks}<text x="${(left+width-right)/2}" y="${height-1}" text-anchor="middle">${tr("forest_axis")}</text></svg>`;
}

function renderQuality() {
  const q = state.data.quality;
  const confidence = q.medication_parse_confidence;
  const items = [
    [q.source_records, tr("quality_source"), ""],
    [q.source_patients, tr("quality_patients"), ""],
    [q.duplicate_records_removed, tr("quality_duplicates"), ""],
    [q.missing_bmi, tr("quality_missing_bmi"), q.missing_bmi ? "warn" : ""],
    [q.missing_meld_na, tr("quality_missing_meld"), q.missing_meld_na ? "warn" : ""],
    [q.manual_review_n, tr("quality_manual_review"), q.manual_review_n ? "warn" : ""],
    [confidence.high || 0, tr("quality_conf_high"), ""],
    [confidence.medium || 0, tr("quality_conf_medium"), confidence.medium ? "warn" : ""],
    [confidence.low || 0, tr("quality_conf_low"), confidence.low ? "warn" : ""],
    [q.meld_na_formula_mismatch, tr("quality_meld_mismatch", { n: q.meld_na_formula_checked }), q.meld_na_formula_mismatch ? "warn" : ""],
    [q.ascites_n || 0, tr("quality_ascites"), ""],
    [q.varices_n || 0, tr("quality_varices"), ""],
    [q.hepatic_encephalopathy_n || 0, tr("quality_he"), ""],
    [q.infection_n || 0, tr("quality_infection"), ""],
    [q.diabetes_n || 0, tr("quality_diabetes"), ""],
    [q.hypertension_n || 0, tr("quality_hypertension"), ""],
    [q.coronary_heart_disease_n || 0, tr("quality_chd"), ""],
  ];
  document.querySelector("#quality-grid").innerHTML = items.map(([value, label, cls]) =>
    `<div class="quality-item ${cls}"><strong>${value}</strong><span>${label}</span></div>`
  ).join("");
}

document.querySelectorAll(".tab").forEach(button => button.addEventListener("click", () => {
  activateView(button.dataset.target, true);
}));
document.querySelectorAll(".segment").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".segment").forEach(el => {
    el.classList.remove("active");
    el.setAttribute("aria-selected", "false");
  });
  button.classList.add("active");
  button.setAttribute("aria-selected", "true");
  state.activeTable = button.dataset.table;
  renderComparison();
}));
document.querySelectorAll(".lang-btn").forEach(button => button.addEventListener("click", () => {
  if (button.dataset.lang !== state.lang) setLanguage(button.dataset.lang);
}));
document.querySelector("#table-search").addEventListener("input", renderComparison);
document.querySelector("#strategy").addEventListener("change", event => loadDashboard(event.target.value));
document.querySelector("#retry").addEventListener("click", () => loadDashboard(state.strategy));

function activateView(target, focusTab = false) {
  const validTarget = ["overview", "comparison", "model", "quality"].includes(target) ? target : "overview";
  state.activeView = validTarget;
  document.querySelectorAll(".tab").forEach(el => {
    const active = el.dataset.target === validTarget;
    el.classList.toggle("active", active);
    el.setAttribute("aria-selected", String(active));
    el.tabIndex = active ? 0 : -1;
    if (active && focusTab) el.focus();
  });
  document.querySelectorAll(".view").forEach(el => el.classList.toggle("active", el.id === validTarget));
  updateUrl();
}

document.querySelector(".tabs").addEventListener("keydown", event => {
  if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
  const tabs = [...document.querySelectorAll(".tab")];
  const current = tabs.findIndex(tab => tab.dataset.target === state.activeView);
  let next = current;
  if (event.key === "ArrowLeft") next = (current - 1 + tabs.length) % tabs.length;
  if (event.key === "ArrowRight") next = (current + 1) % tabs.length;
  if (event.key === "Home") next = 0;
  if (event.key === "End") next = tabs.length - 1;
  event.preventDefault();
  activateView(tabs[next].dataset.target, true);
});

const initialParams = new URLSearchParams(window.location.search);
const initialStrategy = ["first", "latest", "all"].includes(initialParams.get("strategy")) ? initialParams.get("strategy") : "all";
const initialLang = initialParams.get("lang") === "en" ? "en" : "zh";
const initialView = window.location.hash.replace("#", "") || "overview";
state.lang = initialLang;
state.strategy = initialStrategy;
document.querySelector("#strategy").value = initialStrategy;
applyStaticI18n();
activateView(initialView);
loadDashboard(initialStrategy);
