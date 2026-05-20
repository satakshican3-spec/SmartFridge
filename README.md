# SmartFridge: Intelligent Kitchen Inventory & Sustainability Suite

**A high-utility nutritional management platform engineered to reduce household food waste through real-time perishability tracking and relational recipe discovery.**

SmartFridge is a specialized inventory management system designed to monitor food stock and expiration cycles. By utilizing dynamic date-comparisom algorithms, the application providers users with instant visibility into their kitchen assets, freshness alerts, and automated meal-planning options. The suite focuses on sustainability by ensuring users "consume what they own" before purchasing new supplies.

## Technical Architecture

* **Temporal Freshness Logic:** Implements an ISO-date comparison engine using Python's `datetime` library. The system categorizes inventory into three distinct states-**Fresh**, **Use-Soon**, and **Expired**-based on real-time proximity to the current system clock.
* **Relational Recipe Engine:** Features a logic-based discovery system that cross-references the "Fridge" (perishable) and "Pantry" (persistent) data arrays. It unlocks meal options only when the specific hardware requirements (ingredients) are met.
* **Hierarchical Data Modeling:** Separates data into two distinct structures:
  *   **Perishable Inventory:** Items requiring strict expiration monitoring.
  *   **Pantry Vault:** A persistent list for staples and seasonings (e.g., oils, spices) that do not follow traditional expiration cycles.
* **User Interface (UX):** Optimized for high-speed logging with a pre-defined selection array, reducing manual input friction for common grocery items.

## Core Operational Modules

* **Inventory Controller:** A centralized dashboard displaying current stock, sorted automatically by urgency (closest expiration date first).
* **Meal Discovery Lab:** An automated assistant that suggests recipes based on available stock. It includes a "Seasoning Check" that identifies if the user is missing the necessary spices or oils for a specific dish.
* **Pantry Vault:** A dedicated management area for long-term staples, ensuring the user always has a record of their base cooking ingredients.
* **Sustainability Metrics:** Visualizes the health of the kitchen environment through color-coded status indicators (Red/Organge/Green).

## Tech Stack

* **Language:** Python 3.10+
* **Interface Engine:** Streamlit
* **Data Transformation:** Pandas
* **Temporal Logic:** Python Datetime

---

Launch the App Live: [smartfridge-v1.streamlit.app](https://streamlit.app)
