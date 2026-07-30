# Graph Report - rigos-hackathon-2026  (2026-07-28)

## Corpus Check
- 424 files · ~213,895 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2966 nodes · 5425 edges · 220 communities (178 shown, 42 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 228 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e1d56528`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- models/base.py
- Folder: backend/mao/models Code Inventory
- components.jsx
- adapters/__init__.py
- MaintenanceScheduler
- main.py
- Task
- Simulator
- layouts/index.js
- runtime.py
- ActionDB
- client.js
- ProductPage.jsx
- AIConfigGenerator
- chart-tooltip.jsx
- useChartStable
- ConfigService
- views/shared.jsx
- models.py
- get_session
- datetime
- NeonVectorStore
- Path
- charts/index.js
- services/__init__.py
- dependencies
- Assets Workspace Redesign — Industrial OS Spec
- adapters/maintenance_adapter.py
- ExecutionContext
- devDependencies
- AIInvestigationOS.jsx
- chart-phase.js
- StateManager
- PersistenceService
- BackendAPI
- frontend_services/agent_activity_adapter.py
- BackendAPI
- Executor
- memory/FILES.md
- ui/FILES.md
- kernel.py
- line.jsx
- Embedder
- Part 8: Interaction Model ⭐⭐⭐⭐⭐
- KnowledgeAgent
- catalog/index.js
- RefineryGenerator
- IncidentService
- Folder: frontend/src/redesign Code Inventory
- adapters/knowledge_agent_adapter.py
- ComputationEngine
- RevenueService
- ObjectContext.jsx
- chart-context.jsx
- SafetyAgent
- components.json
- time-series-chart-shell.jsx
- index.jsx
- DiagnosticAgent
- NotificationAgent
- KnowledgeRepository
- MAOKernel
- gsap
- Project_Code_Inventory_By_Folder/README.md
- adapters/backend_api_new.py
- frontend_services/maintenance_adapter.py
- ConnectionManager
- AssetRepository
- ._record_execution_sync
- AgentRegistry
- scripts
- ConnectionManager
- Folder: backend/services Code Inventory
- src/README.md
- frontend_services/digital_twin_adapter.py
- mao/README.md
- Project_Code_Inventory_Updated.md
- .__init__
- Phase 7 — E2E verification
- frontend/package.json
- frontend_services/agent_adapter.py
- frontend_services/dashboard_adapter.py
- computation_engine.py
- backend/api/README.md
- HealthService
- Folder: backend/api/adapters Code Inventory
- Folder: backend/api/adapters/frontend_services Code Inventory
- Scheduler
- TelemetryStore
- FaultInjector
- x-axis.jsx
- .get_agent_activity
- frontend_services/asset_adapter.py
- .get_incidents
- .get_reports
- frontend_services/control_adapter.py
- frontend_services/report_adapter.py
- startup_event
- Folder: backend/rag Code Inventory
- enums.py
- CommandPalette.jsx
- projection-config.js
- live-line-chart.jsx
- frontend_services/__init__.py
- fix_imports.py
- Folder: frontend/src/components/Operations Code Inventory
- workspaces.spec.js
- y-domain-utils.js
- cn
- use-animated-y-domains.js
- vite.config.js
- ProductShell.jsx
- projection-utils.js
- adapters/digital_twin_adapter.py
- 3. Design language
- RigOS Object Context
- migrations/FILES.md
- Folder: frontend/src/redesign/views Code Inventory
- Folder: backend/models Code Inventory
- Folder: frontend/src/design-system/catalog Code Inventory
- Assets Workspace Redesign — Industrial OS Spec
- 6. Component catalog
- Page audits
- use-highlight-segment.js
- Folder: backend/agents Code Inventory
- Folder: backend/mao/workflows Code Inventory
- Folder: frontend/src/design-system Code Inventory
- Folder: frontend/src/design-system/layouts Code Inventory
- refinery_geo.py
- RigOS Data Contract
- ExecutiveBriefing.jsx
- loading-sweep.jsx
- AgentRepository
- MemoryManager
- 7. Interaction model
- Folder: backend/database/repositories Code Inventory
- Folder: frontend Code Inventory
- Page adapter shapes (Epic 3)
- RigOS Design System
- chart-defs.js
- frontend_services/health_prediction_adapter.py
- 5. Reusable layouts (6 only — B3)
- events/FILES.md
- Folder: backend/simulator Code Inventory
- redesign/FILES.md
- DotMatrixGlobe.jsx
- RigOS Operating Model
- RigOS V2 design system
- assets/FILES.md
- LLMManager
- styles/FILES.md
- ASSETS_WORKSPACE_REDESIGN.md
- Epic 6 — Frontend performance budget
- WorkflowEngine
- use-animated-series-path.js
- React + Vite
- compilerOptions
- EventStore
- pages/FILES.md
- resourceAdapters.js
- test_incident_service.py
- @base-ui/react
- class-variance-authority
- clsx
- d3-array
- d3-shape
- @emotion/styled
- @fontsource-variable/geist
- lucide-react
- motion
- EventGenerator
- next-themes
- @number-flow/react
- @radix-ui/react-icons
- OperationsContext.jsx
- live-x-axis.jsx
- tailwindcss
- @visx/grid
- @visx/group
- @visx/responsive
- @visx/shape
- react
- react-hot-toast
- react-router-dom
- @tailwindcss/vite
- @visx/event

## God Nodes (most connected - your core abstractions)
1. `ConfigService` - 53 edges
2. `AgentResult` - 42 edges
3. `AIConfigGenerator` - 36 edges
4. `ComputationEngine` - 35 edges
5. `BackendAPI` - 34 edges
6. `BackendAPI` - 33 edges
7. `get_session()` - 33 edges
8. `useChartStable()` - 31 edges
9. `LLMManager` - 29 edges
10. `Folder: frontend/src/redesign Code Inventory` - 29 edges

## Surprising Connections (you probably didn't know these)
- `DiagnosticAgent` --uses--> `Agent`  [INFERRED]
  backend/agents/diagnostic.py → backend/agents/base.py
- `KnowledgeAgent` --uses--> `Agent`  [INFERRED]
  backend/agents/knowledge.py → backend/agents/base.py
- `NotificationAgent` --uses--> `Agent`  [INFERRED]
  backend/agents/notification.py → backend/agents/base.py
- `PlanningAgent` --uses--> `Agent`  [INFERRED]
  backend/agents/planning.py → backend/agents/base.py
- `PredictionAgent` --uses--> `Agent`  [INFERRED]
  backend/agents/prediction.py → backend/agents/base.py

## Import Cycles
- None detected.

## Communities (220 total, 42 thin omitted)

### Community 0 - "models/base.py"
Cohesion: 0.24
Nodes (13): Asset, AssetStatus, AssetType, IncidentSeverity, BaseModel, Enum, str, Unified base models - single source of truth. (+5 more)

### Community 1 - "Folder: backend/mao/models Code Inventory"
Cohesion: 0.25
Nodes (6): backend/mao/models/execution_report.py, backend/mao/models/notification.py, backend/mao/models/result.py, backend/mao/models/task.py, Folder: backend/mao/models Code Inventory, backend/mao/models

### Community 2 - "components.jsx"
Cohesion: 0.06
Nodes (33): clamp(), tone(), V2AIAgentCard(), V2AlertChip(), V2FacilityNode(), V2HealthRing(), V2ProgressIndicator(), V2RecommendationCard() (+25 more)

### Community 3 - "adapters/__init__.py"
Cohesion: 0.06
Nodes (35): get_agent_metrics(), get_agents(), Agent adapter using BackendAPI., Return monitor metrics calculated from the live state., Return registered agents and their latest execution state., get_assets(), Asset adapter using BackendAPI., Get all assets with telemetry history. (+27 more)

### Community 4 - "MaintenanceScheduler"
Cohesion: 0.12
Nodes (15): MaintenancePriority, MaintenanceScheduler, MaintenanceTask, Enum, str, Maintenance scheduling service., Assign maintenance team based on asset type., Generate maintenance description. (+7 more)

### Community 5 - "main.py"
Cohesion: 0.10
Nodes (37): list_asset_notes(), create_maintenance_work_order(), database_health(), export_report(), get_agent_activity(), get_agent_metrics(), get_agents(), get_asset_detail() (+29 more)

### Community 6 - "Task"
Cohesion: 0.11
Nodes (26): create_schema(), Event, BaseModel, BaseModel, Task, FlowWorkflow, GasWorkflow, intelligence_tasks() (+18 more)

### Community 7 - "Simulator"
Cohesion: 0.11
Nodes (15): Notification, NotificationService, NotificationSeverity, NotificationType, Enum, str, Real-time notification service., Simulator with proper incident cooldown and rate limiting. (+7 more)

### Community 8 - "layouts/index.js"
Cohesion: 0.20
Nodes (18): ApplicationShell(), ExecutiveLayout(), TABS, ExplorerLayout(), TABS, IncidentLayout(), TABS, InvestigationLayout() (+10 more)

### Community 9 - "runtime.py"
Cohesion: 0.07
Nodes (26): Agent, ABC, Every agent must return an AgentResult., Production Diagnostic Agent with dynamic thresholds., Knowledge agent shared by MAO workflows and Command Nexus., MaintenanceAgent, Production Maintenance Agent with dynamic priority levels., Maintenance agent using Gemini-generated priorities. (+18 more)

### Community 10 - "ActionDB"
Cohesion: 0.07
Nodes (29): KnowledgeSearchError, RuntimeError, Read-only Knowledge Base access through the shared MAO kernel., Raised when the registered knowledge retrieval path is unavailable., Return normalized Neon retrieval results from the registered KnowledgeAgent., search_knowledge(), approve_maintenance_work_order(), AssetNoteRequest (+21 more)

### Community 11 - "client.js"
Cohesion: 0.12
Nodes (19): api, approveWorkOrder(), askAssistant(), createWorkOrder(), getMaintenancePlan(), getPredictions(), Assistant(), prompts (+11 more)

### Community 12 - "ProductPage.jsx"
Cohesion: 0.10
Nodes (23): fleetHealthForScope(), refineriesForFacility(), telemetryForFacility(), assetLocation(), filterByFacility(), incidentLocation(), PATH_ALIASES, taskLocation() (+15 more)

### Community 13 - "AIConfigGenerator"
Cohesion: 0.07
Nodes (26): calculate_severity(), get_incidents(), Incident adapter with dynamic severity calculation from config., Get all incidents from the runtime., Calculate severity from event payload using dynamic thresholds from AI config., calculate_severity(), get_incidents(), Incident adapter with dynamic severity calculation from config. (+18 more)

### Community 14 - "chart-tooltip.jsx"
Cohesion: 0.13
Nodes (22): ChartConfigContext, DEFAULT_CHART_CONFIG, resolveTooltipBoxMotion(), useChartConfig(), chartCssVars, indicatorFadeGradientStops(), resolveVerticalFadeSides(), ChartTooltip() (+14 more)

### Community 15 - "useChartStable"
Cohesion: 0.15
Nodes (19): useChartStable(), useYScale(), Grid(), hideEdgeTicks(), resolveRowTickValues(), isTerminalMarkerPhaseVisible(), LineSeriesTerminalMarker(), LiveYAxis() (+11 more)

### Community 16 - "ConfigService"
Cohesion: 0.09
Nodes (16): PlanningAgent, Planning agent using Gemini-generated workflow sequences., ConfigService, Get thresholds - uses precomputed values for speed., Generate agent sequence for an incident type., Generate and cache operational configurations using Gemini., Generate priority level for an incident., Generate risk weights for different sensors. (+8 more)

### Community 17 - "views/shared.jsx"
Cohesion: 0.11
Nodes (29): getAssetHealth(), getAssetNotes(), getTwinAssets(), saveAssetNote(), normalizeAgentActivityRow(), telemetryToLivePoints(), DotMatrixGlobe, MetricWithProvenance() (+21 more)

### Community 18 - "models.py"
Cohesion: 0.11
Nodes (16): _ensure_vector_extension(), Development-only schema bootstrap. Production uses Alembic migrations., Return True when pgvector is available for the knowledge table., cached_query(), clear_cache(), get_session_context(), healthcheck(), _normalize_database_url() (+8 more)

### Community 19 - "get_session"
Cohesion: 0.16
Nodes (16): _format_time(), get_agent_activity(), get_agent_metrics(), _persisted_activity(), Activity view-model sourced from live MAO state and persisted audit events., Load immutable activity records without blocking live state rendering., Return the combined live MAO and persisted activity timeline., Return summary metrics from current MAO agent results. (+8 more)

### Community 20 - "datetime"
Cohesion: 0.13
Nodes (29): _action_step(), _agent_step(), get_execution_report_export(), get_execution_reports(), get_incident_audit(), get_incident_audit_detail(), get_live_investigation(), get_operations_live() (+21 more)

### Community 21 - "NeonVectorStore"
Cohesion: 0.09
Nodes (12): KnowledgeDB, KnowledgeIngestion, NeonVectorStore, Search by embedding vector., Return self for compatibility., Return a retriever interface., Create the vector store from a list of documents., Add documents to an existing vector store. (+4 more)

### Community 22 - "Path"
Cohesion: 0.15
Nodes (25): Check, join(), main(), Any, Phase 7 connectivity verification — run with backend on :8080.  Usage (from re, Report, request_json(), verify() (+17 more)

### Community 23 - "charts/index.js"
Cohesion: 0.12
Nodes (18): transitionWithDelay(), projectedHealthToChartRows(), RadarArea, RadarPoint, RadarAxis(), RadarChart(), defaultRadarColors, radarCssVars (+10 more)

### Community 24 - "services/__init__.py"
Cohesion: 0.08
Nodes (12): get_ai_config(), get_runtime(), Services module exports - NO circular imports., Get the AI Configuration Generator (singleton)., get_kernel(), get_simulator(), Lazy-initialize and return the shared MAO kernel., Lazy-initialize and return the shared simulator. (+4 more)

### Community 25 - "dependencies"
Cohesion: 0.09
Nodes (23): animejs, axios, @emotion/react, dependencies, animejs, axios, @emotion/react, @mui/icons-material (+15 more)

### Community 26 - "Assets Workspace Redesign — Industrial OS Spec"
Cohesion: 0.05
Nodes (42): 1. Is the Digital Twin big enough?, 1. Wireframe specification (desktop), 2. Information hierarchy, 2. Is there still wasted space?, 3. Does the explorer scale to 10,000 assets?, 3. Interaction flow, 4. Component list (catalog-aligned), 4. Is the inspector too tall? (+34 more)

### Community 27 - "adapters/maintenance_adapter.py"
Cohesion: 0.16
Nodes (19): approve_work_order(), create_work_order(), get_maintenance_plan(), _persisted_work_orders(), _priority_label(), Any, Read-only maintenance planning data from the shared MAO runtime., Load operator-created work orders from ActionDB. (+11 more)

### Community 28 - "ExecutionContext"
Cohesion: 0.12
Nodes (12): ExecutionContext, Register an agent result and update execution state., Calculate deterministic confidence from evidence quality.          Agent self-, ExecutionReport, BaseModel, Enum, str, TaskStatus (+4 more)

### Community 29 - "devDependencies"
Cohesion: 0.10
Nodes (21): eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks (+13 more)

### Community 30 - "AIInvestigationOS.jsx"
Cohesion: 0.16
Nodes (27): getAgentMetrics(), getAgents(), getIncidentAuditDetail(), getTelemetry(), recordOperatorAction(), searchKnowledge(), triggerIncident(), decisionEntriesFromIncident() (+19 more)

### Community 31 - "chart-phase.js"
Cohesion: 0.47
Nodes (4): DEFAULT_CHART_LIFECYCLE, isChartInteractionPhase(), resolveRestingChartPhase(), useChartPhaseOrchestrator()

### Community 33 - "PersistenceService"
Cohesion: 0.08
Nodes (18): is_database_configured(), True when DATABASE_URL was provided and a session factory exists., TelemetryDB, Create many telemetry readings in smaller batches., TelemetryRepository, get_persistence(), PersistenceService, Persistence service with buffer and sync saving. (+10 more)

### Community 34 - "BackendAPI"
Cohesion: 0.06
Nodes (21): BackendAPI, Get assets for a specific refinery., Get assets of a specific type in a refinery., Cached version of get_assets., Get all assets from all refineries with caching., Get health for a specific asset., Cached version of get_incidents., Get all incidents from the runtime with caching. (+13 more)

### Community 35 - "frontend_services/agent_activity_adapter.py"
Cohesion: 0.16
Nodes (12): _format_time(), get_agent_activity(), get_agent_metrics(), _persisted_activity(), Activity view-model sourced from live MAO state and persisted audit events., Load immutable activity records without blocking live state rendering., Return the combined live MAO and persisted activity timeline., Return summary metrics from current MAO agent results. (+4 more)

### Community 36 - "BackendAPI"
Cohesion: 0.06
Nodes (21): BackendAPI, Get assets of a specific type in a refinery., Cached version of get_assets., Get all assets from all refineries with caching., Cached version of get_asset_telemetry., Get telemetry history for an asset with caching., Get health for a specific asset., Single interface for frontend to access backend data with caching. (+13 more)

### Community 37 - "Executor"
Cohesion: 0.18
Nodes (11): AgentNotFound, MAOException, PolicyViolation, Base exception for the MAO Kernel., TaskExecutionFailed, ToolNotFound, WorkflowNotFound, Executor (+3 more)

### Community 38 - "memory/FILES.md"
Cohesion: 0.40
Nodes (3): backend/mao/memory/memory_manager.py, Folder: backend/mao/memory Code Inventory, backend/mao/memory

### Community 39 - "ui/FILES.md"
Cohesion: 0.40
Nodes (3): Folder: frontend/src/ui Code Inventory, frontend/src/ui/index.jsx, frontend/src/ui

### Community 41 - "line.jsx"
Cohesion: 0.19
Nodes (15): AreaGradientDefs(), DashTailStroke(), fadeGradientStops(), resolveFadeSides(), viewportFadeGradientAttrs(), Line(), LineLoadingPulseStroke(), resolveLineLoadingPulseMode() (+7 more)

### Community 42 - "Embedder"
Cohesion: 0.08
Nodes (9): Embedder, LangChain-compatible embedding proxy that rotates configured Gemini keys.      `, PDFLoader, DocumentLoader, RAGPipeline, Build a FAISS vector store from PDF files., DocumentSplitter, VectorStore (+1 more)

### Community 43 - "Part 8: Interaction Model ⭐⭐⭐⭐⭐"
Cohesion: 0.06
Nodes (31): 9. Architect verdict, Animation rules (Epic 4 enforcement), Blockers B1–B6 — CLOSED, Epic 0 — Contract freeze (NEW — required before Epic 1), Epic 0 re-review (post-contract), Epic 1 — Build the actual Design System ⭐⭐⭐⭐⭐, Epic 2 — Build the reusable layouts ⭐⭐⭐⭐⭐, Epic 3 — Rebuild pages using ONLY layouts + components ⭐⭐⭐⭐⭐ (+23 more)

### Community 44 - "KnowledgeAgent"
Cohesion: 0.11
Nodes (18): KnowledgeAgent, Retrieve refinery guidance for workflows and create grounded chat answers., Lazily load the persisted retrieval index and, for chat, Gemini., Support MAO workflow context and direct Command Nexus requests., ask_knowledge_agent(), _emit(), generate_conversational_response(), get_knowledge_agent() (+10 more)

### Community 45 - "catalog/index.js"
Cohesion: 0.07
Nodes (67): Dock(), DecisionButtonGroup(), FilterChipBar(), PrimaryCTA(), RationaleField(), ScenarioSlider(), EmptyState(), ForecastChart() (+59 more)

### Community 46 - "RefineryGenerator"
Cohesion: 0.29
Nodes (6): Asset, Generate realistic refinery assets for simulation., Generate multiple refineries with assets., Generate assets for a refinery., RefineryGenerator, Refinery

### Community 47 - "IncidentService"
Cohesion: 0.16
Nodes (10): _ApiProxy, _get_api_instance(), Unified backend API for frontend access with caching and refinery support., Trigger an incident and return formatted results., trigger_incident(), Trigger an incident and return formatted results., trigger_incident(), IncidentService (+2 more)

### Community 48 - "Folder: frontend/src/redesign Code Inventory"
Cohesion: 0.07
Nodes (29): Folder: frontend/src/redesign Code Inventory, frontend/src/redesign/accountability.css, frontend/src/redesign/accountability.jsx, frontend/src/redesign/ai-investigation.css, frontend/src/redesign/ambient.css, frontend/src/redesign/AssistantPanel.jsx, frontend/src/redesign/copilot.css, frontend/src/redesign/executive-briefing.css (+21 more)

### Community 49 - "adapters/knowledge_agent_adapter.py"
Cohesion: 0.21
Nodes (14): ask_knowledge_agent(), _emit(), generate_conversational_response(), get_knowledge_agent(), is_operational_query(), KnowledgeAgentUnavailable, ProgressCallback, RuntimeError (+6 more)

### Community 50 - "ComputationEngine"
Cohesion: 0.07
Nodes (19): ComputationEngine, Any, Calculate health based on telemetry violations., Computes health, failure probability, RUL in real-time., Calculate degradation rate from telemetry trends., Calculate failure probability from health and degradation., Calculate Remaining Useful Life in days., Calculate confidence based on sample count. (+11 more)

### Community 51 - "RevenueService"
Cohesion: 0.24
Nodes (6): Calculate revenue impact of a specific incident., Get daily revenue for an asset type., Calculate revenue impact for a single asset., Calculate total revenue impact across all assets., Calculate revenue impact based on asset health and incidents., RevenueService

### Community 52 - "ObjectContext.jsx"
Cohesion: 0.28
Nodes (7): defaultState, defaultTwinCamera, defaultTwinLayers, ObjectContext, ObjectProvider(), persistSession(), readSession()

### Community 53 - "chart-context.jsx"
Cohesion: 0.12
Nodes (19): clipRevealTransition(), DEFAULT_CHART_ENTER_TRANSITION, ChartHoverContext, ChartStableContext, defaultScatterColors, useChart(), useChartHover(), ChartLegendHoverContext (+11 more)

### Community 54 - "SafetyAgent"
Cohesion: 0.24
Nodes (5): Safety assessment agent using Gemini-generated thresholds., Get thresholds for the asset type., Extract asset type from context., Get risk weights for the incident type., SafetyAgent

### Community 55 - "components.json"
Cohesion: 0.09
Nodes (22): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+14 more)

