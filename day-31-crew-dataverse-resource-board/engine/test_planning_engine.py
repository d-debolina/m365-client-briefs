"""Acceptance tests with expected numbers (the spec-driven way the brief asks for).

Run:  python -m unittest discover -s engine -p "test_*.py"
"""
import unittest, datetime as dt
from planning_engine import skill_gap, rentals, add_workdays, read


class SkillGap(unittest.TestCase):
    def test_small_case_with_known_numbers(self):
        crew = [{"CrewId": "A", "SkillLevel": "Foreman", "HoursPerWeek": "40"},
                {"CrewId": "B", "SkillLevel": "Journeyman", "HoursPerWeek": "40"},
                {"CrewId": "C", "SkillLevel": "Journeyman", "HoursPerWeek": "40"}]
        demand = [{"ProjectId": "P1", "WeekStart": "2027-01-04", "Kind": "Skill", "Item": "Journeyman", "Quantity": "56"},
                  {"ProjectId": "P2", "WeekStart": "2027-01-04", "Kind": "Skill", "Item": "Journeyman", "Quantity": "40"},
                  {"ProjectId": "P1", "WeekStart": "2027-01-04", "Kind": "Skill", "Item": "Foreman", "Quantity": "16"}]
        leave = [{"CrewId": "C", "WeekStart": "2027-01-04", "HoursOff": "16"}]
        g = skill_gap(demand, crew, leave)
        self.assertEqual(g[("2027-01-04", "Journeyman")], {"demand": 96, "supply": 64, "gap": -32})
        self.assertEqual(g[("2027-01-04", "Foreman")]["gap"], 24)

    def test_full_sample_supply_is_never_negative(self):
        g = skill_gap(read("weekly_demand.csv"), read("crew_members.csv"), read("leave.csv"))
        self.assertTrue(all(v["supply"] >= 0 for v in g.values()))


class Rentals(unittest.TestCase):
    def test_only_units_above_owned_fleet_are_rented(self):
        fleet = [{"EquipmentType": "Telehandler", "OwnedUnits": "2", "RentalPerWeek": "690"}]
        demand = [{"WeekStart": "2027-01-04", "Kind": "Equipment", "Item": "Telehandler", "Quantity": "1"}] * 3
        self.assertEqual(rentals(demand, fleet), {("2027-01-04", "Telehandler"): {"units": 1, "cost": 690}})


class Workdays(unittest.TestCase):
    def test_skips_weekend_and_holiday(self):
        hol = {dt.date(2027, 4, 2), dt.date(2027, 4, 5)}          # fictional Easter break
        self.assertEqual(add_workdays(dt.date(2027, 4, 1), 1, hol), dt.date(2027, 4, 6))
        self.assertEqual(add_workdays(dt.date(2027, 1, 8), 3, set()), dt.date(2027, 1, 13))


if __name__ == "__main__":
    unittest.main()
