# ESG Portfolio Decarbonization Engine

An interactive scenario modeling engine for portfolio managers and ESG analysts to calculate real-time Weighted Average Carbon Intensity (WACI) and evaluate portfolio alignment against Net Zero 2030 pathways.

Live Application: https://esg-portfolio-decarbonization-api.vercel.app/

---

## Overview

This tool enables dynamic portfolio rebalancing across core equity holdings to simulate carbon exposure reduction. Built in compliance with TCFD and GHG Protocol reporting standards, the engine recalculates portfolio carbon metrics dynamically as target weights shift.

### Key Capabilities
* Dynamic WACI Modeling: Real-time calculation of weighted carbon intensity per million dollars of revenue (tCO2e / $M Rev).
* Net Zero Pathway Alignment: Instant threshold checking against a 2030 benchmark (50.0 tCO2e / $M).
* Asset Breakdown & Visual Analytics: Normalized weight attribution and dynamic visual breakdown of per-asset WACI contributions using Chart.js.

---

## Financial Methodology & Calculations

### Weighted Average Carbon Intensity (WACI)
The core engine computes portfolio carbon intensity by aggregating each holding's Scope 1 and Scope 2 operational carbon intensity, scaled by its normalized portfolio weight:

$$\text{Portfolio WACI} = \sum_{i=1}^{n} \left( w_i \times \frac{\text{Scope 1} + \text{Scope 2 Emissions}_i}{\text{Revenue}_i} \right)$$

*Where $w_i$ represents the dynamically normalized portfolio weight ($\sum w_i = 1.0$).*

### Baseline Asset Operational Data

| Ticker | Company Name | Scope 1 & 2 Emissions (tCO2e) | Revenue ($) | Carbon Intensity (tCO2e / $M) |
| :--- | :--- | :--- | :--- | :--- |
| **AAPL** | Apple Inc. | 58,500 | $416,300,000,000 | **0.13** |
| **MSFT** | Microsoft Corp. | 143,500 | $245,100,000,000 | **0.59** |
| **TSLA** | Tesla, Inc. | 1,060,000 | $96,800,000,000 | **10.92** |
| **XOM** | Exxon Mobil Corp. | 104,000,000 | $323,900,000,000 | **321.08** |

---

## Tech Stack

* Frontend: HTML5, CSS3, JavaScript (ES6+), Chart.js
* Backend: Python / Node.js (Vercel Serverless Functions)
* Deployment & CI/CD: GitHub, Vercel