### Community 56 - "time-series-chart-shell.jsx"
Cohesion: 0.10
Nodes (17): decimateTimeSeries(), maxRenderPointsForWidth(), filterDataByXDomain(), resolveBrushTrackXExtent(), resolveDataXExtent(), generateChartSkeletonData(), generateChartSkeletonFromTarget(), LineChartLoading() (+9 more)

### Community 58 - "DiagnosticAgent"
Cohesion: 0.27
Nodes (4): DiagnosticAgent, Diagnostic agent using Gemini-generated thresholds., Get thresholds for the asset type., Extract asset type from context.

### Community 59 - "NotificationAgent"
Cohesion: 0.28
Nodes (5): NotificationAgent, Create structured in-memory notifications from workflow metadata., Determine severity with dynamic thresholds., Notification, A structured operator notification held in StateManager memory.

### Community 60 - "KnowledgeRepository"
Cohesion: 0.20
Nodes (3): KnowledgeRepository, Return all knowledge chunks from the database., Delete all knowledge chunks from the database.

### Community 61 - "MAOKernel"
Cohesion: 0.13
Nodes (11): PredictionAgent, Extract asset type from context., Estimate health and risk from telemetry using dynamic thresholds., Calculate degradation rate using dynamic thresholds., MAOKernel, create_kernel(), get_kernel(), services/kernel_factory.py  Compatibility access point for the shared MAO kern (+3 more)

