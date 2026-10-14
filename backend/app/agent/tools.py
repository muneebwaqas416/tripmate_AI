import airportsdata
import pycountry
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

_AIRPORTS = airportsdata.load("IATA")


@tool
def find_airports(query: str, limit: int = 10) -> list[dict]:
    """Find airports by IATA code, city or airport name (e.g. "LHR", "Paris", "Heathrow")."""
    q = query.strip().lower()
    if not q:
        return []

    exact = _AIRPORTS.get(q.upper())
    if exact:
        return [exact]

    matches = [
        airport
        for airport in _AIRPORTS.values()
        if q in airport["city"].lower() or q in airport["name"].lower()
    ]
    return matches[:limit]


@tool
def country_info(name_or_code: str) -> dict:
    """Look up a country by name or ISO code and return its ISO codes."""
    try:
        country = pycountry.countries.lookup(name_or_code)
    except LookupError:
        try:
            country = pycountry.countries.search_fuzzy(name_or_code)[0]
        except LookupError:
            return {"error": f"No country found for '{name_or_code}'"}

    return {
        "name": country.name,
        "official_name": getattr(country, "official_name", country.name),
        "alpha_2": country.alpha_2,
        "alpha_3": country.alpha_3,
        "flag": getattr(country, "flag", None),
    }


def get_tools() -> list:
    web_search = TavilySearch(max_results=5, name="web_search")
    return [web_search, find_airports, country_info]
