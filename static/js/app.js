const state = {
  data: null,
  activeTable: "polypharmacy",
  strategy: "first",
  activeView: "overview",
  requestId: 0,
};

const fmt = (value, suffix = "") => value == null ? "NA" : `${value}${suffix}`;
const pLabel = value => value === "NA" ? "P=NA" : value.startsWith("<") ? `P${value}` : `P=${value}`;

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
  setFeedback(`正在载入“${strategySelect.options[strategySelect.selectedIndex].text}”结果...`);
  try {
    const response = await fetch(`/api/dashboard?strategy=${strategy}`);
    if (!response.ok) throw new Error("无法载入统计结果");
    const payload = await response.json();
    if (requestId !== state.requestId) return;
    state.data = payload;
    renderAll();
    setFeedback(`已更新：${payload.meta.strategies[strategy]} · ${payload.summary.n} 条分析记录`);
    updateUrl();
  } catch (error) {
    if (requestId !== state.requestId) return;
    feedback.classList.add("error");
    retry.hidden = false;
    setFeedback(`${error.message}，请检查服务状态后重试。`);
    document.querySelector("#connection-status").classList.add("error");
    document.querySelector("#connection-status").innerHTML = "<span></span> 连接异常";
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
  url.hash = state.activeView;
  window.history.replaceState(null, "", url);
}

function renderAll() {
  const { meta, summary, age_groups, logistic } = state.data;
  document.querySelector("#definitions").textContent = `${meta.polypharmacy_definition} · ${meta.malnutrition_definition} · 肝硬化严重程度：${meta.severity_measure} · ${meta.analysis_unit_note}`;
  document.querySelector("#connection-status").classList.remove("error");
  document.querySelector("#connection-status").innerHTML = "<span></span> 数据就绪";
  const metrics = [
    ["分析样本", summary.n, `${summary.unique_patients} 位患者`, ""],
    ["多重用药", `${summary.polypharmacy_pct}%`, `${summary.polypharmacy_n} 例`, ""],
    ["高营养不良风险", `${summary.malnutrition_pct}%`, `${summary.malnutrition_n} 例`, "amber"],
    ["用药数量", summary.medication_median, "中位种数", ""],
    ["MELD-Na", summary.meld_na_median, "中位评分", ""],
  ];
  document.querySelector("#metrics").innerHTML = metrics.map(([label, value, detail, cls]) => `<article class="metric ${cls}"><span class="metric-label">${label}</span><strong class="metric-value">${value}</strong><span class="metric-detail">${detail}</span></article>`).join("");
  document.querySelector("#figure-note").textContent = `当前口径：${meta.strategies[meta.strategy]}`;
  document.querySelector("#p-medications").textContent = pLabel(age_groups.p_values.medications);
  document.querySelector("#p-polypharmacy").textContent = pLabel(age_groups.p_values.polypharmacy);
  document.querySelector("#p-malnutrition").textContent = pLabel(age_groups.p_values.malnutrition);
  renderBarChart("chart-medications", age_groups.rows, "medication_median", "种", false);
  renderBarChart("chart-polypharmacy", age_groups.rows, "polypharmacy_pct", "%", false);
  renderBarChart("chart-malnutrition", age_groups.rows, "malnutrition_pct", "%", true);
  renderFlow();
  renderComparison();
  renderModel();
  renderQuality();
  document.querySelector("#model-note").textContent = `调整因素：${logistic.adjustment} · ${logistic.variance_estimator}`;
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
  document.querySelector(`#${target}`).innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="年龄分组柱状图">${grid}${bars}</svg>`;
}

function renderFlow() {
  const q = state.data.quality, s = state.data.summary;
  const items = [
    [q.source_records, `原始住院记录 · ${q.source_patients} 位患者`],
    [q.excluded_age_ineligible, `排除年龄不合格记录 · 未满18岁 ${q.under_18}，年龄缺失 ${q.missing_age}`],
    [q.missing_rfh_npt, "排除RFH-NPT缺失记录"],
    [s.n, `纳入主分析 · 完整病例 ${s.complete_case_n}`],
  ];
  document.querySelector("#cohort-flow").innerHTML = items.map(([value, label]) => `<div class="flow-item"><strong>${value}</strong><span>${label}</span></div>`).join("");
}

function renderComparison() {
  const sourceRows = state.activeTable === "polypharmacy" ? state.data.polypharmacy_table : state.data.malnutrition_table;
  const query = document.querySelector("#table-search").value.trim().toLocaleLowerCase("zh-CN");
  const rows = sourceRows.filter(row => row.variable.toLocaleLowerCase("zh-CN").includes(query));
  const first = sourceRows[0];
  const table = document.querySelector("#comparison-table");
  const empty = document.querySelector("#table-empty");
  table.hidden = rows.length === 0;
  empty.hidden = rows.length !== 0;
  table.innerHTML = `<caption class="sr-only">临床特征分组比较</caption><thead><tr><th scope="col">特征</th><th scope="col">总体</th><th scope="col">${first.group0_label}</th><th scope="col">${first.group1_label}</th><th scope="col">P值</th></tr></thead><tbody>${rows.map(row => `<tr><td>${row.variable}</td><td>${row.overall}</td><td>${row.group0}</td><td>${row.group1}</td><td class="${isSignificant(row.p_value) ? "significant" : ""}">${row.p_value}</td></tr>`).join("")}</tbody>`;
}

function isSignificant(p) { return p.startsWith("<") || (!Number.isNaN(Number(p)) && Number(p) < .05); }

function renderModel() {
  const model = state.data.logistic;
  const rows = model.adjusted;
  document.querySelector("#model-table").innerHTML = `<thead><tr><th>模型</th><th>变量</th><th>OR</th><th>95% CI</th><th>P值</th><th>n</th></tr></thead><tbody>${[...model.unadjusted, ...rows].map(row => `<tr><td>${row.model}</td><td>${row.term}</td><td>${row.or}</td><td>${row.ci_low}-${row.ci_high}</td><td class="${isSignificant(row.p_value) ? "significant" : ""}">${row.p_value}</td><td>${row.n}</td></tr>`).join("")}</tbody>`;
  const primary = rows.find(row => row.term.startsWith("多重用药")) || model.unadjusted[0];
  document.querySelector("#primary-estimate").innerHTML = primary ? `<span class="estimate">OR ${primary.or}</span><span class="estimate-ci">95% CI ${primary.ci_low}-${primary.ci_high} · ${pLabel(primary.p_value)}</span>` : `<span class="estimate">模型不可用</span>`;
  document.querySelector("#complete-case-note").textContent = `多变量模型完整病例 n=${model.adjusted_n}。`;
  renderForest(rows);
}

function renderForest(rows) {
  const target = document.querySelector("#forest-plot");
  if (!rows.length) { target.textContent = "模型未能收敛，请检查数据完整性。"; return; }
  const width = 720, rowHeight = 48, top = 42, bottom = 45, left = 210, right = 70;
  const height = top + bottom + rows.length * rowHeight;
  const minLog = Math.log(.25), maxLog = Math.log(8);
  const x = value => left + (Math.log(Math.max(.25, Math.min(8, value))) - minLog) / (maxLog-minLog) * (width-left-right);
  const ticks = [.25,.5,1,2,4,8].map(tick => `<line class="grid" x1="${x(tick)}" y1="${top-10}" x2="${x(tick)}" y2="${height-bottom}"/><text x="${x(tick)}" y="${height-16}" text-anchor="middle">${tick}</text>`).join("");
  const marks = rows.map((row, i) => {
    const y = top + i*rowHeight + 14;
    return `<text x="4" y="${y+4}">${row.term}</text><line class="ci" x1="${x(row.ci_low)}" y1="${y}" x2="${x(row.ci_high)}" y2="${y}"/><line class="ci" x1="${x(row.ci_low)}" y1="${y-5}" x2="${x(row.ci_low)}" y2="${y+5}"/><line class="ci" x1="${x(row.ci_high)}" y1="${y-5}" x2="${x(row.ci_high)}" y2="${y+5}"/><circle class="point" cx="${x(row.or)}" cy="${y}" r="5"><title>OR ${row.or} (95% CI ${row.ci_low}-${row.ci_high})</title></circle><text x="${width-5}" y="${y+4}" text-anchor="end">${row.or} (${row.ci_low}-${row.ci_high})</text>`;
  }).join("");
  target.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="多变量Logistic回归森林图">${ticks}<line class="null" x1="${x(1)}" y1="${top-10}" x2="${x(1)}" y2="${height-bottom}"/>${marks}<text x="${(left+width-right)/2}" y="${height-1}" text-anchor="middle">优势比（对数刻度）</text></svg>`;
}

