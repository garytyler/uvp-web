from typing import Dict

from app.services.features import feature_with_slug_exists, generate_unique_feature_slug


async def validate_feature_slug(body: Dict[str, str]) -> Dict[str, str]:

    slug_in = body.get("slug", "").strip()
    if not slug_in:
        body["slug"] = await generate_unique_feature_slug(title=body["title"])
    elif await feature_with_slug_exists(slug_in):
        raise ValueError(f"Feature with slug '{slug_in}' already exists")
    return body
