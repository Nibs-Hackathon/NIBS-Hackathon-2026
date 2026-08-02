import { useEffect, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import {
  AssignmentOutlined,
  AttachMoneyOutlined,
  AutoAwesomeOutlined,
  BuildOutlined,
  PendingActionsOutlined,
  ScheduleOutlined,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useOperations } from '../../context/OperationsContext';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { approveWorkOrder, createWorkOrder, transitionWorkOrder } from '../../api/client';
import { KanbanLayout } from '../../design-system/layouts';
import { Status, Empty } from './shared';

function MaintenanceKpi({ icon: Icon, label, value, detail, tone = 'blue' }) {
  return (
    <Paper className={`maintenance-kpi tone-${tone}`}>
      <Box className="maintenance-kpi-icon"><Icon /></Box>
      <Box>
        <Typography>{label}</Typography>
        <b>{value}</b>
        <small>{detail}</small>
      </Box>
    </Paper>
  );
}

function normalizeTask(task, index) {
  return {
    ...task,
    id: task.id || `task-${index}`,
    title: task.title || task['Work order'] || task.Task || task.name || `Work order ${index + 1}`,
    priority: task.priority || task.Priority || 'P2',
    owner: task.owner || task.Owner || 'Unassigned crew',
    status: task.status || task.State || task.Status || 'Ready',
    cost: task.estimated_cost ?? task.cost ?? null,
    downtime: task.estimated_downtime || task.downtime || task['Estimated downtime'] || null,
    assetId: task.asset_id || task.assetId || null,
    incidentId: task.incident_id || task.incidentId || null,
    assetName: task.Asset || task.asset || task.assetName || null,
    source: task.source || null,
  };
}

function matchesColumn(status, column) {
  const value = String(status || '').toLowerCase().trim();
  switch (column.toLowerCase()) {
    case 'backlog':
      return value === 'backlog' || value === 'new' || value.includes('planning failed');
    case 'ready':
    case 'needs approval':
      return value.includes('ready') || value.includes('pending_approval') || value === 'pending';
    case 'scheduled':
      return value.includes('scheduled') || value.includes('approved');
    case 'in progress':
      return value === 'in progress' || value === 'in_progress'
        || value.includes('in progress') || value.includes('in_progress');
    case 'complete':
      return value.includes('complete') || value.includes('done') || value.includes('closed');
    default:
      return false;
  }
}

function isPersistedWorkOrderId(id) {
  const value = String(id || '');
  return value && !/^(task-|draft-|plan-|wo-)/.test(value);
}

const QUEUE_FILTERS = [
  { key: 'all', label: 'All work' },
  { key: 'approval', label: 'Needs approval' },
  { key: 'scheduled', label: 'Scheduled' },
  { key: 'active', label: 'In progress' },
  { key: 'complete', label: 'Complete' },
];

const KANBAN_COLUMNS = ['Backlog', 'Needs approval', 'Scheduled', 'In progress', 'Complete'];

export function MaintenancePlanning({ maintenance }) {
  const navigate = useNavigate();
  const { refresh } = useOperations();
  const objectApi = useObjectContext();
  const plan = maintenance;
  const [busy, setBusy] = useState(false);
  const [queueFilter, setQueueFilter] = useState('all');
  const draft = objectApi.draft?.workOrder;

  const refreshPlan = () => {
    refresh().catch(() => {});
  };

  useEffect(() => {
    refresh().catch(() => {});
  }, [refresh]);

  const tasks = Array.isArray(plan?.tasks) ? plan.tasks : [];
  const baseWork = tasks.map(normalizeTask);
  const work = draft && !baseWork.some((item) => item.id === draft.id)
    ? [{ ...normalizeTask(draft, 0), status: draft.status || 'Backlog' }, ...baseWork]
    : baseWork;
  const [selected, setSelected] = useState(objectApi.selection.workOrderId || draft?.id || null);
  const selectedWork = work.find((item) => item.id === selected) || work[0];
  const selectedIsApproved = Boolean(
    selectedWork
    && isPersistedWorkOrderId(selectedWork.id)
    && matchesColumn(selectedWork.status, 'Scheduled'),
  );
  const selectedIsInProgress = Boolean(selectedWork && matchesColumn(selectedWork.status, 'In progress'));
  const selectedIsComplete = Boolean(selectedWork && matchesColumn(selectedWork.status, 'Complete'));

  const chooseWork = (id) => {
    setSelected(id);
    objectApi.setSelection({ workOrderId: id });
  };

  const handleCreate = async () => {
    setBusy(true);
    try {
      const response = await createWorkOrder({
        asset_id: objectApi.selection.assetId || null,
        title: 'New reliability work order',
        priority: 'P2',
        owner: 'Control operator',
        note: 'Created from maintenance planning board.',
      });
      const created = response.data || {};
      objectApi.setDraftWorkOrder({
        id: created.id,
        title: created.title,
        status: 'Ready',
        priority: created.priority || 'P2',
        owner: created.owner || 'Control operator',
        cost: created.estimated_cost,
        downtime: created.downtime,
        assetId: created.asset_id,
        incidentId: created.incident_id,
      });
      chooseWork(created.id);
      refreshPlan();
      toast.success('Work order created');
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || 'Work order could not be created');
    } finally {
      setBusy(false);
    }
  };

  const handleApprove = async () => {
    if (!selectedWork?.id) return;
    setBusy(true);
    try {
      let workOrderId = selectedWork.id;
      if (!isPersistedWorkOrderId(workOrderId) || selectedWork.source === 'mao_plan') {
        const response = await createWorkOrder({
          asset_id: selectedWork.assetId || selectedWork.asset_id || objectApi.selection.assetId || null,
          incident_id: selectedWork.incidentId || selectedWork.incident_id
            || objectApi.selection.incidentId || null,
          title: selectedWork.title,
          priority: selectedWork.priority || 'P2',
          owner: selectedWork.owner || 'Control operator',
          downtime: selectedWork.downtime || undefined,
          estimated_cost: selectedWork.cost != null ? Number(selectedWork.cost) : undefined,
          note: 'Persisted from maintenance plan before approval.',
        });
        workOrderId = response.data?.id;
        if (!workOrderId) throw new Error('Work order could not be persisted');
        chooseWork(workOrderId);
      }
      await approveWorkOrder(workOrderId, {
        operator: 'Maintenance lead',
        note: `Approval requested for ${selectedWork.title}`,
      });
      refreshPlan();
      toast.success('Work order approved');
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || error.message || 'Approval failed');
    } finally {
      setBusy(false);
    }
  };

  const handleTransition = async (status) => {
    if (!selectedWork?.id || !isPersistedWorkOrderId(selectedWork.id)) return;
    setBusy(true);
    try {
      const response = await transitionWorkOrder(selectedWork.id, {
        status,
        operator: 'Maintenance lead',
        note: status === 'completed'
          ? `Field work completed for ${selectedWork.title}`
          : `Field crew started ${selectedWork.title}`,
      });
      await refresh();
      const incidentResolved = Boolean(response.data?.incident_resolution?.resolved);
      toast.success(
        status === 'completed'
          ? incidentResolved
            ? 'Work completed and linked incident resolved'
            : 'Work order completed'
          : 'Field work started',
      );
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || 'Work order status could not be updated');
    } finally {
      setBusy(false);
    }
  };

  const plannedCost = work.reduce((sum, item) => sum + Number(item.cost || 0), 0);
  const openWork = work.filter((item) => !matchesColumn(item.status, 'Complete'));
  const approvalQueue = work.filter((item) => matchesColumn(item.status, 'Ready'));
  const scheduledWork = work.filter((item) => (
    matchesColumn(item.status, 'Scheduled') || matchesColumn(item.status, 'In progress')
  ));
  const nextDowntime = work.find((item) => item.downtime)?.downtime || 'Not assessed';
  const filteredWork = work.filter((item) => {
    if (queueFilter === 'approval') return matchesColumn(item.status, 'Ready');
    if (queueFilter === 'scheduled') return matchesColumn(item.status, 'Scheduled');
    if (queueFilter === 'active') return matchesColumn(item.status, 'In progress');
    if (queueFilter === 'complete') return matchesColumn(item.status, 'Complete');
    return true;
  });
  const visibleColumns = queueFilter === 'approval'
    ? ['Needs approval']
    : queueFilter === 'scheduled'
      ? ['Scheduled']
      : queueFilter === 'active'
        ? ['In progress']
        : queueFilter === 'complete'
          ? ['Complete']
          : KANBAN_COLUMNS;

  const columnContent = Object.fromEntries(visibleColumns.map((column) => {
    const items = filteredWork.filter((item) => matchesColumn(item.status, column));
    return [column, items.length ? items.map((item) => (
      <button
        type="button"
        key={item.id}
        onClick={() => chooseWork(item.id)}
        className={`maintenance-kanban-card ${selectedWork?.id === item.id ? 'selected' : ''}`}
      >
        <span className={`maintenance-priority-badge ${String(item.priority).toLowerCase()}`}>
          {item.priority}
        </span>
        <span className="maintenance-kanban-identity">
          <b>{item.title}</b>
          <small>{item.assetName || item.assetId || 'Asset assignment pending'}</small>
        </span>
        <Status state={item.status} />
        <span className="maintenance-kanban-meta">
          <span>{item.owner || 'Unassigned crew'}</span>
          <span>{item.downtime || 'Window TBD'}</span>
          <span>{item.cost != null ? `$${Number(item.cost).toLocaleString()}` : 'Cost TBD'}</span>
        </span>
      </button>
    )) : (
      <Typography className="maintenance-column-empty">No work in this stage</Typography>
    )];
  }));

  const toolbar = (
    <Box className="maintenance-toolbar">
      <Box className="maintenance-planner-head">
        <Box>
          <Typography className="product-kicker">MAINTENANCE PLANNING</Typography>
          <Typography className="maintenance-planner-title">Reliability work control</Typography>
          <Typography className="maintenance-planner-subtitle">
            Prioritize, approve, and track field work from one operating queue.
          </Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Button size="small" variant="contained" startIcon={<BuildOutlined />} disabled={busy} onClick={handleCreate}>
            Create work order
          </Button>
          {selectedWork?.assetId || selectedWork?.asset_id ? (
            <Button
              size="small"
              onClick={() => navigateTo(objectApi, navigate, 'assets', {
                assetId: selectedWork.assetId || selectedWork.asset_id,
              })}
            >
              Open twin
            </Button>
          ) : null}
        </Stack>
      </Box>

      <Box className="maintenance-kpis">
        <MaintenanceKpi icon={AssignmentOutlined} label="Open work orders" value={openWork.length} detail={`${work.length} total records`} />
        <MaintenanceKpi icon={PendingActionsOutlined} label="Approval queue" value={approvalQueue.length} detail={approvalQueue.length ? 'Operator review required' : 'Nothing waiting'} tone="amber" />
        <MaintenanceKpi icon={ScheduleOutlined} label="Scheduled work" value={scheduledWork.length} detail={nextDowntime} tone="violet" />
        <MaintenanceKpi icon={AttachMoneyOutlined} label="Planned cost" value={plannedCost ? `$${plannedCost.toLocaleString()}` : 'Not costed'} detail={plannedCost ? 'Current scoped estimate' : 'Awaiting cost assessment'} tone="green" />
      </Box>

      <Box className="maintenance-queue-filters" role="group" aria-label="Work order status">
        {QUEUE_FILTERS.map((filter) => (
          <Button
            key={filter.key}
            className={queueFilter === filter.key ? 'active' : ''}
            onClick={() => setQueueFilter(filter.key)}
          >
            {filter.label}
          </Button>
        ))}
        <Typography className="maintenance-visible-count">{filteredWork.length} visible</Typography>
      </Box>
    </Box>
  );

  const inspector = selectedWork ? (
    <Paper className="maintenance-inspector">
      <Box className="maintenance-inspector-head">
        <Box>
          <Typography className="product-kicker">WORK ORDER INSPECTOR</Typography>
          <Typography className="maintenance-work-title">{selectedWork.title}</Typography>
        </Box>
        <Status state={selectedWork.status} />
      </Box>
      <Typography className="maintenance-inspector-asset">
        {selectedWork.assetName || selectedWork.assetId || 'Asset assignment pending'}
      </Typography>
      <Box className="maintenance-facts">
        <Box><span>Priority</span><b>{selectedWork.priority}</b></Box>
        <Box><span>Crew</span><b>{selectedWork.owner}</b></Box>
        <Box><span>Cost</span><b>{selectedWork.cost != null ? `$${Number(selectedWork.cost).toLocaleString()}` : 'Not costed'}</b></Box>
        <Box><span>Downtime</span><b>{selectedWork.downtime || 'Not assessed'}</b></Box>
      </Box>
      <Box className="maintenance-ai">
        <AutoAwesomeOutlined />
        <Box>
          <Typography className="product-kicker">AI SUGGESTED PLAN</Typography>
          <Typography>{plan?.rationale?.[0] || 'No AI schedule rationale published for this work order yet.'}</Typography>
        </Box>
      </Box>
      <Box className="maintenance-checklist">
        <Typography className="product-kicker">DEPENDENCIES & APPROVALS</Typography>
        <Typography><i />Status <b>{selectedWork.status}</b></Typography>
        <Typography><i />Asset <b>{selectedWork.assetName || selectedWork.assetId || 'Unassigned'}</b></Typography>
        <Typography><i />Source <b>{selectedWork.source || 'maintenance plan'}</b></Typography>
      </Box>
      <Stack spacing={1}>
        {!selectedIsApproved && !selectedIsInProgress && !selectedIsComplete && (
          <Button variant="contained" fullWidth disabled={busy} onClick={handleApprove}>
            Approve work order
          </Button>
        )}
        {selectedIsApproved && (
          <Button variant="contained" fullWidth disabled={busy} onClick={() => handleTransition('in_progress')}>
            Start field work
          </Button>
        )}
        {selectedIsInProgress && (
          <Button variant="contained" color="success" fullWidth disabled={busy} onClick={() => handleTransition('completed')}>
            Complete work order
          </Button>
        )}
        {selectedIsComplete && <Status state="Completed" />}
        <Typography variant="caption" color="text.secondary">
          Approval authorizes scheduling. Start and completion actions update the audit record; RigOS does not directly command equipment.
        </Typography>
        {(selectedWork.assetId || selectedWork.asset_id) && (
          <Button
            fullWidth
            onClick={() => navigateTo(objectApi, navigate, 'assets', {
              assetId: selectedWork.assetId || selectedWork.asset_id,
            })}
          >
            Open asset twin
          </Button>
        )}
      </Stack>
    </Paper>
  ) : <Empty text="maintenance" />;

  return (
    <Box className="maintenance-planner">
      <KanbanLayout
        className="maintenance-kanban-layout"
        toolbar={toolbar}
        columns={visibleColumns}
        columnContent={columnContent}
        board={filteredWork.length ? undefined : <Empty text="maintenance" />}
        inspector={inspector}
      />

      <Paper className="maintenance-bottom">
        <Box>
          <Typography className="product-kicker">PLAN RATIONALE</Typography>
          {(Array.isArray(plan?.rationale) && plan.rationale.length
            ? plan.rationale
            : ['No maintenance rationale published yet.']
          ).slice(0, 3).map((line) => (
            <Typography key={String(line).slice(0, 40)}>{String(line)}</Typography>
          ))}
        </Box>
        <Box>
          <Typography className="product-kicker">PRIORITY & DOWNTIME</Typography>
          <Typography>Plan priority <b>{plan?.priority || 'Not assessed'}</b></Typography>
          <Typography>Estimated downtime <b>{plan?.downtime || 'Not assessed'}</b></Typography>
        </Box>
      </Paper>
    </Box>
  );
}
