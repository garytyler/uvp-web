from slugify import slugify  # type: ignore

from app.models.features import Feature


async def feature_with_slug_exists(slug: str) -> bool:
    return bool(await Feature.get_or_none(slug=slug))


async def generate_unique_feature_slug(title: str) -> str:
    slugified_title = slugify(title, max_length=50, word_boundary=True)
    if not await feature_with_slug_exists(slugified_title):
        return slugified_title
    for index in range(99):
        numbered_slugified_title = f"{slugified_title[:47]}-{index}"
        if not await feature_with_slug_exists(numbered_slugified_title):
            return numbered_slugified_title
    raise ValueError("Error generating slug")
