import { useState } from 'react';
import { Box, Button, CircularProgress, IconButton, Stack, TextField, Typography } from '@mui/material';
import { CloseOutlined, SendOutlined, SmartToyOutlined } from '@mui/icons-material';
import { askAssistant } from '../api/client';

const prompts = ['What needs my attention?', 'Explain the active investigation', 'Summarize current asset risk'];

export function AssistantPanel({ onClose }) {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const send = async (value = question) => {
    const text = value.trim(); if (!text || busy) return;
    setMessages((items) => [...items, { role: 'operator', text }]); setQuestion(''); setBusy(true);
    try { const response = await askAssistant(text); setMessages((items) => [...items, { role: 'assistant', text: response.data.answer || 'No response was returned.' }]); }
    catch (error) {
      const unavailable = !error.response;
      setMessages((items) => [...items, { role: 'assistant', text: unavailable ? 'RigOS cannot reach the AI service. Check the deployed backend connection, then try again.' : (error.response?.data?.detail || 'The AI service could not complete that request. Please try again.') }]);
    }
    finally { setBusy(false); }
  };
  return <Box className="assistant-panel"><Stack direction="row" justifyContent="space-between" alignItems="start"><Box><Typography className="product-dialog-label">RIGOS AI</Typography><Typography variant="h6">Operations copilot</Typography><Typography variant="body2" color="text.secondary">Ask about assets, incidents, evidence, and recommended next actions.</Typography></Box><IconButton onClick={onClose}><CloseOutlined /></IconButton></Stack><Stack direction="row" flexWrap="wrap" gap={.7} sx={{ mt: 2 }}>{prompts.map((prompt) => <Button key={prompt} size="small" variant="outlined" onClick={() => send(prompt)}>{prompt}</Button>)}</Stack><Box className="assistant-history">{messages.length ? <Stack spacing={1.2}>{messages.map((message, index) => <Box key={index} className={`assistant-message ${message.role}`}><Typography variant="body2">{message.text}</Typography></Box>)}{busy && <CircularProgress size={20} />}</Stack> : <Box className="assistant-empty"><SmartToyOutlined/><Typography fontWeight={750}>How can I help?</Typography><Typography variant="body2" color="text.secondary">I use the existing RigOS knowledge service and live operational context.</Typography></Box>}</Box><Stack direction="row" spacing={1}><TextField fullWidth value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask RigOS…" onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); send(); } }} /><Button variant="contained" onClick={() => send()} disabled={!question.trim() || busy}><SendOutlined /></Button></Stack></Box>;
}
