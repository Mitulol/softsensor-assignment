## Semantic Layer Comparison – dbt vs Cube.dev
In this logistics pipeline project, we used dbt and Cube.dev together to define, manage, and expose metrics across nested operational data from MongoDB (via Airbyte) into PostgreSQL.

## How We Used dbt
    - Staging models (stg_*): Flattened nested MongoDB documents ingested via Airbyte.
    - Core models: Defined fact and dimension tables like fct_route_performance, dim_vehicle, etc.
    - Snapshots: Captured slow-changing data (e.g., license status, maintenance).
    - Metric definitions: Defined semantic metrics like inspection_pass_rate in metrics.yml.
    - Documentation: Used dbt docs generate to produce schema and lineage documentation.

## How We Used Cube.dev
    -Created Cube.js models (in .js files) for: RoutePerformance, InspectionSummary, MaintenanceTasks
    -Exposed metrics like delivery success rate and inspection pass rate via REST/GraphQL APIs.
    -Optional support for caching and pre-aggregations for performance.

## Performance
    dbt: Optimized for batch pipelines. Performance depends on warehouse engine and dbt run schedules.
        Pro: Leverages warehouse power during scheduled runs.
        Con: Not ideal for live metrics or low-latency needs.
    Cube.dev: Built for fast query responses using caching and pre-aggregations.
        Pro: Highly performant for real-time dashboards.
        Con: Requires tuning for high-complexity queries or large datasets.

## Real-Time Support
    dbt: No native real-time capabilities.
        Con: Data is only fresh after dbt run; not suitable for live applications.
    Cube.dev: Designed for real-time use cases.
        Pro: It gives you live metrics through REST or GraphQL APIs, so your dashboards and apps can show fresh data without waiting for a batch job.

## Governance
    dbt: Git-based, model-driven governance.
        Pro: Changes are version-controlled and auditable.
        Con: Lacks built-in access control or row-level security without external tools.
    Cube.dev: Built-in RBAC, row-level security, and user-specific data filtering.
        Pro: Excellent for multi-tenant or restricted-access environments.
 
## Ease of Use
    dbt: Easy to learn if you're familiar with SQL and modeling logic.
        Pro: Simple setup, strong docs, and vibrant community.
        Con: Requires familiarity with Jinja templating and YAML config.
    Cube.dev: Steeper learning curve, especially for deployment and custom schemas.
        Pro: Very powerful once set up.
        Con: Requires managing backend infra (Docker/Kubernetes) and JS-based config.

## Summary
In this project, dbt served as the backbone for data modeling, testing, and documentation—making it ideal for structured batch pipelines. Cube.dev complemented it by enabling real-time metric access through APIs, which is especially useful for dashboards or user-facing apps. Together, they allowed us to balance strong governance and modeling (via dbt) with responsive, analytics-ready endpoints (via Cube.dev). Depending on whether your focus is data engineering or live analytics, each tool brings unique strengths to the table.
