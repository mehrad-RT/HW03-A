from typing import Optional

from pydantic import BaseModel


class ListingFeatures(BaseModel):
    instant_bookable: bool
    accommodates: int
    bathrooms: Optional[float] = None
    bedrooms: Optional[float] = None
    beds: Optional[float] = None
    listing_price: Optional[float] = None
    minimum_nights: int
    maximum_nights: int
    is_superhost: bool
    host_listing_count: int
    neighbourhood_name: str
    total_reviews_before_cutoff: Optional[float] = None
    unique_reviewers_before_cutoff: Optional[float] = None
    avg_comment_len_before_cutoff: Optional[float] = None
    max_comment_len_before_cutoff: Optional[float] = None
    days_since_last_review: Optional[float] = None
    available_days_last_90d: int
    available_rate_last_90d: Optional[float] = None
    avg_minimum_nights_calendar_last_90d: Optional[float] = None
    avg_maximum_nights_calendar_last_90d: Optional[float] = None
    available_days_last_30d: int
    available_rate_last_30d: Optional[float] = None
    avg_minimum_nights_calendar_last_30d: Optional[float] = None
    avg_maximum_nights_calendar_last_30d: Optional[float] = None


class PredictionResponse(BaseModel):
    listing_id: Optional[int] = None
    prediction: int
    probability_high_demand: float
    model_run_id: str
