---
name: React Expert Pattern-Follower
description: |
  Use when working on frontend React features for this project. The assistant should follow installed React version patterns, existing component/table/form UI design, frontend routes, and sidebar menu structure. Avoid using the "Jerarquia" menu item as a design example unless requested.
---

# React Expert Pattern-Follower

This skill defines the expected behavior for frontend work in this repository.

## What it means

- The project uses `react` `^19.1.1` and `react-dom` `^19.2.3`.
- Prefer existing UI patterns in `frontend/src/components`, especially table layouts and create/edit/delete forms.
- Use the frontend route files in `frontend/src/routes` as the source of navigation and page structure.
- Use the sidebar structure in `frontend/src/components/Sidebar` as a pattern, but do not rely on the `Jerarquia` item as an example unless explicitly asked.
- Consult the backend API documentation at `http://localhost:8000/docs` when implementing or validating data contracts.
- Use correct API base paths: all backend endpoints are prefixed with `/api/v1` (e.g., `/api/v1/brands`, not just `/brands`).
- In data tables, display UUID shortcuts (e.g., first 8 characters + "...") with tooltips showing the full UUID for better UX.
- Do not invent new UI or architectural patterns unless the user explicitly requests a new approach.

## Suggested prompts

- "Usa la skill React Expert Pattern-Follower para implementar esta pantalla siguiendo los patrones existentes."
- "Revisa las rutas y crea el formulario con el mismo estilo de tablas y modales que ya existen." 
- "No cambies los patrones de diseño actuales sin que te lo pida." 
