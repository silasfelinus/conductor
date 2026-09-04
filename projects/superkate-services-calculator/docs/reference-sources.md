# Superkate Services Calculator — Reference Sources

Date: 2026-07-08

## Local reference folders

Silas added two project-local reference folders for future Worker/Reviewer passes:

- `projects/superkate-services-calculator/examples/` — Superkate hair-work examples. Use this as the strongest visual reference for styling, color, vibe, portfolio language, and design direction.
- The current Hair by Superkate WordPress front end is the live site at hairbysuperkate.com, running as an Unraid container — use it directly. The reference copy that used to sit at `projects/superkate-services-calculator/hairpress/` was removed (conductor/t-106); the first-party `wp-content/plugins/superkates-special-plugin/` and the Instagram archive are still tracked here.

## Design interpretation

Superkate is a barber with a strong focus on rainbow hair, gender-affirming haircuts, wild designs, queer/genderqueer/alternative identity, and spunky salon energy. Future visual work should use the examples folder first rather than drifting back into generic salon SaaS.

## Flutter target default

For app scaffolding going forward, include these Flutter platform targets by default unless a project explicitly narrows scope:

```sh
flutter create . --org org.kindrobots --project-name <project_name> --platforms ios,android,windows,linux
```

The Superkate app should be treated as mobile plus desktop-capable by default for local installs and future testing.