### Community 63 - "Project_Code_Inventory_By_Folder/README.md"
Cohesion: 0.08
Nodes (18): backend/agents, backend/data/ai_config.json, Folder: backend/data Code Inventory, backend/data, backend/.env.example, backend/fix_imports.py, backend/requirements.txt, backend/run.py (+10 more)

### Community 64 - "adapters/backend_api_new.py"
Cohesion: 0.21
Nodes (8): _ApiProxy, _as_naive_utc(), _get_api_instance(), _parse_iso(), Unified backend API for frontend access with caching and refinery support., Cached version of get_asset_telemetry., Get telemetry history for an asset; optional ISO since/until window., Normalize timestamps so since/until filters never mix aware and naive datetimes.

### Community 65 - "frontend_services/maintenance_adapter.py"
Cohesion: 0.29
Nodes (9): get_maintenance_plan(), _priority_label(), Any, Read-only maintenance planning data from the shared MAO runtime., Index completed agent output by its workflow task and assigned agent., Resolve an asset label only when it is present in live task/result data., Format state-manager tasks and agent output for the planner UI., _result_index() (+1 more)

### Community 66 - "ConnectionManager"
Cohesion: 0.31
Nodes (5): ConnectionManager, WebSocket, WebSocket manager for real-time updates., Legacy helper endpoint — production uses api.main.websocket_endpoint., websocket_endpoint()

