# Office Block Progress Monitoring Dashboard Specifications

## Overview
A web-based dashboard to monitor construction progress for the Office Block project at 長沙灣新福港地盤. Integrates data from Markdown progress reports, schedules, and WhatsApp summaries.

## Requirements

### Functional
1. **Data Parsing**: Backend API to parse Office_Block_Progress.md into structured JSON (floors, schedules, whatsapp summary).
2. **Display**:
   - Table for floor progress: Floor, Project, Progress/Status, Notes.
   - Table for upcoming schedules: Date, Matter, Details/Impact.
   - Section for WhatsApp monitoring summary.
3. **Real-time Updates**: Auto-refresh every 5 minutes; manual refresh button.
4. **Error Handling**: Graceful handling if MD file missing or parse fails.
5. **Integration**: Future: Pull live data from WhatsApp groups via API.

### Non-Functional
1. **UI/UX**: Responsive design, clean tables, color-coding for schedules (e.g., warnings for stoppages).
2. **Performance**: Lightweight, no heavy libs; use vanilla JS.
3. **Security**: Localhost only; no auth needed for internal use.
4. **Tech Stack**: Flask (backend), HTML/JS/CSS (frontend), Markdown parsing with regex.
5. **Visualization**: Basic tables; future: Progress bars for floors, calendar view for schedules.

## Milestones
- v1.0: Basic tables from MD (completed).
- v1.1: WhatsApp integration.
- v2.0: Visual building mockup with progress indicators.

Updated: 2026-02-13