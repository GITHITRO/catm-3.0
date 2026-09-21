---
title: "Catman 3.0 — Research Belief State & Agent Handoff"
status: active
version: 1.0
date: 2026-09-21
language: ru
purpose: "Полный контекст для независимого AI-агента: поиск reusable-компонентов и video references для Catman demo/MVP."
---

# Catman 3.0 — Research Belief State & Agent Handoff

## 0. Как использовать

Это операционный belief state: рабочие решения, гипотезы, ограничения, противоречия и критерии исследования. Это не финальная продуктовая спецификация.

Новый агент обязан:

1. Сначала прочитать этот файл и `CATMAN_AI_BLUEPRINT.md`.
2. Считать `DECISION` действующим решением до изменения владельцем проекта.
3. Считать `HYPOTHESIS` проверяемой гипотезой, а не фактом.
4. Искать reusable assets, а не пересобирать Catman с нуля.
5. Явно разделять `Build Now`, `Adapt`, `Enterprise Reference`, `Rejected`.

## 1. Миссия

**Catman** — AI-native Category Decision Room / manager workbench для category, commercial, operations и смежных менеджеров. Цель: кратно сократить путь от сигнала в данных до доказательного управленческого решения и контролируемого действия.

Целевой decision loop:

```text
Morning Brief
→ менеджер замечает сигнал/риск
→ задаёт бизнес-вопрос
→ агент строит и выполняет план анализа
→ SQL/Python/tools создают проверяемые evidence
→ агент формирует Decision Memo
→ человек утверждает/отклоняет/запрашивает доанализ
→ только после approval создаётся внешнее действие
```

C-level формулировка:

> Catman — не чат-бот и не «ИИ, который решает вместо бизнеса». Это управляемый AI Decision Room: агент исследует данные и готовит доказательное решение, а человек сохраняет право и ответственность за утверждение действия.

## 2. P0-сценарии

### 2.1 Morning Brief

Утренний brief с 3–7 приоритетными сигналами: KPI-отклонения, риски, аномалии, impact относительно плана и вопросы, требующие решения. Не dashboard dump и не общий пересказ.

### 2.2 Hypothesis / Root-Cause Analysis

Менеджер ставит вопрос «Почему изменился KPI?». Агент проверяет конкретные гипотезы: promotion depth, product mix, price, out-of-stock, channel/store/region effect, plan-vs-actual. Он обязан различать подтверждённые, неподтверждённые и непроверяемые выводы.

### 2.3 Evidence-first Decision Memo

Выход: сигнал, KPI/период, evidence, драйверы, варианты, рекомендация, ожидаемый эффект, риски, владелец, deadline, confidence и ограничения.

### 2.4 Human approval

Агент создаёт только draft: письмо, задачу, Excel/PPT output, request-for-change. Он не должен отправлять письмо, менять цены/ERP/CRM/промо или создавать внешнее обязательство без явного approve.

### 2.5 Demo-сюжет

```text
Morning Brief: gross margin категории Snacks ниже плана на 2.1 п.п.
→ менеджер: «Проверь promo depth, product mix и OOS. Дай только подтверждённые выводы».
→ агент вызывает разрешённые data-tools и SQL/Python analysis.
→ evidence: часть gap концентрируется в выбранном канале; низкомаржинальный mix/promo объясняет вклад; OOS high-margin SKU усиливает эффект.
→ агент отмечает, где причинность не доказана.
→ Decision Memo: две опции, expected impact, risk, owner.
→ manager approves draft action.
```

Это должен быть полностью реальный workflow на реалистичных, но синтетических данных.

## 3. Базовые решения и границы

### 3.1 Deterministic vs generative

`DECISION`: LLM не является источником истинных цифр и не должен быть калькулятором.

- LLM/agent: уточняет запрос, строит исследовательский план, выбирает разрешённые tools, синтезирует результат, объясняет ограничения, создаёт memo.
- SQL/Python/deterministic tools: считают KPI, margin decomposition, plan-vs-actual, сегментацию, OOS impact, statistical checks и exports.
- Semantic/KPI contract: хранит смысл метрики, формулу, source, owner, grain, freshness, ограничения.

### 3.2 Evidence-first

Каждый существенный вывод должен иметь evidence pack: источник и freshness, KPI definition, период/фильтры, tool/query/template ID, численные результаты, допущения и ограничения.

### 3.3 Read/write разделены

`DECISION`: MVP data-tools — read-only. Write-actions — отдельный слой с явным human approval.

### 3.4 RAG

`DECISION`: RAG не нужен для первой задачи «почему упала маржа». Позже это отдельный Knowledge & Policy skill для регламентов, стратегий, QBR, договоров, прошлых решений и SOP.

