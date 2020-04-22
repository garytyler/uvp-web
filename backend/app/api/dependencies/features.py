from app.schemas.features import FeatureCreate
from app.utils.features import feature_with_slug_exists, generate_unique_feature_slug


async def validate_feature_slug(feature_in: FeatureCreate) -> FeatureCreate:
    if not feature_in.slug or not feature_in.slug.strip():
        feature_in.slug = await generate_unique_feature_slug(title=feature_in.title)
    elif await feature_with_slug_exists(feature_in.slug):
        raise ValueError(f"Feature with slug '{feature_in.slug}' already exists")
    return feature_in
