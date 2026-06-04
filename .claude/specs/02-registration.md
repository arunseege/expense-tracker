# Spec: Registration

## Overview
Add a user registration flow so new visitors can create a Spendly account.
This is the first user-facing feature built on top of the database layer from Step 01.
It introduces Flask session management, Jinja2 templates, and the base HTML layout
that all future pages will extend. Without registration (and the login that follows),
no user-specific data can ever be shown or stored.

## Depends on
- Step 01 (Database Setup) — `users` table and `get_db()` must be in place.

## Routes
- `GET /register` — render the registration form — public
- `POST /register` — process form submission, create user, redirect on success — public

## Database changes
No new tables or columns. The existing `users` table already has all required fields:
`name`, `email`, `password_hash`, `created_at`.

A new helper function must be added to `database/db.py`:
- `create_user(name, email, password)` — inserts a new user row, hashes the password with
  `werkzeug`, and returns the new user's `id`. Must raise (or let bubble) the
  `sqlite3.IntegrityError` when the email is already taken so the route can show an error.

## Templates
- **Create:**
  - `templates/base.html` — shared layout with `<head>`, nav, CSS variable declarations, and a `{% block content %}` slot
  - `templates/register.html` — registration form extending `base.html`
- **Modify:** none

## Files to change
- `database/db.py` — add `create_user()` function
- `app.py` — import `create_user`, add `GET /register` and `POST /register` routes

## Files to create
- `templates/base.html`
- `templates/register.html`
- `static/style.css` — base stylesheet using CSS variables (if it does not already exist)

## New dependencies
- `flask` (already installed — needed for `session`, `redirect`, `url_for`, `render_template`, `request`, `flash`)

No new pip packages required.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` — never store plain text
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `flask.flash` + `get_flashed_messages` for user-facing error/success messages
- Set `app.secret_key` (read from env or a hard-coded dev value) so sessions and flash work
- After successful registration, redirect to `/login` (the next step); do **not** auto-login the user yet
- Duplicate email must show a friendly inline error, not a 500

## Definition of done
- [ ] `GET /register` returns a 200 with the registration form rendered inside `base.html`
- [ ] Submitting the form with valid name, email, and password creates a row in `users` and redirects to `/login`
- [ ] The stored password is a bcrypt/werkzeug hash — never the plain-text password
- [ ] Submitting a duplicate email shows an error message on the page instead of crashing
- [ ] Submitting with any blank field shows a validation error message on the page
- [ ] The `/` route still returns `{"status": "ok", ...}` (no regression)
- [ ] App starts without errors and `init_db()` / `seed_db()` still run correctly