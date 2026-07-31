import { useEffect, useState } from 'react';
import { Box, Button, Chip, CircularProgress, IconButton, Stack, TextField, Typography } from '@mui/material';
import { AutoStoriesOutlined, CloseOutlined, SendOutlined, SmartToyOutlined } from '@mui/icons-material';
import { useObjectContext } from '../context/ObjectContext';
import { useOperations } from '../context/OperationsContext';
import { askAssistant, getKnowledgeDocuments } from '../api/client';
import './assistant-knowledge.css';

const prompts = ['What needs my attention?', 'Explain the active investigation', 'Summarize current asset risk'];

function AssistantResponse({ text }) {
  const lines = String(text || '').split('\n');
  return (
    <Box className="assistant-response">
      {lines.map((line, index) => {
        if (line.startsWith('## ')) {
          return <Typography key={index} className="assistant-response-heading">{line.slice(3)}</Typography>;
        }
        if (line.startsWith('- ')) {
          return <Typography key={index} className="assistant-response-bullet"><i />{line.slice(2)}</Typography>;
        }
        return line.trim()
          ? <Typography key={index} variant="body2">{line}</Typography>
          : <Box key={index} className="assistant-response-gap" />;
      })}
    </Box>
  );
}

export function AssistantPanel({ onClose }) {
  const objectApi = useObjectContext();
  const { operations } = useOperations();
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const [knowledgeDocuments, setKnowledgeDocuments] = useState([]);
  const [knowledgeStatus, setKnowledgeStatus] = useState('loading');
  const selectedAsset = (operations.assets || []).find(
    (asset) => asset.id === objectApi.selection.assetId,
  );
  const hasObjectContext = Boolean(
    objectApi.selection.assetId || objectApi.selection.incidentId,
  );

  useEffect(() => {
    let cancelled = false;
    getKnowledgeDocuments()
      .then((response) => {
        if (cancelled) return;
        setKnowledgeDocuments(Array.isArray(response.data?.documents) ? response.data.documents : []);
        setKnowledgeStatus('ready');
      })
      .catch(() => {
        if (cancelled) return;
        setKnowledgeStatus('unavailable');
      });
    return () => { cancelled = true; };
  }, []);

  const send = async (value = question) => {
    const text = value.trim();
    if (!text || busy) return;
    setMessages((items) => [...items, { role: 'operator', text }]);
    setQuestion('');
    setBusy(true);
    try {
      const response = await askAssistant(text, {
        asset_id: objectApi.selection.assetId,
        incident_id: objectApi.selection.incidentId,
        facility: objectApi.scope?.facility,
        history: messages.slice(-6),
      });
      setMessages((items) => [
        ...items,
        { role: 'assistant', text: response.data.answer || 'No response was returned.' },
      ]);
    } catch (error) {
      const unavailable = !error.response;
      setMessages((items) => [
        ...items,
        {
          role: 'assistant',
          text: unavailable
            ? 'RigOS cannot reach the AI service. Check the deployed backend connection, then try again.'
            : (error.response?.data?.detail || 'The AI service could not complete that request. Please try again.'),
        },
      ]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <Box className="assistant-panel">
      <Stack direction="row" justifyContent="space-between" alignItems="start">
        <Box>
          <Typography className="product-dialog-label">RIGOS AI</Typography>
          <Typography variant="h6">Operations copilot</Typography>
          <Typography variant="body2" color="text.secondary">
            Ask about assets, incidents, evidence, and recommended next actions.
          </Typography>
          <Chip
            className="assistant-context-chip"
            size="small"
            label={
              hasObjectContext
                ? `Selected context: ${selectedAsset?.name || 'incident'}`
                : `Scope: ${objectApi.scope?.facility || 'Enterprise view'}`
            }
            onDelete={
              hasObjectContext
                ? () => objectApi.clearSelection(['assetId', 'incidentId'])
                : undefined
            }
          />
        </Box>
        <IconButton onClick={onClose}><CloseOutlined /></IconButton>
      </Stack>
      <Stack direction="row" flexWrap="wrap" gap={0.7} sx={{ mt: 2 }}>
        {prompts.map((prompt) => (
          <Button key={prompt} size="small" variant="outlined" onClick={() => send(prompt)}>{prompt}</Button>
        ))}
      </Stack>
      <Box className="assistant-history">
        {messages.length ? (
          <Stack spacing={1.2}>
            {messages.map((message, index) => (
              <Box key={index} className={`assistant-message ${message.role}`}>
                {message.role === 'assistant'
                  ? <AssistantResponse text={message.text} />
                  : <Typography variant="body2">{message.text}</Typography>}
              </Box>
            ))}
            {busy && (
              <Box className="assistant-pipeline-live">
                <CircularProgress size={16} />
                <Box>
                  <Typography>Resolving operating context</Typography>
                  <Typography>Incident check · financial model · knowledge guidance</Typography>
                </Box>
              </Box>
            )}
          </Stack>
        ) : (
          <Box className="assistant-empty">
            <SmartToyOutlined />
            <Typography fontWeight={750}>How can I help?</Typography>
            <Typography variant="body2" color="text.secondary">
              Live operating context is grounded with an always-available local refinery corpus.
            </Typography>
            <Box className="assistant-knowledge-card">
              <Stack direction="row" spacing={1} alignItems="center">
                <AutoStoriesOutlined fontSize="small" />
                <Box sx={{ minWidth: 0, flex: 1 }}>
                  <Typography variant="caption" fontWeight={800}>KNOWLEDGE SOURCES</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {knowledgeStatus === 'loading' && 'Loading refinery references...'}
                    {knowledgeStatus === 'unavailable' && 'Catalog available when the backend reconnects.'}
                    {knowledgeStatus === 'ready' && `${knowledgeDocuments.length} refinery references ready`}
                  </Typography>
                </Box>
                {knowledgeStatus === 'ready' && <Chip size="small" label="Local" color="success" variant="outlined" />}
              </Stack>
              {knowledgeDocuments.length > 0 && (
                <Stack spacing={0.5} sx={{ mt: 1.2 }}>
                  {knowledgeDocuments.slice(0, 4).map((document) => (
                    <Typography key={document.id} variant="caption" className="assistant-knowledge-source">
                      {document.title}
                    </Typography>
                  ))}
                  {knowledgeDocuments.length > 4 && (
                    <Typography variant="caption" color="text.secondary">
                      +{knowledgeDocuments.length - 4} more references
                    </Typography>
                  )}
                </Stack>
              )}
            </Box>
          </Box>
        )}
      </Box>
      <Stack direction="row" spacing={1}>
        <TextField
          fullWidth
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask RigOS..."
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault();
              send();
            }
          }}
        />
        <Button variant="contained" onClick={() => send()} disabled={!question.trim() || busy}>
          <SendOutlined />
        </Button>
      </Stack>
    </Box>
  );
}
