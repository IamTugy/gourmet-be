from pathlib import Path

from gourmet_be.models.recipes import Recipe


def fetch_recipe(id: int) -> Recipe | None:
    path = Path(__file__).parent / f"recipe_{id}.json"
    if not path.exists():
        return None
    with path.open() as f:
        return Recipe.model_validate_json(f.read())
