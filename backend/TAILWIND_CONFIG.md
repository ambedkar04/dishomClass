# Tailwind CSS Configuration

This project uses `django-tailwind` with a custom theme app named `theme`.

## Configuration
- **App Name**: `theme`
- **CSS Framework**: Tailwind CSS
- **Plugins**: Typography, Forms, Aspect Ratio

## Structure
- `theme/`: Contains the Tailwind configuration and source files.
- `theme/static_src/`: Source CSS files.
- `theme/static/css/`: Compiled CSS output (do not edit directly).
- `theme/templates/`: Template overrides.

## Development
To start the development server with hot reloading:
```bash
python manage.py tailwind start
```
