from typing import Dict

from langchain_core.tools import tool
from serpapi import GoogleSearch 

from src.core import settings
from src.models import (
    FlightsInput,
    FlightsInputSchema,
    HotelsInput,
    HotelsInputSchema,
)


# ------------------------------------------------------------------
# ✈️ Flights Finder Tool (RAW DATA)
# ------------------------------------------------------------------

@tool(
    args_schema=FlightsInputSchema,
    description=(
        "Fetch raw Google Flights data via SerpAPI. "
        "Returns full SerpAPI response without modification."
    ),
)
def flights_finder(params: FlightsInput) -> Dict:
    search_params = {
        "engine": "google_flights",
        "api_key": settings["SERPAPI_API_KEY"],
        "hl": "en",
        "gl": "in",
        "currency": "INR",
        "departure_id": params.departure_airport,
        "arrival_id": params.arrival_airport,
        "outbound_date": params.outbound_date,
        "return_date": params.return_date,
        "adults": params.adults,
        "children": params.children,
        "infants_in_seat": params.infants_in_seat,
        "infants_on_lap": params.infants_on_lap,
        "stops": "1",
    }

    search = GoogleSearch(search_params)
    return search.get_dict()



# ------------------------------------------------------------------
# 🏨 Hotels Finder Tool (RAW DATA)
# ------------------------------------------------------------------

@tool(
    args_schema=HotelsInputSchema,
    description=(
        "Fetch raw Google Hotels data via SerpAPI. "
        "Returns full SerpAPI response without modification."
    ),
)
def hotels_finder(params: HotelsInput) -> Dict:
    search_params = {
        "engine": "google_hotels",
        "api_key": settings["SERPAPI_API_KEY"],
        "hl": "en",
        "gl": "in",
        "currency": "INR",
        "q": params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "adults": params.adults,
        "children": params.children,
        "rooms": params.rooms,
        "sort_by": params.sort_by,
        "hotel_class": params.hotel_class,
    }

    search = GoogleSearch(search_params)
    return search.get_dict()

