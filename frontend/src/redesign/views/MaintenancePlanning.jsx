import { useEffect, useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { BuildOutlined, MoreHorizOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { approveWorkOrder, createWorkOrder, getMaintenancePlan } from '../../api/client';
import { Metric, Status, Empty } from './shared';

function normalizeTask(task, index) {
  return {
    ...task,
    id: task.id || `task-${index}`,
    title: task.title || task['Work order'] || task.Task || task.name || `Work order ${index + 1}`,
    priority: task.priority || task.Priority || 'P2',
    owner: task.owner || task.Owner || '—',
    status: task.status || task.State || task.Status || 'Ready',
    cost: task.estimated_cost ?? task.cost ?? null,
    downtime: task.estimated_downtime || task.downtime || task['Estimated downtime'] || null,
    assetId: task.asset_id || task.assetId || null,
    assetName: task.Asset || task.asset || task.assetName || null,
  };
}

export function MaintenancePlanning({ maintenance }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const [plan, setPlan] = useState(maintenance);
  const [busy, setBusy] = useState(false);
  const draft = objectApi.draft?.workOrder;

  useEffect(() => { setPlan(maintenance); }, [maintenance]);

  const refreshPlan = () => {
    getMaintenancePlan()
      .then((response) => {
        if (!response?.data) return;
        setPlan((prev) => ({
          ...(prev || {}),
          ...response.data,
          tasks: Array.isArray(response.data.tasks) && response.data.tasks.length
            ? response.data.tasks
            : prev?.tasks || [],
        }));
      })
      .catch(() => {});
  };

  useEffect(() => {
    refreshPlan();
  }, []);

  const tasks = Array.isArray(plan?.tasks) ? plan.tasks : [];
  const baseWork = tasks.map(normalizeTask);
  const work = draft && !baseWork.some((item) => item.id === draft.id)
    ? [{ ...normalizeTask(draft, 0), status: draft.status || 'Backlog' }, ...baseWork]
    : baseWork;
  const [selected, setSelected] = useState(objectApi.selection.workOrderId || draft?.id || null);

  const chooseWork = (id) => {
    setSelected(id);
    objectApi.setSelection({ workOrderId: id });
  };

  const columns = ['Backlog', 'Ready', 'Scheduled', 'In progress', 'Complete'];
  const selectedWork = work.find((item) => item.id === selected) || work[0];

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
    // Local drafts without server ids cannot be approved via API
    if (String(selectedWork.id).startsWith('draft-') || String(selectedWork.id).startsWith('wo-')) {
      toast.error('Persist the work order before requesting approval');
      return;
    }
    setBusy(true);
    try {
      await approveWorkOrder(selectedWork.id, {
        operator: 'Maintenance lead',
        note: `Approval requested for ${selectedWork.title}`,
      });
      refreshPlan();
      toast.success('Work order approved');
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || 'Approval failed');
    } finally {
      setBusy(false);
    }
  };

  const plannedCost = work.reduce((sum, item) => sum + Number(item.cost || 0), 0);

  return (
    <Box className="maintenance-planner">
      <Box className="maintenance-planner-head">
        <Box>
          <Typography className="product-kicker">MAINTENANCE PLANNING</Typography>
          <Typography className="maintenance-planner-title">Reliability work control</Typography>
          {draft ? (
            <Typography variant="caption" color="text.secondary">
              Draft work order from forecast is staged in Backlog.
            </Typography>
          ) : null}
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
        <Metric label="Open work orders" value={work.length} />
        <Metric label="Approval queue" value={work.filter((item) => /ready|pending/i.test(String(item.status))).length} />
        <Metric
          label="Estimated downtime"
          value={work.some((item) => item.downtime) ? work.map((item) => item.downtime).filter(Boolean)[0] : '—'}
        />
        <Metric label="Planned cost" value={plannedCost ? `$${plannedCost.toLocaleString()}` : '—'} />
      </Box>

      <Box className="maintenance-layout">
        <Paper className="maintenance-board">
          <Box className="maintenance-board-head">
            <Box className="maintenance-view-tabs">
              <Button className="active">kanban</Button>
              {['calendar', 'timeline', 'gantt'].map((view) => (
                <Button key={view} disabled title="Calendar views are not connected to a scheduling backend">
                  {view}
                </Button>
              ))}
            </Box>
            <Typography variant="caption" color="text.secondary">
              Calendar / timeline / gantt are not available yet — board is kanban only.
            </Typography>
          </Box>
          <Box className="maintenance-kanban">
            {columns.map((column) => {
              const columnWork = work.filter((item) => String(item.status).toLowerCase().includes(column.toLowerCase().split(' ')[0]));
              return (
                <Box key={column} className="maintenance-column">
                  <Typography>
                    {column}
                    <b>{columnWork.length}</b>
                  </Typography>
                  {columnWork.map((item) => (
                    <button
                      type="button"
                      key={item.id}
                      onClick={() => chooseWork(item.id)}
                      className={`work-order ${selectedWork?.id === item.id ? 'selected' : ''}`}
                    >
                      <Box>
                        <span className={`priority ${String(item.priority).toLowerCase()}`}>{item.priority}</span>
                        <MoreHorizOutlined fontSize="small" />
                      </Box>
                      <b>{item.title}</b>
                      <Typography>{item.owner}</Typography>
                      <Box>
                        <span>{item.downtime || '—'} downtime</span>
                        <span>{item.cost != null ? `$${Number(item.cost).toLocaleString()}` : '—'}</span>
                      </Box>
                    </button>
                  ))}
                </Box>
              );
            })}
          </Box>
        </Paper>

        <Paper className="maintenance-inspector">
          <Typography className="product-kicker">WORK ORDER INSPECTOR</Typography>
          {selectedWork ? (
            <>
              <Typography className="maintenance-work-title">{selectedWork.title}</Typography>
              <Status state={selectedWork.status} />
              <Box className="maintenance-facts">
                <Metric label="Priority" value={selectedWork.priority} />
                <Metric label="Crew" value={selectedWork.owner} />
                <Metric label="Cost" value={selectedWork.cost != null ? `$${Number(selectedWork.cost).toLocaleString()}` : '—'} />
                <Metric label="Downtime" value={selectedWork.downtime || '—'} />
              </Box>
              <Box className="maintenance-ai">
                <Typography className="product-kicker">AI SUGGESTED SCHEDULE</Typography>
                <Typography>
                  {plan?.rationale?.[0] || 'No AI schedule rationale published for this work order yet.'}
                </Typography>
              </Box>
              <Box className="maintenance-checklist">
                <Typography className="product-kicker">DEPENDENCIES & APPROVALS</Typography>
                <Typography><i />Status <b>{selectedWork.status}</b></Typography>
                <Typography><i />Asset <b>{selectedWork.assetName || selectedWork.assetId || 'Unassigned'}</b></Typography>
                <Typography><i />Source <b>{selectedWork.source || 'maintenance plan'}</b></Typography>
              </Box>
              <Button variant="contained" fullWidth disabled={busy} onClick={handleApprove}>
                Request approval
              </Button>
            </>
          ) : <Empty text="maintenance" />}
        </Paper>
      </Box>

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
          <Typography>Plan priority <b>{plan?.priority || '—'}</b></Typography>
          <Typography>Estimated downtime <b>{plan?.downtime || '—'}</b></Typography>
        </Box>
      </Paper>
    </Box>
  );
}