### Community 67 - "AssetRepository"
Cohesion: 0.18
Nodes (7): AssetDB, AssetRepository, Optimized Asset Repository with batch operations., Batch insert for better performance., Bulk update asset health in one query., _persist_assets_to_database(), Persist all assets and refineries to database.

### Community 68 - "._record_execution_sync"
Cohesion: 0.17
Nodes (5): ExecutionReportDB, IncidentDB, IncidentRepository, ReportRepository, Sync version for execution.

### Community 70 - "scripts"
Cohesion: 0.20
Nodes (9): name, private, scripts, backend, build, dev, lint, preview (+1 more)

### Community 72 - "ConnectionManager"
Cohesion: 0.39
Nodes (4): ConnectionManager, WebSocket, Push operations snapshots every ~2s.      Must also await receive() — a send-o, websocket_endpoint()

### Community 73 - "Folder: backend/services Code Inventory"
Cohesion: 0.08
Nodes (25): backend/services/ai_config.py, backend/services/asset.py, backend/services/computation_engine.py, backend/services/config_services.py, backend/services/embedding.py, backend/services/health.py, backend/services/incident_manager.py, backend/services/incident_service.py (+17 more)

### Community 75 - "src/README.md"
Cohesion: 0.07
Nodes (21): Folder: frontend/src/api Code Inventory, frontend/src/api/client.js, frontend/src/api, Folder: frontend/src/context Code Inventory, frontend/src/context/breadcrumbs.js, frontend/src/context/ColorModeContext.jsx, frontend/src/context/ObjectContext.jsx, frontend/src/context/objectNavigation.js (+13 more)

