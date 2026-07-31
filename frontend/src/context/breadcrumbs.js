/**
 * Pure breadcrumb resolver — docs/OBJECT_CONTEXT.md + DESIGN_SYSTEM.md
 */

import { WORKSPACE_LABELS, WORKSPACE_PATHS } from './objectNavigation';

/**
 * @typedef {{ label: string, workspace?: string, preserve?: object }} Crumb
 */

/**
 * @param {object} params
 * @param {string} params.facility
 * @param {string} params.workspace — key from WORKSPACE_PATHS
 * @param {object} [params.labels] — { assetName, unitLabel, incidentLabel, workOrderTitle, reportTitle, stageLabel }
 * @param {object} [params.selection]
 * @returns {Crumb[]}
 */
export function resolveBreadcrumbs({ facility, workspace, labels = {}, selection = {} }) {
  const crumbs = [
    {
      label: facility || 'Facility',
      workspace: 'command',
      preserve: {},
    },
    {
      label: WORKSPACE_LABELS[workspace] || workspace,
      workspace,
      preserve: {},
    },
  ];

  if (workspace === 'assets') {
    if (labels.unitLabel) {
      crumbs.push({
        label: labels.unitLabel,
        workspace: 'assets',
        preserve: { assetId: selection.assetId || undefined, unitId: labels.unitLabel },
      });
    }
    if (labels.assetName || selection.assetId) {
      crumbs.push({
        label: labels.assetName || selection.assetId,
        workspace: 'assets',
        preserve: { assetId: selection.assetId },
      });
    }
  }

  if (workspace === 'incidents' && (labels.incidentLabel || selection.incidentId)) {
    crumbs.push({
      label: labels.incidentLabel || selection.incidentId,
      workspace: 'incidents',
      preserve: { incidentId: selection.incidentId },
    });
  }

  if (workspace === 'investigation') {
    if (labels.incidentLabel || selection.incidentId) {
      crumbs.push({
        label: labels.incidentLabel || selection.incidentId,
        workspace: 'investigation',
        preserve: { incidentId: selection.incidentId },
      });
    }
    if (labels.stageLabel || selection.agentStageId) {
      crumbs.push({
        label: labels.stageLabel || selection.agentStageId,
        workspace: 'investigation',
        preserve: {
          incidentId: selection.incidentId,
          agentStageId: selection.agentStageId,
        },
      });
    }
  }

  if (workspace === 'maintenance' && (labels.workOrderTitle || selection.workOrderId)) {
    crumbs.push({
      label: labels.workOrderTitle || selection.workOrderId,
      workspace: 'maintenance',
      preserve: { workOrderId: selection.workOrderId },
    });
  }

  if (workspace === 'forecasting' && (labels.assetName || selection.assetId)) {
    crumbs.push({
      label: labels.assetName || selection.assetId,
      workspace: 'forecasting',
      preserve: { assetId: selection.assetId },
    });
  }

  if (workspace === 'reports' && (labels.reportTitle || selection.reportId)) {
    crumbs.push({
      label: labels.reportTitle || selection.reportId,
      workspace: 'reports',
      preserve: { reportId: selection.reportId },
    });
  }

  return crumbs;
}

export function crumbPath(crumb) {
  return WORKSPACE_PATHS[crumb.workspace] || '/';
}
