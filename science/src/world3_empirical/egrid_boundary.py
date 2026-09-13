"""Reconcile eGRID plant totals with unit and generator accounting boundaries."""
import math


def _positive(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Invalid {label}")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"Invalid {label}")
    return value


def _close(left, right):
    return abs(left - right) <= max(1e-6, 1e-9 * max(abs(left), abs(right)))


def reconcile_boundaries(year, plant_rows, unit_rows, generator_rows, plant_ids):
    """Return deterministic evidence summaries for a reviewed set of plants."""
    requested = set(plant_ids)
    if not requested:
        raise ValueError("No requested plants")
    plants = {}
    for row in plant_rows:
        plant = row.get("ORISPL")
        if plant not in requested:
            continue
        if plant in plants:
            raise ValueError("Duplicate plant-year")
        if row.get("YEAR") != year:
            raise ValueError("Unexpected plant year")
        plants[plant] = row
    if set(plants) != requested:
        raise ValueError("Requested plant is absent")

    grouped_units = {plant: [] for plant in requested}
    grouped_generators = {plant: [] for plant in requested}
    for row, grouped, label in (
        *[(row, grouped_units, "unit") for row in unit_rows],
        *[(row, grouped_generators, "generator") for row in generator_rows],
    ):
        plant = row.get("ORISPL")
        if plant in requested:
            if row.get("YEAR") != year:
                raise ValueError(f"Unexpected {label} year")
            grouped[plant].append(row)

    output = []
    for plant in sorted(requested):
        row = plants[plant]
        units = grouped_units[plant]
        generators = grouped_generators[plant]
        if not units or not generators:
            raise ValueError("Plant has an empty accounting component")
        plant_generation = _positive(row.get("PLNGENAN"), "plant generation")
        plant_heat = _positive(row.get("UNHTI"), "plant heat")
        plant_co2 = _positive(row.get("UNCO2"), "plant CO2")
        generator_generation = math.fsum(
            _positive(item.get("GENNTAN"), "generator generation") for item in generators
        )
        unit_heat = math.fsum(_positive(item.get("HTIAN"), "unit heat") for item in units)
        unit_co2 = math.fsum(_positive(item.get("CO2AN"), "unit CO2") for item in units)
        output.append({
            "plant_id": plant,
            "plant_name": row.get("PNAME"),
            "year": year,
            "plant_nameplate_capacity_mw": _positive(row.get("NAMEPCAP"), "capacity"),
            "plant_net_generation_mwh": plant_generation,
            "generator_net_generation_sum_mwh": generator_generation,
            "plant_unadjusted_heat_input_mmbtu": plant_heat,
            "unit_heat_input_sum_mmbtu": unit_heat,
            "plant_unadjusted_co2_short_tons": plant_co2,
            "unit_co2_sum_short_tons": unit_co2,
            "reported_heat_rate_btu_per_net_kwh": 1000 * plant_heat / plant_generation,
            "plant_generation_matches_generator_sum": _close(plant_generation, generator_generation),
            "plant_heat_matches_unit_sum": _close(plant_heat, unit_heat),
            "plant_co2_matches_unit_sum": _close(plant_co2, unit_co2),
            "plant_heat_source": row.get("UNHTISRC"),
            "plant_generation_sources": sorted(set(item.get("GENERSRC") for item in generators)),
            "units": [{
                "unit_id": item.get("UNITID"),
                "prime_mover": item.get("PRMVR"),
                "status": item.get("UNTOPST"),
                "primary_fuel": item.get("FUELU1"),
                "associated_generators": item.get("NUMGEN"),
                "heat_input_mmbtu": item.get("HTIAN"),
                "heat_source": item.get("HTIANSRC"),
            } for item in sorted(units, key=lambda item: str(item.get("UNITID")))],
            "generators": [{
                "generator_id": item.get("GENID"),
                "prime_mover": item.get("PRMVR"),
                "status": item.get("GENSTAT"),
                "primary_fuel": item.get("FUELG1"),
                "nameplate_capacity_mw": item.get("NAMEPCAP"),
                "net_generation_mwh": item.get("GENNTAN"),
                "generation_source": item.get("GENERSRC"),
                "online_year": item.get("GENYRONL"),
            } for item in sorted(generators, key=lambda item: str(item.get("GENID")))],
        })
    return output


def compare_years(records):
    """Describe roster and ratio changes without assigning a causal label."""
    by_plant = {}
    for row in records:
        key = row["plant_id"]
        if row["year"] in by_plant.setdefault(key, {}):
            raise ValueError("Duplicate reconciled plant-year")
        by_plant[key][row["year"]] = row
    transitions = []
    for plant in sorted(by_plant):
        years = sorted(by_plant[plant])
        for left_year, right_year in zip(years, years[1:]):
            if right_year != left_year + 1:
                raise ValueError("Reconciled years must be consecutive")
            left, right = by_plant[plant][left_year], by_plant[plant][right_year]
            left_ids = {str(row["generator_id"]) for row in left["generators"]}
            right_ids = {str(row["generator_id"]) for row in right["generators"]}
            transitions.append({
                "plant_id": plant,
                "from_year": left_year,
                "to_year": right_year,
                "added_generator_ids": sorted(right_ids - left_ids),
                "removed_generator_ids": sorted(left_ids - right_ids),
                "nameplate_capacity_ratio": right["plant_nameplate_capacity_mw"] / left["plant_nameplate_capacity_mw"],
                "net_generation_ratio": right["plant_net_generation_mwh"] / left["plant_net_generation_mwh"],
                "heat_input_ratio": right["plant_unadjusted_heat_input_mmbtu"] / left["plant_unadjusted_heat_input_mmbtu"],
                "reported_heat_rate_ratio": right["reported_heat_rate_btu_per_net_kwh"] / left["reported_heat_rate_btu_per_net_kwh"],
            })
    return transitions
