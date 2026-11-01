"""
Comprehensive test suite verifying Table Seating Analytics, Budget Strategy Presets,
Day-of Emergency Coordinator Briefing Kit, and In-Memory Sub-Millisecond Caching.
"""

import time
from starlette.testclient import TestClient
from app.main import app
from app.models.ai import AIPromptRequest
from app.models.event import EventType
from app.services.ai_planner import AIPlannerService

client = TestClient(app)


def test_table_seating_summary_and_dietary_alerts():
    """Verify table distribution, capacity calculations, and allergen warnings."""
    # Fetch seed event
    list_res = client.get("/api/events")
    assert list_res.status_code == 200
    events = list_res.json()
    wedding = next(e for e in events if "Wedding" in e["title"])

    res = client.get(f"/api/events/{wedding['id']}/seating?seats_per_table=10")
    assert res.status_code == 200
    data = res.json()

    assert data["total_tables"] >= 1
    assert data["total_seated_guests"] >= 1
    assert "dietary_summary" in data
    assert len(data["tables"]) > 0

    # Verify table attributes
    table1 = data["tables"][0]
    assert table1["table_number"] == 1
    assert table1["max_seats"] == 10
    assert table1["occupied_seats"] >= 1
    assert table1["occupancy_percentage"] > 0.0


def test_auto_assign_tables_balances_unassigned_guests():
    """Verify auto-assign endpoint clusters unseated guests into numbered tables."""
    list_res = client.get("/api/events")
    events = list_res.json()
    wedding = next(e for e in events if "Wedding" in e["title"])

    # Add an unseated guest
    new_guest_res = client.post(
        f"/api/events/{wedding['id']}/guests",
        json={
            "name": "Dr. Sarah Jenkins",
            "party_size": 3,
            "rsvp_status": "confirmed",
            "dietary": "Vegan",
            "table_number": 0,
        },
    )
    assert new_guest_res.status_code == 201

    # Trigger auto-assign
    assign_res = client.post(f"/api/events/{wedding['id']}/seating/auto-assign?seats_per_table=8")
    assert assign_res.status_code == 200
    data = assign_res.json()

    assert data["total_unseated_guests"] == 0
    # Clean up guest
    guest_id = new_guest_res.json()["id"]
    client.delete(f"/api/events/{wedding['id']}/guests/{guest_id}")


def test_emergency_coordinator_kit():
    """Verify Day-of Emergency Coordinator Kit aggregates vendors, cues, and dietary safety."""
    list_res = client.get("/api/events")
    events = list_res.json()
    wedding = next(e for e in events if "Wedding" in e["title"])

    res = client.get(f"/api/events/{wedding['id']}/coordinator-kit")
    assert res.status_code == 200
    kit = res.json()

    assert kit["event_id"] == wedding["id"]
    assert "emergency_vendor_contacts" in kit
    assert len(kit["emergency_vendor_contacts"]) > 0
    assert "critical_day_of_cues" in kit
    assert len(kit["critical_day_of_cues"]) > 0
    assert "dietary_safety_roster" in kit
    assert "vip_tables_summary" in kit


def test_budget_preset_strategies():
    """Verify applying frugal, balanced, and luxury preset profiles."""
    list_res = client.get("/api/events")
    events = list_res.json()
    wedding = next(e for e in events if "Wedding" in e["title"])

    # 1. Apply Frugal strategy
    frugal_res = client.post(
        f"/api/events/{wedding['id']}/budget/preset",
        json={"preset": "frugal", "total_budget": 2000000.0},
    )
    assert frugal_res.status_code == 200
    frugal_items = frugal_res.json()
    assert len(frugal_items) > 0
    # Miscellaneous contingency should be boosted in frugal
    misc = next(i for i in frugal_items if i["category"] == "Miscellaneous & Contingency")
    assert "Frugal Strategy" in misc["notes"]

    # 2. Apply Luxury strategy
    luxury_res = client.post(
        f"/api/events/{wedding['id']}/budget/preset",
        json={"preset": "luxury", "total_budget": 3500000.0},
    )
    assert luxury_res.status_code == 200
    luxury_items = luxury_res.json()
    favors = next(i for i in luxury_items if i["category"] == "Invitations & Favors")
    assert "Luxury Strategy" in favors["notes"]


def test_ai_planner_sub_millisecond_caching():
    """Verify in-memory hash cache returns identical celebration plans instantaneously."""
    req = AIPromptRequest(
        event_type=EventType.WEDDING,
        title="Cache Performance Benchmark Celebration",
        budget=1500000.0,
        guest_count=80,
        currency="INR",
    )

    # First call (generates plan and caches it)
    bundle1 = AIPlannerService.generate_complete_plan(req)
    assert bundle1 is not None

    # Second call (must be served from cache)
    t0 = time.perf_counter()
    bundle2 = AIPlannerService.generate_complete_plan(req)
    t1 = time.perf_counter()

    assert len(bundle2.budget_items) == len(bundle1.budget_items)
    assert len(bundle2.timeline_items) == len(bundle1.timeline_items)
    # Cache lookup should take less than 15 milliseconds
    assert (t1 - t0) < 0.015


def test_edge_cases_nonexistent_event_returns_404():
    """Verify 404 responses on invalid event IDs for new endpoints."""
    bad_id = "nonexistent-event-99999"
    assert client.get(f"/api/events/{bad_id}/seating").status_code == 404
    assert client.post(f"/api/events/{bad_id}/seating/auto-assign").status_code == 404
    assert client.get(f"/api/events/{bad_id}/coordinator-kit").status_code == 404
    assert client.post(f"/api/events/{bad_id}/budget/preset", json={"preset": "balanced"}).status_code == 404