function renderQuality() {
  const q = state.data.quality;
  const confidence = q.medication_parse_confidence;
  const items = [
    [q.source_records, "原始记录数", ""], [q.source_patients, "唯一患者数", ""],
    [q.duplicate_records_removed, "当前口径去除的重复记录", ""],
    [q.missing_bmi, "分析队列BMI缺失", q.missing_bmi ? "warn" : ""],
    [q.missing_meld_na, "分析队列MELD-Na缺失", q.missing_meld_na ? "warn" : ""],
    [q.manual_review_n, "药物文本需人工复核", q.manual_review_n ? "warn" : ""],
    [confidence.high || 0, "药物解析高置信度", ""],
    [confidence.medium || 0, "药物解析中置信度", confidence.medium ? "warn" : ""],
    [confidence.low || 0, "药物解析低置信度", confidence.low ? "warn" : ""],
    [q.meld_na_formula_mismatch, `MELD-Na公式不一致 · 已核验 ${q.meld_na_formula_checked} 条`, q.meld_na_formula_mismatch ? "warn" : ""],
  ];
  document.querySelector("#quality-grid").innerHTML = items.map(([value,label,cls]) => `<div class="quality-item ${cls}"><strong>${value}</strong><span>${label}</span></div>`).join("");
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
const initialStrategy = ["first", "latest", "all"].includes(initialParams.get("strategy")) ? initialParams.get("strategy") : "first";
const initialView = window.location.hash.replace("#", "") || "overview";
document.querySelector("#strategy").value = initialStrategy;
activateView(initialView);
loadDashboard(initialStrategy);