### 3.5 Оркестрация

`DECISION`: не начинать с multi-agent swarm, тяжёлых graph orchestration, LangGraph или n8n как «мозга».

- Skills + MCP + SQL/Python покрывают первый demo.
- n8n — позднее для schedules, integrations, approval, retries и write-actions.
- Graph — только при долгих процессах, ветвлении, нескольких ролях/правах, parallel tools и escalation.

## 4. Лёгкая MVP-архитектура

```text
Manager-facing runtime
(ChatGPT Work OR Claude Cowork OR OpenWork)
         │
         ├── Skills
         │   ├── Morning Brief
         │   ├── Hypothesis Analyst
         │   └── Decision Memo
         │
         └── MCP server
               ├── safe data tools
               ├── KPI contracts
               ├── SQLite demo database
               ├── SQL query templates
               ├── Python analytics
               ├── evidence pack
               └── export: Markdown / Excel / PPTX / draft task
```

### 4.1 Runtime strategy

`DECISION`: архитектура provider-agnostic. Главные активы лежат в Git, а не принадлежат одному UI/vendor.

- **Claude Cowork-first:** возможный быстрый путь к manager-facing demo.
- **ChatGPT Work/Enterprise:** важный enterprise-facing reference для Data Agent, Excel/PowerPoint, workspace agents и custom connectors; может требовать платного плана, admin approval и remote MCP.
- **OpenWork/OpenCode/Codex/OpenClaw-like:** local-first/self-hosted или developer/runtime proof; не обязательны для первой manager-facing записи.

`DECISION`: выбрать один основной runtime. Второй — только короткое доказательство переносимости, а не второй MVP.

### 4.2 Data layer

`DECISION`: первая БД — SQLite с synthetic data. Позднее: Postgres/DWH/Excel/CSV/Google Sheets/SharePoint/BI.

Ориентировочные таблицы:

- `fact_sales`: date, SKU, category, channel, store, units, revenue, discount, COGS, gross_margin
- `fact_inventory`: date, SKU, store, on_hand, OOS flag, days_of_supply
- `fact_promo`: promo, period, SKU, mechanic, discount, budget
- `fact_plan`: planned revenue, units, margin
- `dim_product`, `dim_store`, `dim_calendar`
- `kpi_dictionary`: formula, source, owner, grain, freshness, constraints

### 4.3 P0 MCP tools

```text
get_kpi_summary(period, category, channel)
compare_plan_actual(metric, period, dimensions)
analyze_margin_drivers(period, category, channel)
analyze_promo_effect(period, category, channel)
analyze_oos_impact(period, category, channel)
get_metric_definition(metric_id)
generate_evidence_pack(analysis_id)
create_decision_memo(analysis_id)
export_brief(format)
```

`DECISION`: не предоставлять unrestricted `run_sql(sql)` в MVP. Предпочтительны typed tools/safe templates. Если raw SQL нужен: SELECT-only, table/column allowlist, row/time limits, query log, запрет DDL/DML/ATTACH.

## 5. Переносимые артефакты

Целевая структура (ориентир):

```text
catman-decision-room/
├── skills/
│   ├── morning-brief/SKILL.md
│   ├── hypothesis-analyst/SKILL.md
│   └── decision-memo/SKILL.md
├── contracts/
│   ├── kpi_dictionary.yaml
│   ├── tool_permissions.yaml
│   └── decision_memo_schema.yaml
├── mcp-server/
│   ├── analytics.py
│   ├── sql_guard.py
│   ├── tools.py
│   └── evidence_pack.py
├── data/catman_demo.sqlite
├── evals/
│   ├── margin_decline_cases.json
│   └── expected_answers.json
└── demo/video-script.md
```

Уникальные активы Catman: domain skills, KPI/business contracts, deterministic data-tools, evidence policy, decision-memo schema, evaluation cases, permissions/approval model, demo scenarios и deliberately embedded anomalies.

## 6. Миссия исследования

Найти материалы, из которых Catman можно **собрать**, а не только концептуально обосновать. Не искать только по слову `Catman`; искать функциональные аналоги.

### A. Reuse Scout

Искать code/config/data assets:

- ChatGPT Work/Enterprise: Data Agent, Workspace Agents, Skills, Plugins, MCP/connectors, Excel/PowerPoint/data workflows
- Claude/Cowork/Desktop: Skills, MCP, files/data analysis, scheduled tasks, report generation
- Open-source/local-first: OpenWork, OpenCode, OpenClaw, OpenWorker, self-hosted agent workspaces
- agentic analytics, conversational BI, semantic layer, dbt, anomaly/root-cause, plan-vs-actual
- MCP for SQLite/Postgres/DuckDB/Excel/Google Sheets/Power BI/GitHub
- synthetic retail/sales/margin/inventory/promotion/supply-chain data
- safe SQL, evidence/citation, evals, decision memo, executive brief templates

