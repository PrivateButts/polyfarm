# Copilot Instructions for polyfarm

## Project Architecture

- This is a Django-based multi-app project for managing 3D printers and related workflows.
- Major apps are located in `src/`:
  - `farm/`: Core models, views, and templates for printer management.
  - `mnrkr/`: Moonraker (Klipper) printer integration, including handler and connection models.
  - `polyfarm/`: Project-level settings, helpers, and shared templates/static files.
  - `prslnk/`: PrusaLink integration (see handler for async patterns).
- Handlers for external printer APIs (Moonraker, PrusaLink) are implemented in their respective app directories and subclass `BaseHandler` from `polyfarm/helpers/handlers.py`.
- Django Unicorn is used to bring interactivity to pages
- Daisy UI and Tailwind CSS are used for styling.

## Key Patterns & Conventions

- Printer API handlers must:
  - Use the dataclasses `PrinterInfo` and `PrinterStatus` from `BaseHandler` for all status/info returns.
  - Support authentication (e.g., Moonraker uses `X-Api-Key` header).
  - Prefer `httpx` for HTTP requests (async for PrusaLink, sync for Moonraker).
  - Prefer benedict objects for cleaner data handling.
- Models for external connections (e.g., `MoonrakerConnection`) are in each app's `models.py` and must provide a `.handler()` method returning a configured handler instance.
- Templates use Django's `{% with %}` and dot-access for handler dataclass fields (see `farm/templates/unicorn/printer_list_item.html`).
- Static files are in `src/staticfiles/` and referenced via Django's static system.

## Developer Workflows

- Python dependencies are managed via UV
- Use `justfile` for common tasks (if present).
  - `just manage XXXX` for django manage.py commands.
- Database is SQLite by default (`src/db.sqlite3`).
- To run the server: `just manage runserver`
- To run tests: `just manage test`
- Migrations: `just manage makemigrations` and `python src/manage.py migrate`
- For new handler integrations, subclass `BaseHandler` and implement required dataclass-returning methods.

## Integration Points

- Handlers communicate with external printer APIs via HTTP (Moonraker, PrusaLink).
- Cross-app communication is via Django models and handler interfaces.
- Templates expect handler methods to return dataclasses, not raw dicts.

## Examples

- See `src/mnrkr/handler.py` for Moonraker handler using `httpx` and dataclasses.
- See `src/prslnk/handler.py` for async PrusaLink handler and status mapping.
- See `src/polyfarm/helpers/handlers.py` for handler base class and dataclass schema.
- See `src/farm/templates/unicorn/printer_list_item.html` for template usage of handler dataclasses.

## Notes

- Do not use entity references in templates (use `°C` instead of `&deg;C`).
- All handler errors should raise `BaseHandler.HandlerError` for consistency.
- Keep handler interfaces stable for template and model integration.
