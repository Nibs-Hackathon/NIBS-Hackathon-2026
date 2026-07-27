import { Box } from '@mui/material';

// A minimal, repository-local ReactBits timeline shell for trace-oriented interfaces.
export function ReactBitsTimeline({ children }) {
  return <Box className="reactbits-timeline-shell" role="list" aria-label="AI investigation workflow">{children}</Box>;
}
