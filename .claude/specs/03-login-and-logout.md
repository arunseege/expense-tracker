# Spec: Login and Logout

## Overview
Add a fully working login and logout flow so registered users can authenticate
into Spendly and have a persistent server-side session. This step also hardens
the nav bar (showing context-aware links depending on auth state), establishes a
`login_required` helper that future routes can use, and makes the root `/` route
serve a real HTML response rather than a raw JSON blob. Without this step no
protected page can exist and the nav always shows stale auth links.

## Depends on
- Step 01 (Database Setup) — `users` table, `get_db()`, `verify_user()` must be in place.
- Step 02 (Registration) — `base.html`, `register.html`, and `static/style.css` must exist.

## Routes
- `GET /login` — render the login form — public
- `POST /login` — validate credentials, set session, redirect to `/` on success — public
- `GET /logout` — clear session, flash message, redirect to `/login` — logged-in
- `GET /` — render a simple home/dashboard placeholder page — public (redirect to `/login` if not authenticated)

Note: `GET /login` and `POST /login` routes already exist in `app.py`, as does
`GET /logout`. All three need review/adjustment as noted in **Files to change**.

## Database changes
No new tables or columns. `verify_user(email, password)` and
`get_user_by_email(email)` already exist in `database/db.py` and are sufficient.

## Templates
- **Create:**
  - `templates/index.html` — minimal logged-in home/dashboard placeholder extending `base.html`
- **Modify:**
  - `templates/base.html` — update nav to show "Log out" (with user name) when
    `session.user_id` is set, otherwise show "Register" and "Log in" links

## Files to change
- `app.py`
  - Add a `login_required` helper (a simple function, not a decorator, is fine —
    returns a redirect or `None` so routes can call it at the top)
  - Update `GET /` to render `index.html` (redirect to `/login` if not logged in)
  - Ensure `POST /login` redirects to `/` after a successful login
  - Ensure `GET /logout` is only reachable when logged in (or is idempotent on
    unauthenticated calls — clearing an empty session is harmless)
- `templates/base.html` — conditional nav links based on `session`

## Files to create
- `templates/index.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug` — `verify_user` already does this; do not bypass it
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session keys used: `session["user_id"]` (int) and `session["user_name"]` (str)
- `login_required` must redirect to `/login` and may optionally flash a message
- Do not auto-login the user on registration (Step 02 already handles this correctly)
- `base.html` must read session via `session` (available in Jinja2 when
  `app.secret_key` is set); no extra context injection needed

## Definition of done
- [ ] `GET /login` returns 200 and renders the login form inside `base.html`
- [ ] Submitting valid credentials via `POST /login` sets `session["user_id"]` and `session["user_name"]` and redirects to `/`
- [ ] Submitting invalid credentials shows a flash error and re-renders the form (no 500)
- [ ] Submitting with blank fields shows a validation error on the form
- [ ] `GET /logout` clears the session, flashes a success message, and redirects to `/login`
- [ ] After logout, visiting `/` redirects to `/login`
- [ ] When logged in, the nav shows the user's name and a "Log out" link; "Register" and "Log in" links are hidden
- [ ] When logged out, the nav shows "Register" and "Log in" links
- [ ] `GET /` renders `index.html` (not a JSON response) when the user is logged in
- [ ] App starts without errors; `init_db()` and `seed_db()` still run correctly
