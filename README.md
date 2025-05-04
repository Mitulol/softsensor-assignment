# SoftSensor Assignment – Final Submission

This repository contains all components and deliverables for the SoftSensor logistics data pipeline assignment. The project integrates MongoDB, Airbyte, PostgreSQL, dbt, and Cube.dev to build an end-to-end analytics pipeline.

---

## 📁 Deliverable 1 – MongoDB Schema Design

Includes the design and explanation of the MongoDB schema used to capture deeply nested logistics data.
📄 Located in [`deliverables/deliverable_1.md`](./deliverables/deliverable_1.md)  

---

## 📁 Deliverable 2 – Airbyte Ingestion Setup

I originally tried using `abctl` to install Airbyte locally, but the install took over 10 hours on my personal laptop. I then switched to **Airbyte Cloud**, which doesn’t support exporting full connection configs—but I’ve included the **source and destination configs** separately instead.

📄 Markdown: [`deliverables/deliverable_2.md`](./deliverables/deliverable_2.md)  
📄 Config JSON: [`deliverables/deliverable_2.json`](./deliverables/deliverable_2.json)  
📷 Sync Logs: [`deliverables/deliverable_2_sync_log_1.png`](./deliverables/deliverable_2_sync_log_1.png), [`deliverables/deliverable_2_sync_log_2.png`](./deliverables/deliverable_2_sync_log_2.png)

---

## 📁 Deliverable 3 – ERD Diagram

Shows the final ERD derived from the ingested MongoDB schema.
📷 [`deliverables/deliverable_3.png`](./deliverables/deliverable_3.png)  

---

## 📁 Deliverable 4 – dbt Transformation Project

Includes:

- Staging models to flatten nested MongoDB documents
- Core fact/dimension models
- Snapshots
- Metrics definitions
- dbt documentation site (via `dbt docs generate`)

📁 Full project located in the [`logistics_pipeline/`](./logistics_pipeline) directory.  

---

## 📁 Deliverable 5 – Cube.dev Semantic Layer

📄 [`deliverables/deliverable_5.js`](./deliverables/deliverable_5.js) (summary version)  
📁 Full implementation lives in [`cube_project/`](./cube_project), where metrics were defined and exposed via Cube.dev’s REST/GraphQL API.

---

## 📁 Deliverable 6 – Semantic Layer Comparison

Comparison of dbt and Cube.dev’s semantic layers across performance, real-time support, governance, and ease of use—based on actual project implementation.
📄 [`deliverables/deliverable_6.md`](./deliverables/deliverable_6.md)  

---

## 📁 Deliverable 7 – Cube.dev Dashboard Screenshot

Screenshot of the Cube Playground, showing calculated metrics like `deliverySuccessRate`, `completedDeliveries`, and `exceptionCount`.
📷 [`deliverables/deliverable_7.png`](./deliverables/deliverable_7.png)  


---

