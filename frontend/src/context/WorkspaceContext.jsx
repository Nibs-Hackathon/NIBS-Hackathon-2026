import { createContext, useContext, useEffect, useMemo, useState } from 'react';

const WorkspaceContext = createContext(null);
const STORAGE_KEY = 'rigos.workspace.v1';

function readWorkspace() {
  try { return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '{}'); } catch { return {}; }
}

export function WorkspaceProvider({ children }) {
  const [workspace, setWorkspace] = useState(readWorkspace);
  useEffect(() => { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(workspace)); }, [workspace]);
  const value = useMemo(() => ({
    workspace,
    setWorkspaceValue: (key, value) => setWorkspace((current) => ({ ...current, [key]: value })),
  }), [workspace]);
  return <WorkspaceContext.Provider value={value}>{children}</WorkspaceContext.Provider>;
}

export function useWorkspace() {
  const context = useContext(WorkspaceContext);
  // Keep route-level UI usable during React Fast Refresh, when a context
  // provider can briefly be remounted after its consumers.
  const [fallbackWorkspace, setFallbackWorkspace] = useState(readWorkspace);
  useEffect(() => {
    if (!context) sessionStorage.setItem(STORAGE_KEY, JSON.stringify(fallbackWorkspace));
  }, [context, fallbackWorkspace]);
  const fallback = useMemo(() => ({
    workspace: fallbackWorkspace,
    setWorkspaceValue: (key, value) => setFallbackWorkspace((current) => ({ ...current, [key]: value })),
  }), [fallbackWorkspace]);
  return context || fallback;
}
