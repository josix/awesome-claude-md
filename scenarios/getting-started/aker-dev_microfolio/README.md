# Analysis: Microfolio - Static Portfolio Generator

**Category: Getting Started**
**Source**: [aker-dev/microfolio](https://github.com/aker-dev/microfolio)
**CLAUDE.md**: [View Original](https://github.com/aker-dev/microfolio/blob/main/CLAUDE.md)
**License**: MIT
**Stars**: 127

## Why This Example

This CLAUDE.md demonstrates an ideal onboarding document for a SvelteKit-based static site generator. It covers the file-based content management system, data loading patterns, build and deployment configuration, and project metadata schema in a well-organized format. The document makes it straightforward for an AI assistant to understand how content flows from Markdown files through server-side processing to the final static site.

### Key Features That Make This Exemplary

### 1. File-Based Content System Documentation
The document clearly describes the content structure: projects live in `/content/projects/{project-name}/` with `index.md` for metadata, `thumbnail.jpg` for thumbnails, and subdirectories for images, documents, and videos. This filesystem-as-CMS pattern is documented precisely enough for an AI assistant to create new content correctly.

### 2. Data Loading Pattern Explanation
The server-side data loading pipeline is documented step by step: `+page.server.js` files read Markdown with `fs/promises`, parse YAML frontmatter with the `yaml` library, and convert Markdown to HTML using `marked`. This chain of transformations is exactly what an AI assistant needs to understand when debugging content rendering issues.

### 3. Project Metadata Schema with YAML Example
A complete YAML frontmatter schema is provided with all supported fields: title, date, location, coordinates (for map display), description, type, tags, authors with roles, and the `featured` flag for homepage display. This schema reference enables AI assistants to create properly structured content without trial and error.

### 4. Environment-Aware Build Configuration
The document explains how the base path differs between development and production (GitHub Pages uses `/microfolio`, custom domains use no base path), controlled by the `CUSTOM_DOMAIN` environment variable. This deployment-aware configuration documentation prevents common build issues.

### 5. Multi-View Architecture
The routing structure is documented with four distinct views: homepage with featured projects, gallery view, datatable view with filtering, and an interactive Leaflet map view. Each route is mapped to its URL path, giving AI assistants a complete picture of the application's user-facing surface.

### 6. CLI Tool Integration
The document mentions a Homebrew-installable CLI tool (`microfolio new`, `microfolio dev`, `microfolio build`) that wraps the development commands. This bridges the gap between the package manager commands and a user-friendly CLI interface.

## Key Takeaways

1. **Document Content Schemas Explicitly** - For content-driven sites, providing the exact YAML/frontmatter schema with all supported fields eliminates guesswork and enables AI assistants to create correctly structured content on the first attempt.
2. **Explain the Data Loading Pipeline** - Documenting how content moves from filesystem through parsing libraries to rendered HTML gives AI assistants the context needed to debug issues at any point in the chain.
3. **Address Environment Differences** - Explicitly documenting how build configuration varies between development, production, and custom domain deployments prevents an entire class of "works locally, breaks in production" issues.

## Attribution

- **Repository**: [aker-dev/microfolio](https://github.com/aker-dev/microfolio)
- **Original CLAUDE.md**: [Direct Link](https://github.com/aker-dev/microfolio/blob/main/CLAUDE.md)
- **License**: MIT
- **Creator**: AKER
