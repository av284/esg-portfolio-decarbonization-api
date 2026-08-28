from http.server import BaseHTTPRequestHandler
import json

PORTFOLIO_DATA = {
    "AAPL": {"name": "Apple Inc.", "revenue_m": 383285, "scope_1_2_tco2e": 324100, "sector": "Technology"},
    "MSFT": {"name": "Microsoft Corp.", "revenue_m": 211915, "scope_1_2_tco2e": 400400, "sector": "Technology"},
    "TSLA": {"name": "Tesla Inc.", "revenue_m": 96773, "scope_1_2_tco2e": 1210000, "sector": "Automotive"},
    "XOM":  {"name": "Exxon Mobil Corp.", "revenue_m": 344582, "scope_1_2_tco2e": 60000000, "sector": "Energy"}
}

def calculate_waci(holdings: dict) -> dict:
    waci_score = 0
    breakdown = []

    for ticker, weight_pct in holdings.items():
        if ticker in PORTFOLIO_DATA:
            company = PORTFOLIO_DATA[ticker]
            intensity = company["scope_1_2_tco2e"] / company["revenue_m"]
            weighted_intensity = intensity * (weight_pct / 100.0)
            waci_score += weighted_intensity

            breakdown.append({
                "ticker": ticker,
                "name": company["name"],
                "portfolio_weight": f"{weight_pct}%",
                "carbon_intensity": round(intensity, 2),
                "weighted_contribution": round(weighted_intensity, 2)
            })

    return {
        "portfolio_waci_tco2e_per_m_rev": round(waci_score, 2),
        "target_net_zero_2030_waci": 50.0,
        "alignment_status": "Aligned" if waci_score <= 50.0 else "Action Required (High Carbon Exposure)",
        "holdings_breakdown": breakdown
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        default_holdings = {"AAPL": 40, "MSFT": 30, "XOM": 30}
        results = calculate_waci(default_holdings)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results, indent=2).encode('utf-8'))
