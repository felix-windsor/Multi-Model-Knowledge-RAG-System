# Frontend Redesign Design Document

**Date:** 2026-01-29
**Status:** Approved
**Author:** Claude & User

## Overview

Redesign the MultiModal RAG System frontend to improve visual aesthetics, add missing functionality, and optimize the user experience.

## Current State

- Bootstrap 5.3.0 + vanilla JavaScript
- Three-column layout (30% / 40% / 50%)
- Standard Bootstrap styling, lacks modern feel
- Missing features: document deletion, streaming output, theme switching
- Knowledge graph constrained by limited space

## Design Goals

1. **Visual Upgrade** - Dark tech aesthetic with theme switching
2. **Feature Enhancement** - Add deletion, streaming, and other missing capabilities
3. **Layout Optimization** - Tab-based switching for full-width content areas

---

## Layout Design

### Overall Structure

```
┌─────────────────────────────────────────────────────────────┐
│  🧠 MultiModal RAG                              [🌙/☀️]    │  ← Top navbar
├─────────────────────────────────────────────────────────────┤
│  [📄 Documents]   [💬 Q&A]   [🔗 Graph]   [⚙️ Settings]    │  ← Tab navigation
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                     Content Area                            │
│                     (switches by tab)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
│  Status: Qdrant ✓ · Neo4j ✓ · Documents: 5                 │  ← Status bar
└─────────────────────────────────────────────────────────────┘
```

### Tab Navigation

- Four tabs: Documents, Q&A, Knowledge Graph, Settings
- Current tab highlighted with accent color
- Icons for quick recognition
- Smooth transition animation between tabs

---

## Document Management Tab

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  📄 Document Management                                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📁 Drag files here to upload                       │   │
│  │     or [Choose Files]                               │   │
│  │     Supports: PDF, Word, Excel, PPT, Images         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ Document List ─────────────────────────────────────┐   │
│  │ □  Name                  Status      Time     Actions│   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ □  architecture.pdf      ✅ Done     10:30     🗑️   │   │
│  │ □  requirements.docx     ⏳ Processing 10:28   🗑️   │   │
│  │ □  report.xlsx           ❌ Failed   10:25     🔄 🗑️ │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  [Select All] [Delete Selected (2)]         Total: 4 docs  │
└─────────────────────────────────────────────────────────────┘
```

### Features

| Feature | Description |
|---------|-------------|
| Drag & drop upload | Dashed border area, highlights on drag over |
| Multi-file upload | Support selecting multiple files at once |
| Real-time status | Auto-poll status for processing documents |
| **Single delete** | Delete icon per row, confirmation dialog |
| **Batch delete** | Checkbox selection + batch delete button |
| Retry mechanism | Retry button for failed documents |
| Document details | Click to expand (entities, relations, processing time) |

### Status Indicators

- ⏳ Processing - Blue with spinner animation
- ✅ Complete - Green
- ❌ Failed - Red with error message

---

## Q&A Tab

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  💬 Q&A                                                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─ Query Settings ─────────────────────────────────────┐  │
│  │  Mode: [Mix ▼]           Scope: [All Documents ▼]    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ Conversation ───────────────────────────────────────┐  │
│  │  🧑 What are the main points of this document?       │  │
│  │                                                       │  │
│  │  🤖 Based on the knowledge base, the document        │  │
│  │     discusses the following points:                   │  │
│  │     1. Microservice architecture design...            │  │
│  │                                                       │  │
│  │     📎 Source: architecture.pdf (Page 3)             │  │
│  │     ────────────────────────────────                  │  │
│  │                                                       │  │
│  │  🧑 How are the entities related?                    │  │
│  │                                                       │  │
│  │  🤖 ▌ (streaming...)                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────┐ [Send]   │
│  │  Enter your question...                       │         │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Features

| Feature | Description |
|---------|-------------|
| Query mode selector | mix/local/global/hybrid/naive |
| Document scope filter | All documents or specific selection |
| **Streaming output** | Call `/api/v1/query/stream` for real-time display |
| Source citations | Show source document and page, clickable |
| Conversation history | Retain Q&A history for current session |
| Copy answer | Hover to show copy button |
| Clear conversation | One-click clear history |

### Interactions

- `Ctrl+Enter` to send
- Typewriter cursor effect `▌` during generation
- Source links highlight on hover

---

## Knowledge Graph Tab

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  🔗 Knowledge Graph                             [⛶ Fullscreen]│
├─────────────────────────────────────────────────────────────┤
│  ┌─ Toolbar ────────────────────────────────────────────┐  │
│  │ 🔍 Search entities...  [Filter ▼]  [+] [-] [⟲ Reset] │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────┬───────────────┐  │
│  │                                      │  📋 Details    │  │
│  │         ○───○                        │               │  │
│  │        /     \                       │  Entity: RAG   │  │
│  │       ○       ○───○                  │  Type: Tech    │  │
│  │        \     /                       │  Desc: ...     │  │
│  │         ○───○                        │               │  │
│  │              \                       │  Relations:    │  │
│  │               ○                      │  → contains A  │  │
│  │                                      │  → depends DB  │  │
│  │      (vis.js interactive graph)      │               │  │
│  │                                      │  [Query this]  │  │
│  └──────────────────────────────────────┴───────────────┘  │
│                                                             │
│  Stats: 156 entities · 243 relations · from 5 documents    │
└─────────────────────────────────────────────────────────────┘
```

