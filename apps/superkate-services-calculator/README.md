# Superkate Services Calculator

A private appointment services calculator for Hair by Superkate.

Core formula:

```txt
hourly rate × time spent + product cost = appointment total
```

See `projects/superkate-services-calculator/SPEC.md` for the product brief and `projects/superkate-services-calculator/roadmap.yaml` for the agent plan.

First checkout on a dev machine:

```sh
cd apps/superkate-services-calculator
flutter create . --org org.kindrobots --project-name superkate_services_calculator --platforms ios,android
flutter pub get
flutter test
```