### Community 78 - "frontend_services/digital_twin_adapter.py"
Cohesion: 0.38
Nodes (6): get_twin_assets(), _maintenance_recommendation(), Any, Read-only asset and telemetry view-model for the Digital Twin page., Return current assets and latest observed telemetry from the runtime., _reading_value()

### Community 79 - "mao/README.md"
Cohesion: 0.07
Nodes (19): backend/mao/core/context.py, backend/mao/core/exceptions.py, backend/mao/core/executor.py, backend/mao/core/logger.py, backend/mao/core/registry.py, backend/mao/core/scheduler.py, backend/mao/core/state_manager.py, Folder: backend/mao/core Code Inventory (+11 more)

### Community 80 - "Project_Code_Inventory_Updated.md"
Cohesion: 0.12
Nodes (13): Folder: frontend/e2e Code Inventory, frontend/e2e/workspaces.spec.js, frontend/e2e, Folder: frontend/public Code Inventory, frontend/public/favicon.svg, frontend/public/icons.svg, frontend/public, frontend (+5 more)

### Community 81 - ".__init__"
Cohesion: 0.11
Nodes (8): KernelLogger, EventBus, Planner, Any, mao/workflows/planner.py  Workflow Planner  Determines which workflow should, Selects the most appropriate workflow for an incoming event., Determine which workflow should handle an event.          Priority:, Infer workflow directly from telemetry.

### Community 82 - "Phase 7 — E2E verification"
Cohesion: 0.29
Nodes (6): Automated API checklist (`e2e_verify.py`), Fix for database blocker, Latest run (2026-07-27), Manual UI smoke (Playwright), Other fixes applied during verification, Phase 7 — E2E verification

### Community 83 - "frontend/package.json"
Cohesion: 0.17
Nodes (11): name, private, scripts, build, dev, lint, preview, test:e2e (+3 more)

### Community 84 - "frontend_services/agent_adapter.py"
Cohesion: 0.40
Nodes (5): get_agent_metrics(), get_agents(), Agent adapter using BackendAPI., Return monitor metrics calculated from the live state., Return registered agents and their latest execution state.

### Community 85 - "frontend_services/dashboard_adapter.py"
Cohesion: 0.40
Nodes (5): calculate_severity(), get_dashboard(), Dashboard adapter using BackendAPI., Get dashboard data using BackendAPI with caching., Calculate severity from event payload.

### Community 86 - "computation_engine.py"
Cohesion: 0.18
Nodes (9): BaseModel, Enum, str, Sensor, SensorType, Real-time computation engine - Runs every 10-15 seconds., Health service using the computation engine with AI-generated thresholds., Manual incident injection for the shared live simulator. (+1 more)

### Community 88 - "backend/api/README.md"
Cohesion: 0.11
Nodes (10): backend/api/adapters/frontend_services, backend/api/adapters, Subfolders, backend/api/main.py, Folder: backend/api Code Inventory, backend/api, Subfolders, backend/api/websocket/manager.py (+2 more)

### Community 89 - "HealthService"
Cohesion: 0.18
Nodes (6): HealthService, Calculate health from readings using AI-generated thresholds., Calculate health with custom limits (fallback method).                  Args:, Calculates asset health from recent telemetry using AI-generated thresholds., Get full health metrics for an asset using computation engine., Get cached health status for an asset.                  Args:             ass

### Community 90 - "Folder: backend/api/adapters Code Inventory"
Cohesion: 0.11
Nodes (18): backend/api/adapters/agent_activity_adapter.py, backend/api/adapters/agent_adapter.py, backend/api/adapters/asset_adapter.py, backend/api/adapters/backend_api_new.py, backend/api/adapters/control_adapter.py, backend/api/adapters/dashboard_adapter.py, backend/api/adapters/digital_twin_adapter.py, backend/api/adapters/health_adapter.py (+10 more)

### Community 91 - "Folder: backend/api/adapters/frontend_services Code Inventory"
Cohesion: 0.12
Nodes (17): backend/api/adapters/frontend_services/agent_activity_adapter.py, backend/api/adapters/frontend_services/agent_adapter.py, backend/api/adapters/frontend_services/asset_adapter.py, backend/api/adapters/frontend_services/backend_api_new.py, backend/api/adapters/frontend_services/control_adapter.py, backend/api/adapters/frontend_services/dashboard_adapter.py, backend/api/adapters/frontend_services/digital_twin_adapter.py, backend/api/adapters/frontend_services/health_adapter.py (+9 more)

### Community 95 - "x-axis.jsx"
Cohesion: 0.17
Nodes (15): LINE_LOADING_PULSE_EASE, allIndexLayouts(), binomial(), buildDataAlignedTicks(), composePositiveSum(), dedupeIndicesByLabel(), gapsToIndices(), indexGaps() (+7 more)

### Community 102 - "frontend_services/asset_adapter.py"
Cohesion: 0.50
Nodes (3): get_assets(), Asset adapter using BackendAPI., Get all assets with telemetry history.

### Community 110 - "frontend_services/control_adapter.py"
Cohesion: 0.50
Nodes (3): get_control_state(), Control adapter using BackendAPI., Return a facility snapshot derived from live state.

