from typing import Dict, List

from langchain_core.tools import tool
from serpapi import Client

from src.core import settings
from src.models import (
    FlightsInput,
    FlightsInputSchema,
    HotelsInput,
    HotelsInputSchema,
)
from src.tools.parsers import parse_flight_response, parse_hotel_response


# ------------------------------------------------------------------
# ✈️ Flights Finder Tool
# ------------------------------------------------------------------

@tool(
    args_schema=FlightsInputSchema,
    description=(
        "Search for flights via SerpAPI. "
        "Returns list of flights with airline, departure, arrival, duration, price, and airline logo."
    ),
)
def flights_finder(params: FlightsInput) -> List[Dict]:
    client = Client(api_key=settings["SERPAPI_API_KEY"])
    
    search_params = {
        "engine": "google_flights",
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
    }

    results = client.search(search_params)
    raw_response = results.as_dict()
    
    # Parse and return clean flight data
    return parse_flight_response(raw_response)



# ------------------------------------------------------------------
# 🏨 Hotels Finder Tool
# ------------------------------------------------------------------

@tool(
    args_schema=HotelsInputSchema,
    description=(
        "Search for hotels via SerpAPI. "
        "Returns list of hotels with name, description, rates, rating, check-in/out times, hotel class, and logo."
    ),
)
def hotels_finder(params: HotelsInput) -> List[Dict]:
    client = Client(api_key=settings["SERPAPI_API_KEY"])
    
    search_params = {
        "engine": "google_hotels",
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

    results = client.search(search_params)
    raw_response = results.as_dict()
    
    # Parse and return clean hotel data
    return parse_hotel_response(raw_response)
