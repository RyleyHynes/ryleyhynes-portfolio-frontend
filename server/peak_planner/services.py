from .models import Route, TripPlan

def estimate_time_hours(route: Route, pace_up_m_per_hr=350, pace_flat_km_per_hr=4.5):
    """_summary_

    Args:
        route (Route): _description_
        pace_up_m_per_hr (int, optional): _description_. Defaults to 350.
        pace_flat_km_per_hr (float, optional): _description_. Defaults to 4.5.

    Returns:
        _type_: _description_
    """
    return (route.vert_gain_m or 0)/pace_up_m_per_hr + (route.distance_km or 0)/pace_flat_km_per_hr

def score_weather_window(lat, lon, start_date, end_date):
    """_summary_

    Args:
        lat (_type_): _description_
        lon (_type_): _description_
        start_date (_type_): _description_
        end_date (_type_): _description_

    Returns:
        _type_: _description_
    """
    # stub: plug in real API later (Open-Meteo, etc.). Return 0–100 “go/no-go”.
    return 72