### B. Video & UX Scout

Искать official demos, walkthroughs, conference talks и credible practitioner videos по:

- business question → data investigation → dashboard/insight → action
- morning brief/KPI alerts
- margin/sales/promo/mix/OOS/forecast/plan-vs-actual root cause
- Excel/PPT/decision memo/QBR output
- skills + MCP + SQL/Python
- local-first/self-hosted agent demos

Для каждого видео: URL, timestamp, scene description, Catman mapping, trust level, reuse idea.

### C. Reconstruction Architect

Только после A и B: выдать конкретный 1–3 day plan — что взять as-is, что адаптировать, что написать, как протестировать и как снять 5–7 minute demo. Выбрать один основной runtime.

## 7. Политика отбора

### Readiness

- **A:** use almost immediately
- **B:** light adaptation: configuration, schema, `SKILL.md`, MCP wrapper, output contract, synthetic data, permissions
- **C:** architecture idea only
- **D:** marketing/unverified/outdated/risky; do not use as a foundation

`DECISION`: искать A первым, но B обязательно рассматривать. Лучший MVP реалистично будет A + ограниченный B. Исключать B, если нужен runtime rewrite, heavy frontend, complex deployment, unclear license, major lock-in или unsafe data access.

### Full lifecycle vs partials

Highest priority:

```text
question → trusted data → analysis → evidence → recommendation → human-approved action
```

Но сильные частичные реализации обязательны: Morning Brief, anomaly detection, root cause, SQL/Python, semantic metrics, evidence, decision memo, Excel/PPT, approval, MCP, skills, evals/audit.

### Source policy

- Основа: публично проверяемые official docs/product demos, GitHub, public templates/datasets, talks, videos, case studies.
- Enterprise-only включать, если они официально публично описаны. Маркировать: `enterprise-only`, `paid plan`, `admin approval`, `preview/beta`, `availability unclear`.
- NDA/closed sources не использовать как доказательство, dependency или reusable asset; только как market signal при публичном упоминании.

### Required fields per asset

| Field | Requirement |
|---|---|
| Name / URL / author / date | mandatory |
| Type | product, OSS repo, template, docs, dataset, video, case study |
| Source reliability | official / credible practitioner / community / promotional |
| Catman layer | UX, skill, MCP, data, analytics, RAG, workflow, approval, output, eval, demo |
| Reuse | use-as-is / configure / adapt / rebuild |
| Readiness | A/B/C/D |
| License/terms | mandatory for code/data reuse |
| Demo value | low/medium/high |
| Time-to-demo | hours / 1 day / 2–3 days / >1 week |
| Risk | security, lock-in, stale API, unsupported, fake demo, unclear license |
| Priority | P0/P1/P2 |
| Exact next step | specific action |

Итог всегда делить на:

- **Track A — Build Now:** public/currently accessible demo components
- **Track B — Enterprise Reference:** C-level narrative/future roadmap, not MVP dependency

## 8. Video policy

`DECISION`: не копировать и не «перегенерировать» чужое product video. Другие видео — референсы для narrative, UX, pacing и scenes.

Core demo должен быть реальным screen recording:

```text
real runtime + real MCP + real SQLite + real SQL/Python + real evidence + real Decision Memo
```

Generative video допустим только для коротких нефункциональных переходов/открытия/абстрактной визуальной метафоры/voice support; не для интерфейса, чисел, таблиц, calculation flow или proof.

### Two-video strategy

1. **Business video (5–7 min):** CEO/COO/CCO. Morning Brief → Investigation → Evidence → Decision Memo → Approval. Не показывать terminal/Git/MCP config.
2. **Trust/architecture video:** CIO/CTO/CISO/Head of Data. Skill contract → MCP allowlist → SQLite/SQL truth → evidence pack → permissions → eval → portability.

Visual/narrative benchmark supplied by project owner:

`https://cdn.openai.com/devhub/videos-learn/chatgpt-work-overview-1080p-v1.mp4`

Найти функционально похожие публичные references; не предполагать, что файл можно переиспользовать.

## 9. C-level framing

Показывать:

- shorter `signal → analysis → decision → action`
- меньше ручного сбора/reconciliation/reporting
- единый смысл KPI и traceability
- быстрый evidence-based разбор margin/sales/promo/OOS/mix/plan risks
- human accountability and governance

Не лидировать с model names, swarm, LangGraph/n8n/terminal, claim «AI replaces managers» или неподтверждённым ROI.

Lead statement:

