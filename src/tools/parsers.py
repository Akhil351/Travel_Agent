# 📁 tools/parsers.py
# Parsers for cleaning SerpAPI responses

from typing import Dict, List


def parse_flight_response(raw_response: Dict) -> List[Dict]:
    """
    Parse raw SerpAPI flight response and extract essential fields.
    Returns only top 5 best flights.
    
    Args:
        raw_response: Raw response from SerpAPI flights search
        
    Returns:
        List of cleaned flight dictionaries (max 5)
    """
    flights = []
    
    # Get only best_flights (top recommendations)
    best_flights = raw_response.get("best_flights", [])
    
    # Limit to top 5
    top_flights = best_flights[:5]
    
    for flight_option in top_flights:
        # Get flight legs
        flight_legs = flight_option.get("flights", [])
        if not flight_legs:
            continue
        
        # Get first leg (outbound)
        first_leg = flight_legs[0]
        
        # Extract departure info
        dep_airport = first_leg.get("departure_airport", {})
        dep_name = dep_airport.get("name", "Unknown")
        dep_id = dep_airport.get("id", "")
        dep_time = dep_airport.get("time", "")
        
        # Extract arrival info (from last leg for multi-leg flights)
        last_leg = flight_legs[-1]
        arr_airport = last_leg.get("arrival_airport", {})
        arr_name = arr_airport.get("name", "Unknown")
        arr_id = arr_airport.get("id", "")
        arr_time = arr_airport.get("time", "")
        
        # Build cleaned flight object
        cleaned_flight = {
            "airline": first_leg.get("airline", "Unknown"),
            "departure": f"{dep_name} ({dep_id}) on {dep_time}",
            "arrival": f"{arr_name} ({arr_id}) on {arr_time}",
            "duration": f"{flight_option.get('total_duration', 0)} minutes",
            "price": f"₹{flight_option.get('price', 0)}",
            "airline_logo": flight_option.get("airline_logo", "")
        }
        
        flights.append(cleaned_flight)
    
    return flights


def parse_hotel_response(raw_response: Dict) -> List[Dict]:
    """
    Parse raw SerpAPI hotel response and extract essential fields.
    Returns only top 5 hotels.
    
    Args:
        raw_response: Raw response from SerpAPI hotels search
        
    Returns:
        List of cleaned hotel dictionaries (max 5)
    """
    hotels = []
    
    # Get properties from response
    properties = raw_response.get("properties", [])
    
    # Limit to top 5
    top_properties = properties[:5]
    
    for hotel in top_properties:
        # Extract rate information
        rate_per_night = hotel.get("rate_per_night", {})
        rate_amount = rate_per_night.get("extracted_lowest")
        rate_display = rate_per_night.get("lowest", "Not Provided")
        
        total_rate = hotel.get("total_rate", {})
        total_amount = total_rate.get("extracted_lowest")
        total_display = total_rate.get("lowest", "Not Provided")
        
        # Extract hotel logo/image
        images = hotel.get("images", [])
        hotel_logo = images[0].get("thumbnail", "") if images else ""
        
        # Build cleaned hotel object
        cleaned_hotel = {
            "name": hotel.get("name", "Unknown Hotel"),
            "description": hotel.get("description", "No description available"),
            "rate_per_night": rate_display if rate_amount else "Not Provided",
            "total_rate_for_stay": total_display if total_amount else "Not Provided",
            "rating": hotel.get("overall_rating", "N/A"),
            "check_in_time": hotel.get("check_in_time", "Not specified"),
            "check_out_time": hotel.get("check_out_time", "Not specified"),
            "hotel_class": hotel.get("hotel_class", "Not specified"),
            "hotel_logo": hotel_logo
        }
        
        hotels.append(cleaned_hotel)
    
    return hotels
