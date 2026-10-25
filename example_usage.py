from client import VoyagerTravelOptimizerClient
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

def main():
    voyager = VoyagerTravelOptimizerClient()
    print("=== VOYAGER MULTI-MODAL TRAVEL ROUTE OPTIMIZER ===")

    # Typical regional intercity corridor: 600 km journey
    res = voyager.compare_routes(distance_km=600.0, passenger_count=2)
    print()
    print(f"Journey: 600.0 km (2 Passengers) | Recommended: {res['recommended_mode']}")
    print()
    for m in res['modal_comparisons']:
        print(f"  Mode: {m['mode']}")
        print(f"    Time: {m['transit_time_hours']} hrs | Cost: ${m['monetary_cost_usd']} | CO2: {m['carbon_emissions_kg']} kg")
        print(f"    Total Social Cost (Incl. Carbon Tax): ${m['total_social_cost_usd']}")

if __name__ == "__main__":
    main()
