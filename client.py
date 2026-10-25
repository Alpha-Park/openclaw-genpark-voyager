import sys, math
sys.stdout.reconfigure(encoding='utf-8')

class VoyagerTravelOptimizerClient:
    """
    Multi-modal travel routing & sustainability engine.
    Compares air, high-speed rail, and road transit alternatives,
    evaluating monetary expense, door-to-door transit time, and kg CO2 emissions.
    """
    def __init__(self, carbon_price_per_ton=50.0):
        self.carbon_price_per_kg = carbon_price_per_ton / 1000.0

    def compare_routes(self, distance_km, passenger_count=1):
        """
        Calculates Pareto-comparison for transit modes across distance.
        """
        # Emission factors (kg CO2 per passenger-km)
        modes = {
            "COMMERCIAL_FLIGHT": {
                "base_speed_kmh": 750.0,
                "fixed_airport_overhead_hours": 3.0,
                "cost_per_km": 0.16,
                "base_ticket_fee": 60.0,
                "emission_factor": 0.185
            },
            "HIGH_SPEED_RAIL": {
                "base_speed_kmh": 280.0,
                "fixed_airport_overhead_hours": 0.75,
                "cost_per_km": 0.11,
                "base_ticket_fee": 20.0,
                "emission_factor": 0.028
            },
            "EV_RIDESHARE": {
                "base_speed_kmh": 90.0,
                "fixed_airport_overhead_hours": 0.2,
                "cost_per_km": 0.28,
                "base_ticket_fee": 10.0,
                "emission_factor": 0.045
            }
        }

        results = []
        for mode_name, params in modes.items():
            transit_hours = (distance_km / params["base_speed_kmh"]) + params["fixed_airport_overhead_hours"]
            monetary_cost = (params["base_ticket_fee"] + (distance_km * params["cost_per_km"])) * passenger_count
            co2_kg = distance_km * params["emission_factor"] * passenger_count
            carbon_cost = co2_kg * self.carbon_price_per_kg
            total_social_cost = monetary_cost + carbon_cost

            results.append({
                "mode": mode_name,
                "transit_time_hours": round(transit_hours, 2),
                "monetary_cost_usd": round(monetary_cost, 2),
                "carbon_emissions_kg": round(co2_kg, 1),
                "total_social_cost_usd": round(total_social_cost, 2)
            })

        results.sort(key=lambda x: x["total_social_cost_usd"])

        return {
            "status": "success",
            "distance_km": distance_km,
            "passenger_count": passenger_count,
            "recommended_mode": results[0]["mode"],
            "modal_comparisons": results
        }
