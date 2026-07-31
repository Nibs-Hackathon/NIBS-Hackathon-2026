# RigOS V2 design system

This package is the visual foundation for future RigOS screens. It is intentionally not mounted by the existing application during Phase 1.

## Adoption contract

1. Wrap a future V2 surface with MUI's `ThemeProvider` using `createRigOSV2Theme(mode)`.
2. Import `motion.css` once from the application entry point when V2 components are first mounted.
3. Prefer components from `src/design-system` over one-off page styling.
4. Use semantic tones (`success`, `warning`, `danger`, `info`, `violet`, `neutral`) rather than decorative color choices.

## State language

The library uses a shared state vocabulary: `hover`, `active`, `loading`, `disabled`, and `animated` (via the motion classes). Interactive primitives expose the relevant props directly; informational primitives expose active/loading presentation states where meaningful.

## Architecture decisions

- The system is MUI-compatible to preserve the current frontend dependency stack.
- Tokens are centralized in `tokens.js`; `RigOSV2Theme.js` derives light and dark themes from those tokens.
- Motion is CSS-only and respects `prefers-reduced-motion`.
- Components are presentational and data-agnostic. Pages own API calls and domain state.

## Primitives

Use `src/design-system/primitives.jsx` as the canonical reusable surface. It provides RigCard, MetricCard, StatusBadge, AIAgentCard, TimelineCard, EmptyState, TelemetryChart, RigDrawer, RigModal, Toast, NotificationItem, CommandPalette, RigSearch, RigToolbar, SectionHeader, PageHeader and FloatingPanel.

The implementation takes the structural card/layout approach of Kokonut UI, restrained state treatments from Magic UI, and the utility interactions of ReactBits. Motion powers state entrances, hover/press feedback and live-status indicators; all work is reduced or removed under `prefers-reduced-motion`.
