# Epic 6 — Frontend performance budget

## Targets

| Metric | Target |
|--------|--------|
| Vite `chunkSizeWarningLimit` | 450 KB |
| Route workspace chunk (gzip) | ~150 KB |
| First paint | Command Center shell + mission chunk |

## Implemented

- **Lazy routes:** each workspace view is a separate chunk under `src/redesign/views/`
- **Vendor split:** `vendor-react`, `vendor-mui`, `vendor-motion`, `vendor-utils`
- **CSS trim:** dropped unused legacy sheets (`mission-control`, `incidents`, `investigation`, `operations-v2`, `refinery-twin`)
- **Deps trim:** removed `@mui/lab`, `socket.io-client`
- **Tokens:** new UI should use `design-system/tokens.js` + `catalog.css`; `product.css` remains shell chrome

## Measure

```bash
npm run build
```

Inspect `dist/assets/*` sizes after each release.