> Я создаю управляемые AI-системы, которые превращают корпоративные данные в проверяемые решения, а решения — в контролируемые действия.

## 10. Existing knowledge and precedence

Сначала читать `CATMAN_AI_BLUEPRINT.md` в этом репозитории. Сохранять его принятые решения, если данный документ не фиксирует более позднее упрощение именно для demo.

Внешний SSOT проекта `SSOT_Catman/` (может быть не зеркалирован в GitHub):

1. `doc-catman-ai-platform-2026-v1-001.md` — canonical AI platform concept/MVP scenes
2. `doc_20260915-retail-ai-needs-mapping-001.md` — canonical needs map
3. `doc_20260915-vertical-ai-agents-retail.md` — canonical market/vertical report
4. `catman-functionality-graph.md` — domain ontology/functionality graph
5. `doc_cdr-fdd-spec-002.md` — Category Decision Room FFD specification
6. `agent-brief-catman3-deep-research.md` — отдельный research brief по CMA CatMan 3.0 methodology/history; не смешивать с текущим reusable-assets research

Не скрывать tension:

- В старой platform-thinking могут быть n8n/LangChain/Streamlit/CopilotKit/PostgreSQL/Redis.
- Текущая demo decision намеренно легче: один runtime + skills + MCP + SQLite + SQL/Python + evidence + human approval.
- Light demo не отменяет enterprise architecture; это fast proof layer перед DWH, RBAC, observability, semantic layer и workflow orchestration.

## 11. Не-цели первого demo

- Universal autonomous business agent
- Production ERP/CRM write access
- Real customer data
- Full RAG/knowledge graph
- Multi-agent graph/swarm
- Custom frontend
- DWH migration
- Enterprise certification
- Causal certainty from correlational data

## 12. Evals and robustness gates

Synthetic data обязана содержать expected-truth scenarios:

- margin decline from lower-margin mix + promotion depth
- sales decline related to OOS rather than demand
- revenue up while profit down
- issue concentrated in channel/store/region, not universal

Pass criteria:

- agent uses approved tool to obtain figures
- cites evidence and filters/time period
- does not invent unavailable fields
- separates fact, hypothesis, recommendation, limitation
- does not claim causality without proper design
- does not execute write without approval
- outputs Decision Memo schema

## 13. Open questions

1. Какой runtime быстрее и надёжнее для первой screen-recorded demo: Claude Cowork, ChatGPT Work, OpenWork или иной совместимый environment?
2. Какой public MCP/template лучший secure starting point для read-only SQLite/DuckDB analytics?
3. Какой permissively licensed synthetic dataset/schema покрывает sales + COGS/margin + inventory/OOS + promotions + plan с минимальной адаптацией?
4. Какие public video scenes лучше всего иллюстрируют decision loop?
5. Какой skill/plugin format практичнее переносить между Claude, Codex/ChatGPT и local runtimes?
6. Для каждого selected runtime нужен ли remote MCP, и каков simplest secure demo deployment?
7. Какой Excel/PPT export route наиболее воспроизводим без enterprise-only dependency?
8. Какой minimal eval harness проверит tool selection, numerical truth, evidence и non-hallucination?
9. Какие существующие Catman SSOT assets можно маппить на три MVP skills, а не создавать заново?

## 14. Required deliverables from next agent

1. Executive Summary: top-10 reusable assets and what Catman avoids building
2. Reuse Matrix: asset, URL, type, layer, readiness, license, risk, priority, exact next step
3. Video Reference Library: video, URL, timestamp, scene, Catman mapping, trust, reuse idea
4. MVP Assembly Recommendation: selected runtime, ready components, adaptations, original work, S/M/L effort
5. Business Demo Script (5–7 min)
6. Trust/Architecture Demo Script
7. Five explicit research gaps

Report in Russian. Cite every material. Separate verified availability from announcement, preview, marketing claim and private/enterprise-only reference.

## 15. Fresh-agent prompt

```text
Read CATMAN_RESEARCH_BELIEF_STATE.md and CATMAN_AI_BLUEPRINT.md before doing anything.

Find and evaluate reusable public assets for Catman’s first working demo: code repos, MCP servers, skills/plugins, synthetic datasets, data-agent/analytics workflows, evaluation patterns and video scenes. Catman is a manager AI Decision Room: Morning Brief → business question → SQL/Python analysis via approved tools → evidence pack → Decision Memo → human approval.

Do not redesign the platform. Do not treat generic AI-agent content as relevant. Find components usable as-is or with light adaptation. Prioritize public, technically verifiable sources. Search full decision loops first but include strong partial modules. Deliver Build Now vs Enterprise Reference tracks, a reuse matrix, timestamped video library, one recommended 1–3 day MVP assembly plan, and demo scripts.
```