### Features

| Feature | Description |
|---------|-------------|
| Entity search | Highlight matching nodes |
| Document filter | Show subgraph for specific documents |
| Zoom controls | Zoom in/out/reset |
| **Fullscreen mode** | Graph fills entire browser window |
| Node interaction | Click node to show details panel |
| Drag layout | Drag nodes to adjust positions |
| Relation navigation | Click relation to locate related nodes |
| Linked query | Launch Q&A query for selected entity |

### Visual Effects

- Nodes colored by type (person, location, concept, tech, etc.)
- Relation lines with arrows and labels
- Selected node highlights neighbors, dims others
- Subtle glow effect on nodes against dark background

### Fullscreen Mode

- Press `F` or click fullscreen button to enter
- `ESC` to exit
- Hides top navigation, maximizes graph space

---

## Settings Tab

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Settings                                                │
├─────────────────────────────────────────────────────────────┤
│  ┌─ Appearance ─────────────────────────────────────────┐  │
│  │  Theme     [🌙 Dark]  [☀️ Light]  [💻 System]        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ Query Defaults ─────────────────────────────────────┐  │
│  │  Default mode        [Mix ▼]                         │  │
│  │  Enable streaming    [✓]                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ System Info ────────────────────────────────────────┐  │
│  │  Backend version     v1.0.0                          │  │
│  │  LLM Provider        Qwen                            │  │
│  │  Embedding Model     text-embedding-v3 (1024d)       │  │
│  │  Vector DB           Qdrant ✅ Connected             │  │
│  │  Graph DB            Neo4j ✅ Connected              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ Data Management ────────────────────────────────────┐  │
│  │  [Clear All Documents]  [Reset Graph]  [Export Data] │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Theme System

### Color Palette

#### Dark Theme (Default)

```css
:root[data-theme="dark"] {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #21262d;
  --border-color: #30363d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --accent: #58a6ff;
  --accent-hover: #79c0ff;
  --success: #7ee787;
  --warning: #d29922;
  --error: #f97583;
}
```

#### Light Theme

```css
:root[data-theme="light"] {
  --bg-primary: #ffffff;
  --bg-secondary: #f6f8fa;
  --bg-tertiary: #eaeef2;
  --border-color: #d0d7de;
  --text-primary: #1f2328;
  --text-secondary: #656d76;
  --accent: #0969da;
  --accent-hover: #0550ae;
  --success: #1a7f37;
  --warning: #9a6700;
  --error: #cf222e;
}
```

### Implementation

- CSS variables for all colors
- `localStorage` to persist user preference
- Support `prefers-color-scheme` media query
- Smooth transition (0.2s) on theme change

---

## Technical Implementation

### File Structure

```
frontend/
├── index.html              # Main HTML (restructured)
├── assets/
│   ├── css/
│   │   ├── variables.css   # CSS variables & themes
│   │   ├── base.css        # Reset & base styles
│   │   ├── components.css  # Buttons, cards, forms
│   │   ├── layout.css      # Tab layout, navbar
│   │   ├── documents.css   # Document management styles
│   │   ├── query.css       # Q&A styles
│   │   ├── graph.css       # Knowledge graph styles
│   │   └── settings.css    # Settings page styles
│   └── js/
│       ├── app.js          # Main app, tab switching
│       ├── theme.js        # Theme management
│       ├── documents.js    # Document management (with delete)
│       ├── query.js        # Q&A (with streaming)
│       ├── graph.js        # Knowledge graph (with fullscreen)
│       └── settings.js     # Settings management
```

### API Endpoints Used

| Feature | Endpoint |
|---------|----------|
| Upload document | `POST /api/v1/documents/upload` |
| List documents | `GET /api/v1/documents` |
| Document status | `GET /api/v1/documents/{id}` |
| **Delete document** | `DELETE /api/v1/documents/{id}` |
| Query | `POST /api/v1/query` |
| **Stream query** | `POST /api/v1/query/stream` (SSE) |
| Get graph | `GET /api/v1/graph` |
| Get subgraph | `GET /api/v1/graph/subgraph` |
| Graph stats | `GET /api/v1/graph/stats` |
| Health check | `GET /api/v1/health/detailed` |
| Config | `GET /api/v1/config` |

### Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Summary of Changes

| Module | Key Improvements |
|--------|------------------|
| Layout | Three-column → Tab switching, full-width content |
| Documents | Add delete (single + batch), retry, expand details |
| Q&A | Add streaming output, source citations, history |
| Graph | Add fullscreen, search, details panel, linked query |
| Visual | Dark tech theme + light theme switching |
| Settings | New page for preferences and system info |

---

## Next Steps

1. Create implementation plan with detailed tasks
2. Set up git worktree for isolated development
3. Implement in phases:
   - Phase 1: Layout restructure and theme system
   - Phase 2: Document management with delete
   - Phase 3: Q&A with streaming
   - Phase 4: Knowledge graph enhancements
   - Phase 5: Settings page and polish