### Community 111 - "frontend_services/report_adapter.py"
Cohesion: 0.50
Nodes (3): get_reports(), Report adapter using BackendAPI., Get execution reports.

### Community 115 - "startup_event"
Cohesion: 0.67
Nodes (3): Report readiness without blocking the HTTP/WebSocket server., startup_event(), on_event

### Community 119 - "Folder: backend/rag Code Inventory"
Cohesion: 0.12
Nodes (17): backend/rag/chunker.py, backend/rag/citation.py, backend/rag/embedder.py, backend/rag/ingestion.py, backend/rag/__init__.py, backend/rag/knowledge.py, backend/rag/llm_manager.py, backend/rag/llm.py (+9 more)

### Community 120 - "enums.py"
Cohesion: 0.25
Nodes (9): AssetStatus, AssetType, FacilityStatus, IncidentSeverity, Enum, str, Incident, BaseModel (+1 more)

### Community 123 - "projection-config.js"
Cohesion: 0.16
Nodes (15): CLIP_EXCLUDED_COMPONENT_NAMES, isChartClipPassthrough(), isClipExcludedComponent(), isPostOverlayComponent(), isUnderlayComponent(), resolveChartChildElement(), UNDERLAY_COMPONENT_NAMES, extractProjectionLineConfigs() (+7 more)

### Community 124 - "live-line-chart.jsx"
Cohesion: 0.15
Nodes (9): ChartProvider(), DEFAULT_MARGIN, interpolateAtTime(), LiveLineChart(), LiveLineChartCore, resolveLiveTooltip(), extractReferenceAreaConfigs(), getChildComponentName() (+1 more)

### Community 127 - "Folder: frontend/src/components/Operations Code Inventory"
Cohesion: 0.12
Nodes (11): Folder: frontend/src/components/Operations Code Inventory, frontend/src/components/Operations/Assistant.jsx, frontend/src/components/Operations/CommandPalette.jsx, frontend/src/components/Operations/Primitives.jsx, frontend/src/components/Operations/System.jsx, frontend/src/components/Operations, frontend/src/components, Subfolders (+3 more)

### Community 129 - "y-domain-utils.js"
Cohesion: 0.22
Nodes (12): useChartInteraction(), defaultDedupeKey(), useScheduledTooltip(), buildYScalesForLines(), buildYScalesFromDomains(), getPrimaryYScale(), groupLinesByYAxisId(), normalizeYAxisId() (+4 more)

### Community 130 - "cn"
Cohesion: 0.19
Nodes (16): ChartLoadingLabel(), ChartInner(), DEFAULT_MARGIN, extractLineConfigs(), getChildComponentName(), LINE_DOMAIN_EXCLUDED_NAMES, LineChart(), registersLineDomain() (+8 more)

### Community 131 - "use-animated-y-domains.js"
Cohesion: 0.47
Nodes (8): lerpDomain(), snapDomains(), tweenDomains(), useAnimatedYDomains(), domainsEqual(), isYDomainTweenPhase(), resolveAnimatedYDestinationDomains(), shouldTweenYDomain()

### Community 160 - "ProductShell.jsx"
Cohesion: 0.11
Nodes (25): markNotificationsRead(), App(), createProductTheme(), PRODUCT_PATHS, RoutedApp(), ApplicationShell(), nav, ColorModeContext (+17 more)

### Community 161 - "projection-utils.js"
Cohesion: 0.38
Nodes (11): buildAutoFutureValues(), buildProjectionPath(), buildTargetPath(), computeProjectionAnchorTangentSlope(), intervalFromAdjacentRows(), intervalFromSeriesSpan(), linearRegressionSlope(), readDate() (+3 more)

### Community 162 - "adapters/digital_twin_adapter.py"
Cohesion: 0.31
Nodes (8): _failure_label(), get_twin_assets(), _maintenance_recommendation(), Any, Read-only asset and telemetry view-model for the Digital Twin page., Derive failure probability from computation engine; fall back to health-based es, Return current assets and latest observed telemetry from the runtime., _reading_value()

### Community 163 - "3. Design language"
Cohesion: 0.14
Nodes (14): 3. Design language, Cards, Control room principles, Dashboard density, Elevation, Enterprise principles, Grid, Icons (+6 more)

### Community 164 - "RigOS Object Context"
Cohesion: 0.14
Nodes (14): Application Shell responsibilities, Assets workspace extensions (Phase 0 freeze), Behavior rules, Breadcrumb resolver, Exit criteria (Assets Phase 0), Exit criteria (Epic 0), navigateTo options (Assets-related), Navigation API (+6 more)

### Community 165 - "migrations/FILES.md"
Cohesion: 0.14
Nodes (10): backend/database/migrations/env.py, backend/database/migrations/script.py.mako, Folder: backend/database/migrations Code Inventory, backend/database/migrations, Subfolders, backend/database/migrations/versions/0001_operational_records.py, backend/database/migrations/versions/0002_add_knowledge_source.py, backend/database/migrations/versions/0003_incident_outcome_snapshots.py (+2 more)

### Community 166 - "Folder: frontend/src/redesign/views Code Inventory"
Cohesion: 0.14
Nodes (14): Folder: frontend/src/redesign/views Code Inventory, frontend/src/redesign/views/AIInvestigationOS.jsx, frontend/src/redesign/views/AssetBottomWorkspace.jsx, frontend/src/redesign/views/AssetConsole.jsx, frontend/src/redesign/views/AssetExplorer.jsx, frontend/src/redesign/views/AssetObjectInspector.jsx, frontend/src/redesign/views/assets-workspace.css, frontend/src/redesign/views/DigitalTwinCanvas.jsx (+6 more)

### Community 167 - "Folder: backend/models Code Inventory"
Cohesion: 0.15
Nodes (13): backend/models/asset.py, backend/models/base.py, backend/models/enums.py, backend/models/event.py, backend/models/facility.py, backend/models/incident.py, backend/models/__init__.py, backend/models/maintenance.py (+5 more)

### Community 168 - "Folder: frontend/src/design-system/catalog Code Inventory"
Cohesion: 0.15
Nodes (13): Folder: frontend/src/design-system/catalog Code Inventory, frontend/src/design-system/catalog/actions.jsx, frontend/src/design-system/catalog/data.jsx, frontend/src/design-system/catalog/executive.jsx, frontend/src/design-system/catalog/index.js, frontend/src/design-system/catalog/investigation.jsx, frontend/src/design-system/catalog/objects.jsx, frontend/src/design-system/catalog/panels.jsx (+5 more)

