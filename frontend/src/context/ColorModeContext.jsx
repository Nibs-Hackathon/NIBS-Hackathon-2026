import { createContext, useContext, useEffect, useMemo, useState } from 'react';

const ColorModeContext = createContext(null);

export function ColorModeProvider({ children }) {
  const [mode, setMode] = useState(() => localStorage.getItem('rigos-color-mode') || 'dark');
  useEffect(() => { localStorage.setItem('rigos-color-mode', mode); document.documentElement.dataset.rigosTheme = mode; }, [mode]);
  const value = useMemo(() => ({ mode, toggle: () => setMode((current) => current === 'dark' ? 'light' : 'dark') }), [mode]);
  return <ColorModeContext.Provider value={value}>{children}</ColorModeContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useColorMode() {
  const context = useContext(ColorModeContext);
  if (!context) throw new Error('useColorMode must be used inside ColorModeProvider');
  return context;
}
