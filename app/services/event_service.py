"""
Event Service for CelebraTech AI Event Planner.
Provides thread-safe state management, CRUD operations, item manipulation,
guest tracking, and pre-seeded reference events for instant evaluation.
"""

from typing import List, Optional, Dict
from datetime import datetime, timezone
import threading
from app.models.event import (
    EventPlan,
    EventCreateRequest,
    EventUpdateRequest,
    BudgetItem,
    TimelineItem,
    VendorItem,
    PersonalizedIdeaItem,
    GuestItem,
    GuestRSVPStatus,
    EventType,
    VendorStatus,
    BudgetCategory,
    TableGuestInfo,
    TableInfo,
    TableSeatingSummary,
    EmergencyCoordinatorKit,
)
from app.models.ai import AIPromptRequest
from app.services.ai_planner import AIPlannerService


class EventService:
    """Thread-safe event repository and workflow coordinator."""

    def __init__(self) -> None:
        self._events: Dict[str, EventPlan] = {}
        self._lock = threading.RLock()
        self._initialize_seed_data()

    def _initialize_seed_data(self) -> None:
        """Seed rich, realistic showcase events for Weddings, Birthdays, and Community."""
        wedding_req = AIPromptRequest(
            event_type=EventType.WEDDING,
            title="Elegance & Blooms: Sofia & Julian's Wedding",
            budget=2800000.0,
            guest_count=120,
            location="The Leela Palace & Royal Gardens, Udaipur",
            theme_preference="Royal Sunset & Marigold Silk Elegance",
            vibe="Romantic, candle-lit, royal and timeless",
            additional_notes="Include outdoor cocktail hour and live acoustic ceremony music",
            currency="INR",
        )
        wedding_bundle = AIPlannerService.generate_complete_plan(wedding_req)
        wedding_plan = EventPlan(
            id="seed-wedding-001",
            title=wedding_req.title,
            event_type=wedding_req.event_type,
            date="2026-11-14",
            location=wedding_req.location,
            guest_count=wedding_req.guest_count,
            currency="INR",
            total_budget=wedding_req.budget,
            theme=wedding_req.theme_preference,
            vibe=wedding_req.vibe,
            budget_items=wedding_bundle.budget_items,
            timeline_items=wedding_bundle.timeline_items,
            vendors=wedding_bundle.vendors,
            ideas=wedding_bundle.ideas,
            guests=wedding_bundle.guests,
            color_palette=wedding_bundle.color_palette,
        )
        if wedding_plan.budget_items:
            wedding_plan.budget_items[0].actual_cost = wedding_plan.budget_items[0].estimated_cost
            wedding_plan.budget_items[0].paid = True
        if wedding_plan.timeline_items:
            wedding_plan.timeline_items[0].completed = True
        self._events[wedding_plan.id] = wedding_plan

        # Seed Birthday Event
        birthday_req = AIPromptRequest(
            event_type=EventType.BIRTHDAY,
            title="Marcus's Electric Neon 30th Birthday Bash",
            budget=350000.0,
            guest_count=50,
            location="Skyline Penthouse Lounge, Bengaluru",
            theme_preference="Neon Noir & Retro Cyber Lounge",
            vibe="High energy, playful, neon glow, upbeat music",
            additional_notes="360 photo booth and signature nitro dessert bar",
            currency="INR",
        )
        bday_bundle = AIPlannerService.generate_complete_plan(birthday_req)
        bday_plan = EventPlan(
            id="seed-birthday-002",
            title=birthday_req.title,
            event_type=birthday_req.event_type,
            date="2026-12-05",
            location=birthday_req.location,
            guest_count=birthday_req.guest_count,
            currency="INR",
            total_budget=birthday_req.budget,
            theme=birthday_req.theme_preference,
            vibe=birthday_req.vibe,
            budget_items=bday_bundle.budget_items,
            timeline_items=bday_bundle.timeline_items,
            vendors=bday_bundle.vendors,
            ideas=bday_bundle.ideas,
            guests=bday_bundle.guests,
            color_palette=bday_bundle.color_palette,
        )
        self._events[bday_plan.id] = bday_plan

        # Seed Community Event
        community_req = AIPromptRequest(
            event_type=EventType.COMMUNITY,
            title="Greenwood Park Annual Harvest Festival",
            budget=850000.0,
            guest_count=350,
            location="Greenwood Community Grounds & Amphitheatre",
            theme_preference="Harmony Harvest & Neighborhood Unity Festival",
            vibe="Family-friendly, inclusive, eco-friendly, joyful",
            additional_notes="Live community bands, local food trucks, and children's craft village",
            currency="INR",
        )
        community_bundle = AIPlannerService.generate_complete_plan(community_req)
        community_plan = EventPlan(
            id="seed-community-003",
            title=community_req.title,
            event_type=community_req.event_type,
            date="2026-10-31",
            location=community_req.location,
            guest_count=community_req.guest_count,
            currency="INR",
            total_budget=community_req.budget,
            theme=community_req.theme_preference,
            vibe=community_req.vibe,
            budget_items=community_bundle.budget_items,
            timeline_items=community_bundle.timeline_items,
            vendors=community_bundle.vendors,
            ideas=community_bundle.ideas,
            guests=community_bundle.guests,
            color_palette=community_bundle.color_palette,
        )
        self._events[community_plan.id] = community_plan

    def list_events(self) -> List[EventPlan]:
        with self._lock:
            events = list(self._events.values())
            return sorted(events, key=lambda e: e.updated_at, reverse=True)

    def get_event(self, event_id: str) -> Optional[EventPlan]:
        with self._lock:
            return self._events.get(event_id)

    def create_event(self, req: EventCreateRequest) -> EventPlan:
        now_str = datetime.now(timezone.utc).isoformat()
        plan = EventPlan(
            title=req.title,
            event_type=req.event_type,
            date=req.date or None,
            location=req.location or "To be determined",
            guest_count=req.guest_count,
            currency=req.currency or "INR",
            total_budget=req.total_budget,
            theme=req.theme or f"Celebration of {req.title}",
            vibe=req.vibe or "Warm, memorable, and celebratory",
            created_at=now_str,
            updated_at=now_str,
        )

        if req.generate_ai_plan:
            ai_req = AIPromptRequest(
                event_type=req.event_type,
                title=req.title,
                budget=req.total_budget,
                guest_count=req.guest_count,
                location=req.location,
                theme_preference=req.theme,
                vibe=req.vibe,
                currency=req.currency,
            )
            bundle = AIPlannerService.generate_complete_plan(ai_req)
            plan.budget_items = bundle.budget_items
            plan.timeline_items = bundle.timeline_items
            plan.vendors = bundle.vendors
            plan.ideas = bundle.ideas
            plan.guests = bundle.guests
            plan.color_palette = bundle.color_palette

        with self._lock:
            self._events[plan.id] = plan
        return plan

    def update_event(self, event_id: str, req: EventUpdateRequest) -> Optional[EventPlan]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            update_data = req.model_dump(exclude_unset=True)
            for key, val in update_data.items():
                if val is not None:
                    setattr(event, key, val)
            event.updated_at = datetime.now(timezone.utc).isoformat()
            return event

    def delete_event(self, event_id: str) -> bool:
        with self._lock:
            if event_id in self._events:
                del self._events[event_id]
                return True
            return False

    # Cross-Tab Synchronization Helpers
    def _sync_vendor_to_budget(self, event: EventPlan, vendor: VendorItem, actual_paid: Optional[float] = None) -> None:
        """Synchronize vendor payments and status directly with budget items preserving actual spent."""
        v_name_lower = (vendor.name or "").lower().strip()
        v_cat_lower = (vendor.category or "").lower().strip()
        matched_item: Optional[BudgetItem] = None

        for b in event.budget_items:
            b_name_lower = (b.name or "").lower().strip()
            b_cat_lower = (b.category or "").lower().strip()
            if (
                v_name_lower in b_name_lower
                or b_name_lower in v_name_lower
                or (b.notes and vendor.id in b.notes)
                or (b_cat_lower == v_cat_lower and abs(b.estimated_cost - vendor.quoted_price) < 0.01)
            ):
                matched_item = b
                break

        if vendor.status == VendorStatus.FULLY_PAID:
            final_cost = (
                actual_paid
                if actual_paid is not None
                else (matched_item.actual_cost if matched_item and matched_item.actual_cost > 0 else vendor.quoted_price)
            )
            if matched_item:
                matched_item.paid = True
                matched_item.actual_cost = round(float(final_cost), 2)
            else:
                new_item = BudgetItem(
                    category=vendor.category or BudgetCategory.MISCELLANEOUS.value,
                    name=vendor.name,
                    estimated_cost=vendor.quoted_price,
                    actual_cost=round(float(final_cost), 2),
                    paid=True,
                    notes=f"Vendor contract settled ({vendor.name})",
                )
                event.budget_items.append(new_item)
        elif vendor.status == VendorStatus.DEPOSIT_PAID:
            deposit_amount = round(vendor.quoted_price * 0.5, 2)
            if matched_item:
                if matched_item.actual_cost == 0:
                    matched_item.actual_cost = deposit_amount
            else:
                new_item = BudgetItem(
                    category=vendor.category or BudgetCategory.MISCELLANEOUS.value,
                    name=vendor.name,
                    estimated_cost=vendor.quoted_price,
                    actual_cost=deposit_amount,
                    paid=False,
                    notes=f"50% deposit paid ({vendor.name})",
                )
                event.budget_items.append(new_item)
        elif vendor.status in [VendorStatus.RESEARCHING, VendorStatus.CONTACTED, VendorStatus.QUOTE_RECEIVED]:
            if matched_item and matched_item.paid:
                matched_item.paid = False

    def _sync_budget_to_vendor(self, event: EventPlan, budget_item: BudgetItem) -> None:
        """Synchronize budget item payment status directly with corresponding vendor."""
        b_name_lower = (budget_item.name or "").lower().strip()
        b_cat_lower = (budget_item.category or "").lower().strip()

        for v in event.vendors:
            v_name_lower = (v.name or "").lower().strip()
            v_cat_lower = (v.category or "").lower().strip()
            if (
                v_name_lower in b_name_lower
                or b_name_lower in v_name_lower
                or (budget_item.notes and v.id in budget_item.notes)
                or (v_cat_lower == b_cat_lower and abs(v.quoted_price - budget_item.estimated_cost) < 0.01)
            ):
                if budget_item.paid:
                    v.status = VendorStatus.FULLY_PAID
                elif v.status == VendorStatus.FULLY_PAID and not budget_item.paid:
                    v.status = VendorStatus.CONTRACT_SIGNED
                break

    # Budget Item operations
    def add_budget_item(self, event_id: str, item: BudgetItem) -> Optional[BudgetItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            event.budget_items.append(item)
            self._sync_budget_to_vendor(event, item)
            event.updated_at = datetime.now(timezone.utc).isoformat()
            return item

    def update_budget_item(self, event_id: str, item_id: str, updated_item: BudgetItem) -> Optional[BudgetItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for idx, item in enumerate(event.budget_items):
                if item.id == item_id:
                    updated_item.id = item_id
                    event.budget_items[idx] = updated_item
                    self._sync_budget_to_vendor(event, updated_item)
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return updated_item
            return None

    def record_budget_payment(
        self,
        event_id: str,
        item_id: str,
        actual_cost: float,
        paid: bool = True,
        notes: Optional[str] = None,
    ) -> Optional[BudgetItem]:
        """Record exact actual payment spent on a budget line item and synchronize."""
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for item in event.budget_items:
                if item.id == item_id:
                    item.actual_cost = max(0.0, round(float(actual_cost), 2))
                    item.paid = paid
                    if notes is not None:
                        item.notes = notes
                    self._sync_budget_to_vendor(event, item)
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return item
            return None

    def toggle_budget_item_paid(
        self,
        event_id: str,
        item_id: str,
        actual_cost: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Optional[BudgetItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for item in event.budget_items:
                if item.id == item_id:
                    if actual_cost is not None:
                        item.actual_cost = max(0.0, round(float(actual_cost), 2))
                        item.paid = True
                    else:
                        item.paid = not item.paid
                        if item.paid and item.actual_cost == 0:
                            item.actual_cost = item.estimated_cost
                    if notes is not None:
                        item.notes = notes
                    self._sync_budget_to_vendor(event, item)
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return item
            return None

    def settle_vendor_payment(
        self,
        event_id: str,
        vendor_id: str,
        actual_paid: float,
        notes: Optional[str] = None,
    ) -> Optional[VendorItem]:
        """Settle vendor contract with actual payment amount and sync with budget ledger."""
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for v in event.vendors:
                if v.id == vendor_id:
                    v.status = VendorStatus.FULLY_PAID
                    v.actual_paid = round(float(actual_paid), 2)
                    if notes:
                        v.notes = notes
                    self._sync_vendor_to_budget(event, v, actual_paid=actual_paid)
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return v
            return None

    def delete_budget_item(self, event_id: str, item_id: str) -> bool:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return False
            initial_len = len(event.budget_items)
            event.budget_items = [i for i in event.budget_items if i.id != item_id]
            if len(event.budget_items) < initial_len:
                event.updated_at = datetime.now(timezone.utc).isoformat()
                return True
            return False

    # Timeline operations
    def add_timeline_item(self, event_id: str, item: TimelineItem) -> Optional[TimelineItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            item.order = len(event.timeline_items) + 1
            event.timeline_items.append(item)
            event.updated_at = datetime.now(timezone.utc).isoformat()
            return item

    def toggle_timeline_item(self, event_id: str, item_id: str) -> Optional[TimelineItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for item in event.timeline_items:
                if item.id == item_id:
                    item.completed = not item.completed
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return item
            return None

    def delete_timeline_item(self, event_id: str, item_id: str) -> bool:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return False
            initial_len = len(event.timeline_items)
            event.timeline_items = [i for i in event.timeline_items if i.id != item_id]
            if len(event.timeline_items) < initial_len:
                event.updated_at = datetime.now(timezone.utc).isoformat()
                return True
            return False

    # Vendor operations
    def add_vendor(self, event_id: str, vendor: VendorItem) -> Optional[VendorItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            event.vendors.append(vendor)
            self._sync_vendor_to_budget(event, vendor)
            event.updated_at = datetime.now(timezone.utc).isoformat()
            return vendor

    def update_vendor_status(self, event_id: str, vendor_id: str, status: VendorStatus) -> Optional[VendorItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for v in event.vendors:
                if v.id == vendor_id:
                    v.status = status
                    if status == VendorStatus.FULLY_PAID:
                        if v.actual_paid is None or v.actual_paid == 0:
                            v.actual_paid = v.quoted_price
                    elif status != VendorStatus.DEPOSIT_PAID:
                        v.actual_paid = None
                    self._sync_vendor_to_budget(event, v, actual_paid=v.actual_paid)
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return v
            return None

    def toggle_vendor_task(self, event_id: str, vendor_id: str, task: str) -> Optional[VendorItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for v in event.vendors:
                if v.id == vendor_id:
                    if task in v.completed_tasks:
                        v.completed_tasks.remove(task)
                    else:
                        v.completed_tasks.append(task)
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return v
            return None

    def delete_vendor(self, event_id: str, vendor_id: str) -> bool:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return False
            initial_len = len(event.vendors)
            event.vendors = [v for v in event.vendors if v.id != vendor_id]
            if len(event.vendors) < initial_len:
                event.updated_at = datetime.now(timezone.utc).isoformat()
                return True
            return False

    # Guest operations
    def add_guest(self, event_id: str, guest: GuestItem) -> Optional[GuestItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            event.guests.append(guest)
            event.updated_at = datetime.now(timezone.utc).isoformat()
            return guest

    def update_guest_rsvp(self, event_id: str, guest_id: str, rsvp_status: GuestRSVPStatus) -> Optional[GuestItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            for g in event.guests:
                if g.id == guest_id:
                    g.rsvp_status = rsvp_status
                    event.updated_at = datetime.now(timezone.utc).isoformat()
                    return g
            return None

    def delete_guest(self, event_id: str, guest_id: str) -> bool:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return False
            initial_len = len(event.guests)
            event.guests = [g for g in event.guests if g.id != guest_id]
            if len(event.guests) < initial_len:
                event.updated_at = datetime.now(timezone.utc).isoformat()
                return True
            return False

    # Idea operations
    def add_idea(self, event_id: str, idea: PersonalizedIdeaItem) -> Optional[PersonalizedIdeaItem]:
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            event.ideas.append(idea)
            event.updated_at = datetime.now(timezone.utc).isoformat()
            return idea


    # Seating & Capacity Analytics
    def get_table_seating_summary(self, event_id: str, seats_per_table: int = 10) -> Optional[TableSeatingSummary]:
        """
        Calculate table occupancy rates, guest distribution, and dietary flags per table.

        Args:
            event_id: Unique event identifier.
            seats_per_table: Max capacity per table (default: 10).

        Returns:
            TableSeatingSummary or None if event not found.
        """
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None

            tables_map: Dict[int, TableInfo] = {}
            unseated_count = 0
            seated_count = 0
            dietary_totals: Dict[str, int] = {}

            for guest in event.guests:
                # Track global dietary needs
                diet = guest.dietary if guest.dietary else "Standard"
                dietary_totals[diet] = dietary_totals.get(diet, 0) + guest.party_size

                if guest.table_number and guest.table_number > 0:
                    t_num = guest.table_number
                    if t_num not in tables_map:
                        tables_map[t_num] = TableInfo(
                            table_number=t_num,
                            max_seats=seats_per_table,
                            occupied_seats=0,
                            available_seats=seats_per_table,
                            occupancy_percentage=0.0,
                            dietary_alerts=[],
                            guests=[],
                        )
                    table = tables_map[t_num]
                    table.guests.append(
                        TableGuestInfo(
                            name=guest.name,
                            party_size=guest.party_size,
                            dietary=diet,
                            rsvp_status=guest.rsvp_status,
                        )
                    )
                    table.occupied_seats += guest.party_size
                    table.available_seats = max(0, table.max_seats - table.occupied_seats)
                    table.occupancy_percentage = round((table.occupied_seats / table.max_seats) * 100, 1)
                    if diet != "Standard" and diet not in table.dietary_alerts:
                        table.dietary_alerts.append(f"{diet} ({guest.name})")
                    seated_count += guest.party_size
                else:
                    unseated_count += guest.party_size

            sorted_tables = [tables_map[k] for k in sorted(tables_map.keys())]
            total_seats_capacity = len(sorted_tables) * seats_per_table
            utilization = round((seated_count / total_seats_capacity * 100), 1) if total_seats_capacity > 0 else 0.0

            return TableSeatingSummary(
                total_tables=len(sorted_tables),
                total_seated_guests=seated_count,
                total_unseated_guests=unseated_count,
                capacity_utilization_rate=utilization,
                dietary_summary=dietary_totals,
                tables=sorted_tables,
            )

    def auto_assign_tables(self, event_id: str, seats_per_table: int = 8) -> Optional[TableSeatingSummary]:
        """
        Intelligently assign unseated guests to reception tables respecting party sizes.

        Args:
            event_id: Unique event identifier.
            seats_per_table: Target capacity per table.

        Returns:
            Updated TableSeatingSummary.
        """
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None

            current_table = 1
            current_occupancy = 0

            # Sort unseated guests or re-assign seamlessly
            for guest in event.guests:
                if not guest.table_number or guest.table_number <= 0:
                    if current_occupancy + guest.party_size > seats_per_table:
                        current_table += 1
                        current_occupancy = 0
                    guest.table_number = current_table
                    current_occupancy += guest.party_size

            event.updated_at = datetime.now(timezone.utc).isoformat()

        return self.get_table_seating_summary(event_id, seats_per_table=seats_per_table)

    def get_emergency_coordinator_kit(self, event_id: str) -> Optional[EmergencyCoordinatorKit]:
        """
        Compile an all-in-one Day-of Emergency Coordinator Briefing Kit.

        Args:
            event_id: Unique event identifier.

        Returns:
            EmergencyCoordinatorKit containing contacts, cues, seating, and dietary flags.
        """
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None

            # 1. Emergency Vendor Contacts
            vendor_contacts = []
            for v in event.vendors:
                vendor_contacts.append({
                    "name": v.name,
                    "category": v.category,
                    "contact_person": v.contact_name or "Manager on Duty",
                    "phone_or_email": v.phone or v.email or "On File",
                    "status": v.status.value,
                    "actual_paid": v.actual_paid or 0.0,
                    "deposit_paid": v.status in (VendorStatus.DEPOSIT_PAID, VendorStatus.FULLY_PAID),
                    "notes": v.notes or "None",
                })

            # 2. Critical Day-of Cues (sorted by time)
            day_of_cues = []
            for t in sorted(event.timeline_items, key=lambda x: x.order):
                if t.phase.value == "day_of":
                    day_of_cues.append({
                        "time": t.time_or_offset,
                        "cue": t.title,
                        "owner": t.owner or "Lead Coordinator",
                        "description": t.description or "",
                    })

            # 3. Dietary Safety Alert Matrix
            dietary_safety: Dict[str, List[str]] = {}
            vip_tables: List[Dict[str, Any]] = []

            for g in event.guests:
                diet = g.dietary if g.dietary else "Standard"
                if diet != "Standard":
                    if diet not in dietary_safety:
                        dietary_safety[diet] = []
                    dietary_safety[diet].append(f"{g.name} (Table {g.table_number or 'Unassigned'})")

            # 4. VIP Seating summary
            table_summary = self.get_table_seating_summary(event_id)
            if table_summary:
                for t in table_summary.tables:
                    vip_tables.append({
                        "table_number": t.table_number,
                        "headcount": t.occupied_seats,
                        "dietary_alerts": t.dietary_alerts,
                        "primary_guests": [g.name for g in t.guests[:3]],
                    })

            return EmergencyCoordinatorKit(
                event_id=event.id,
                event_title=event.title,
                event_type=event.event_type.value,
                date=event.date or "TBD",
                location=event.location or "TBD",
                total_budget=event.total_budget,
                currency=event.currency,
                coordinator_notes="Master Day-of Emergency Protocol Sheet. Keep readily accessible to venue captain and lead coordinator.",
                emergency_vendor_contacts=vendor_contacts,
                critical_day_of_cues=day_of_cues,
                dietary_safety_roster=dietary_safety,
                vip_tables_summary=vip_tables,
            )


event_service = EventService()
