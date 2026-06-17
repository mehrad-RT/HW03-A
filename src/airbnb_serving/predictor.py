import pandas as pd

from airbnb_serving.schema import ListingFeatures, PredictionResponse


FEATURE_COLS = [
    "instant_bookable",
    "accommodates",
    "bathrooms",
    "bedrooms",
    "beds",
    "listing_price",
    "minimum_nights",
    "maximum_nights",
    "is_superhost",
    "host_listing_count",
    "neighbourhood_name",
    "total_reviews_before_cutoff",
    "unique_reviewers_before_cutoff",
    "avg_comment_len_before_cutoff",
    "max_comment_len_before_cutoff",
    "days_since_last_review",
    "available_days_last_90d",
    "available_rate_last_90d",
    "avg_minimum_nights_calendar_last_90d",
    "avg_maximum_nights_calendar_last_90d",
    "available_days_last_30d",
    "available_rate_last_30d",
    "avg_minimum_nights_calendar_last_30d",
    "avg_maximum_nights_calendar_last_30d",
]


def _probability_for_high_demand(probabilities) -> float:
    if probabilities.ndim == 1:
        return float(probabilities[0].item())
    if probabilities.shape[1] == 1:
        return float(probabilities[0, 0].item())
    return float(probabilities[0, 1].item())


def predict_single(features: ListingFeatures, model, run_id: str) -> PredictionResponse:
    row = features.model_dump()
    df = pd.DataFrame([[row[col] for col in FEATURE_COLS]], columns=FEATURE_COLS)

    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)

    return PredictionResponse(
        prediction=int(prediction.item() if hasattr(prediction, "item") else prediction),
        probability_high_demand=_probability_for_high_demand(probabilities),
        model_run_id=run_id,
    )


def predict_batch(
    features_list: list[ListingFeatures], model, run_id: str
) -> list[PredictionResponse]:
    rows = [features.model_dump() for features in features_list]
    df = pd.DataFrame(rows, columns=FEATURE_COLS)

    predictions = model.predict(df)
    probabilities = model.predict_proba(df)

    responses: list[PredictionResponse] = []
    for prediction, probability_row in zip(predictions, probabilities):
        probability = probability_row[1] if len(probability_row) > 1 else probability_row[0]
        responses.append(
            PredictionResponse(
                prediction=int(prediction.item() if hasattr(prediction, "item") else prediction),
                probability_high_demand=float(
                    probability.item() if hasattr(probability, "item") else probability
                ),
                model_run_id=run_id,
            )
        )
    return responses
