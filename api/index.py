from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

PORTFOLIO_DATA = {
    "AAPL": {"name": "Apple Inc.", "revenue_m": 416290, "scope_1_2_tco2e": 58500, "sector": "Technology"},
    "MSFT": {"name": "Microsoft Corp.", "revenue_m": 245107, "scope_1_2_tco2e": 143510, "sector": "Technology"},
    "XOM":  {"name": "Exxon Mobil Corp.", "revenue_m": 323905, "scope_1_2_tco2e": 104000000, "sector": "Energy"},
    "TSLA": {"name": "Tesla Inc.", "revenue_m": 96773, "scope_1_2_tco2e": 1057000, "sector": "Automotive"}
}

def calculate_waci(holdings: dict) -> dict:
    total_weight = sum(holdings.values())
    if total_weight == 0:
        total_weight = 100  # Avoid division by zero
        
    waci_score = 0
    breakdown = []

    for ticker, weight_pct in holdings.items():
        if ticker in PORTFOLIO_DATA:
            company = PORTFOLIO_DATA[ticker]
            # Carbon Intensity = tCO2e / $M Revenue
            intensity = company["scope_1_2_tco2e"] / company["revenue_m"]
            # Normalize weight relative to portfolio sum
            normalized_weight = weight_pct / total_weight
            weighted_intensity = intensity * normalized_weight
            waci_score += weighted_intensity

            breakdown.append({
                "ticker": ticker,
                "name": company["name"],
                "portfolio_weight": f"{round(normalized_weight * 100, 1)}%",
                "raw_weight": weight_pct,
                "carbon_intensity": round(intensity, 2),
                "weighted_contribution": round(weighted_intensity, 2)
            })

    return {
        "portfolio_waci_tco2e_per_m_rev": round(waci_score, 2),
        "target_net_zero_2030_waci": 50.0,
        "alignment_status": "Aligned with 2030 Net Zero Target" if waci_score <= 50.0 else "Action Required (High Carbon Exposure)",
        "holdings_breakdown": breakdown
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)

        # Dynamic query parsing or default allocation
        holdings = {
            "AAPL": float(params.get("aapl", [40])[0]),
            "MSFT": float(params.get("msft", [30])[0]),
            "XOM":  float(params.get("xom", [30])[0]),
            "TSLA": float(params.get("tsla", [0])[0])
        }

        results = calculate_waci(holdings)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results, indent=2).encode('utf-8'))