### Community 169 - "Assets Workspace Redesign — Industrial OS Spec"
Cohesion: 0.05
Nodes (43): 1. Is the Digital Twin big enough?, 1. Wireframe specification (desktop), 2. Information hierarchy, 2. Is there still wasted space?, 3. Does the explorer scale to 10,000 assets?, 3. Interaction flow, 4. Component list (catalog-aligned), 4. Is the inspector too tall? (+35 more)

### Community 170 - "6. Component catalog"
Cohesion: 0.17
Nodes (12): 6. Component catalog, Actions, Composition rules, Data display, Epic 1 priority split, Executive, Investigation & AI, Objects & lists (+4 more)

### Community 171 - "Page audits"
Cohesion: 0.25
Nodes (8): 1. Command Center, 2. Assets (Digital Twin), 3. Incident Center, 4. AI Investigation, 5. Maintenance Planning, 6. Forecasting, 7. Executive Reports, Page audits

### Community 172 - "use-highlight-segment.js"
Cohesion: 0.39
Nodes (5): computeSegmentBounds(), INACTIVE_SEGMENT, HighlightSegment(), SeriesHighlightLayer(), useHighlightSegment()

### Community 173 - "Folder: backend/agents Code Inventory"
Cohesion: 0.17
Nodes (12): backend/agents/base.py, backend/agents/diagnostic.py, backend/agents/__init__.py, backend/agents/knowledge.py, backend/agents/maintenance.py, backend/agents/notification.py, backend/agents/planning.py, backend/agents/prediction.py (+4 more)

### Community 174 - "Folder: backend/mao/workflows Code Inventory"
Cohesion: 0.17
Nodes (12): backend/mao/workflows/flow_workflow.py, backend/mao/workflows/gas_workflow.py, backend/mao/workflows/intelligence_tasks.py, backend/mao/workflows/maintenance_workflow.py, backend/mao/workflows/planner.py, backend/mao/workflows/policy_engine.py, backend/mao/workflows/pressure_workflow.py, backend/mao/workflows/supervisor.py (+4 more)

### Community 175 - "Folder: frontend/src/design-system Code Inventory"
Cohesion: 0.17
Nodes (12): Folder: frontend/src/design-system Code Inventory, frontend/src/design-system/catalog.css, frontend/src/design-system/CatalogPreview.jsx, frontend/src/design-system/components.jsx, frontend/src/design-system/index.js, frontend/src/design-system/LayoutsPreview.jsx, frontend/src/design-system/motion.css, frontend/src/design-system/primitives.css (+4 more)

### Community 176 - "Folder: frontend/src/design-system/layouts Code Inventory"
Cohesion: 0.10
Nodes (15): frontend/src/design-system/catalog, Folder: frontend/src/design-system/layouts Code Inventory, frontend/src/design-system/layouts/ApplicationShell.jsx, frontend/src/design-system/layouts/ExecutiveLayout.jsx, frontend/src/design-system/layouts/ExplorerLayout.jsx, frontend/src/design-system/layouts/IncidentLayout.jsx, frontend/src/design-system/layouts/index.js, frontend/src/design-system/layouts/InvestigationLayout.jsx (+7 more)

### Community 177 - "refinery_geo.py"
Cohesion: 0.47
Nodes (5): format_display_location(), Any, Static geographic metadata for refinery names (keyed by asset.location)., Flatten geo fields for operations snapshot refinery rows., refinery_geo_payload()

### Community 178 - "RigOS Data Contract"
Cohesion: 0.20
Nodes (10): Canonical IDs (A4), Exit criteria (Epic 0), Mapping rules (adapters), Operator actions (A3 / A8), Principles, Provenance (A2), RigOS Data Contract, Snapshot top-level keys (+2 more)

### Community 179 - "ExecutiveBriefing.jsx"
Cohesion: 0.24
Nodes (12): exportReport(), getReports(), downloadReportExport(), downloadTextFile(), Card, CardSwap(), makeSlot(), placeNow() (+4 more)

### Community 181 - "loading-sweep.jsx"
Cohesion: 0.39
Nodes (7): BarLoadingSkeleton(), generateEasedGradientStops(), getSkeletonHeights(), getSkeletonSigns(), hashFract(), LineLoadingSweep(), LoadingSweepMask()

### Community 184 - "7. Interaction model"
Cohesion: 0.22
Nodes (9): 7. Interaction model, Breadcrumbs, Epic 3 AuditSpine rule, Epic 3 CTA rule, In-place vs navigate, Keyboard, ObjectInspector sections (asset), Persistence keys (ObjectContext) (+1 more)

### Community 185 - "Folder: backend/database/repositories Code Inventory"
Cohesion: 0.08
Nodes (20): backend/database/base.py, backend/database/bootstrap.py, backend/database/connection.py, backend/database/__init__database.py, backend/database/__init__.py, backend/database/models.py, backend/database/seed_demo.py, Folder: backend/database Code Inventory (+12 more)

### Community 186 - "Folder: frontend Code Inventory"
Cohesion: 0.22
Nodes (9): Folder: frontend Code Inventory, frontend/eslint.config.js, frontend/.gitignore, frontend/index.html, frontend/package.json, frontend/PERFORMANCE.md, frontend/playwright.config.js, frontend/README.md (+1 more)

### Community 187 - "Page adapter shapes (Epic 3)"
Cohesion: 0.25
Nodes (8): Assets, Command Center, Forecasting, Incidents, Investigation, Maintenance, Page adapter shapes (Epic 3), Reports

### Community 188 - "RigOS Design System"
Cohesion: 0.25
Nodes (8): 1. Migration decision (B5), 2. Naming: ObjectInspector vs WorkspacePanel (B1), 4. Application Shell (Epic 2), 8. Route map (canonical), 9. Error / empty / stale, Primitive → catalog migration map, Related contracts, RigOS Design System

### Community 190 - "chart-defs.js"
Cohesion: 0.50
Nodes (7): collectChartDefsChildren(), getChartChildComponentName(), isChartDefsComponent(), isGradientDefComponent(), isPatternDefComponent(), partitionChartDefNodes(), VISX_PATTERN_COMPONENT_NAMES

### Community 191 - "frontend_services/health_prediction_adapter.py"
Cohesion: 0.40
Nodes (5): format_telemetry(), get_health_prediction(), Health prediction using computation engine., Format telemetry for display., Get health prediction using the computation engine.

### Community 192 - "5. Reusable layouts (6 only — B3)"
Cohesion: 0.29
Nodes (7): 5. Reusable layouts (6 only — B3), ExecutiveLayout, ExplorerLayout (Assets + Forecast), IncidentLayout, InvestigationLayout, KanbanLayout, MissionControlLayout

### Community 193 - "events/FILES.md"
Cohesion: 0.29
Nodes (5): backend/mao/events/event_bus.py, backend/mao/events/event.py, backend/mao/events/event_store.py, Folder: backend/mao/events Code Inventory, backend/mao/events

### Community 194 - "Folder: backend/simulator Code Inventory"
Cohesion: 0.20
Nodes (8): backend/simulator/asset.py, backend/simulator/event_generator.py, backend/simulator/facility.py, backend/simulator/fault_injector.py, backend/simulator/sensor.py, backend/simulator/simulator.py, Folder: backend/simulator Code Inventory, backend/simulator

### Community 195 - "redesign/FILES.md"
Cohesion: 0.29
Nodes (3): frontend/src/redesign, Subfolders, frontend/src/redesign/views

### Community 196 - "DotMatrixGlobe.jsx"
Cohesion: 0.50
Nodes (6): buildDots(), projectLatLng(), siteWeight(), angularDistanceDeg(), cellCenter(), isLand()

### Community 197 - "RigOS Operating Model"
Cohesion: 0.33
Nodes (5): Data provenance, Hackathon scope and future production work, Operational guardrails, RigOS Operating Model, What RigOS demonstrates

### Community 198 - "RigOS V2 design system"
Cohesion: 0.33
Nodes (5): Adoption contract, Architecture decisions, Primitives, RigOS V2 design system, State language

### Community 200 - "assets/FILES.md"
Cohesion: 0.33
Nodes (4): Folder: frontend/src/assets Code Inventory, frontend/src/assets/react.svg, frontend/src/assets/vite.svg, frontend/src/assets

### Community 202 - "LLMManager"
Cohesion: 0.06
Nodes (23): Quota-aware Gemini embeddings with the same key rotation policy as chat., Compatibility export for the centralized LLM service., Compatibility export for the centralized LLM service., _has_invalid_gemini_proxy(), KeyStatus, LLMManager, any, RateLimiter (+15 more)

### Community 203 - "styles/FILES.md"
Cohesion: 0.33
Nodes (4): Folder: frontend/src/styles Code Inventory, frontend/src/styles/premium.css, frontend/src/styles/theme.js, frontend/src/styles

### Community 204 - "ASSETS_WORKSPACE_REDESIGN.md"
Cohesion: 0.33
Nodes (4): Cross-cutting failures, Executive verdict, Redesign roadmap (product), RigOS Product Audit

### Community 205 - "Epic 6 — Frontend performance budget"
Cohesion: 0.40
Nodes (4): Epic 6 — Frontend performance budget, Implemented, Measure, Targets

### Community 208 - "use-animated-series-path.js"
Cohesion: 0.67
Nodes (5): computeSeriesPathPoints(), interpolateSeriesPathPoints(), seriesPathFromPoints(), seriesPathTransitionSignature(), useAnimatedSeriesPath()

### Community 209 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 210 - "compilerOptions"
Cohesion: 0.33
Nodes (5): compilerOptions, ignoreDeprecations, paths, include, src

### Community 213 - "pages/FILES.md"
Cohesion: 0.33
Nodes (4): Folder: frontend/src/pages Code Inventory, frontend/src/pages/live-investigation.css, frontend/src/pages/mission-control.css, frontend/src/pages

### Community 216 - "resourceAdapters.js"
Cohesion: 0.26
Nodes (11): enrichRefineryGeo(), facilityOptionsFromRefineries(), mergeAssetsWithTwin(), normalizePredictionResponse(), normalizeRefineryOptions(), normalizeTwinAsset(), parsePercent(), parseRulDays() (+3 more)

### Community 218 - "test_incident_service.py"
Cohesion: 0.14
Nodes (20): Asset, AssetStatus, AssetType, BaseModel, Enum, str, Refinery, Facility (+12 more)

### Community 228 - "EventGenerator"
Cohesion: 0.18
Nodes (6): EventGenerator, Optimized event generator - ONLY generates events from injected faults., Add a fault that will generate an event., ✅ ONLY generate events from injected faults.         No auto-detection from tel, Clear all stored faults., test_pressure_sensor_enum_generates_pressure_spike_event()

### Community 232 - "OperationsContext.jsx"
Cohesion: 0.27
Nodes (9): getOperationsLive(), collectionKeys, emptySnapshot, mergeOperations(), objectKeys, OperationsContext, OperationsProvider(), resolveWsUrl() (+1 more)

### Community 233 - "live-x-axis.jsx"
Cohesion: 0.22
Nodes (6): hmsTimeFmt, shortDateFmt, weekdayDateFmt, crosshairSpringConfig, LiveXAxis(), LiveXAxisInner

## Knowledge Gaps
- **660 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+655 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AIConfigGenerator` connect `AIConfigGenerator` to `Task`, `Simulator`, `runtime.py`, `LLMManager`, `ComputationEngine`, `RevenueService`, `computation_engine.py`, `services/__init__.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `ConfigService` connect `ConfigService` to `adapters/backend_api_new.py`, `BackendAPI`, `BackendAPI`, `runtime.py`, `LLMManager`, `AIConfigGenerator`, `IncidentService`, `SafetyAgent`, `services/__init__.py`, `DiagnosticAgent`, `NotificationAgent`, `MAOKernel`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `gsap`, `frontend/package.json`, `@base-ui/react`, `class-variance-authority`, `clsx`, `d3-array`, `d3-shape`, `@emotion/styled`, `@fontsource-variable/geist`, `lucide-react`, `motion`, `next-themes`, `@number-flow/react`, `@radix-ui/react-icons`, `tailwindcss`, `@visx/grid`, `@visx/group`, `@visx/responsive`, `@visx/shape`, `react`, `react-hot-toast`, `react-router-dom`, `@tailwindcss/vite`, `@visx/event`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ConfigService` (e.g. with `DiagnosticAgent` and `MaintenanceAgent`) actually correct?**
  _`ConfigService` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `AgentResult` (e.g. with `Agent` and `DiagnosticAgent`) actually correct?**
  _`AgentResult` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `AIConfigGenerator` (e.g. with `LLMManager` and `ComputationEngine`) actually correct?**
  _`AIConfigGenerator` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ComputationEngine` (e.g. with `AIConfigGenerator` and `HealthService`) actually correct?**
  _`ComputationEngine` has 3 INFERRED edges - model-reasoned connections that need verification._