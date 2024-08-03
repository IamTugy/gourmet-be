import uuid

from fastapi import APIRouter, Response
from pydantic import TypeAdapter
from gourmet_be.models.recipes import Recipe, IngredientListItem, ListBlock, TextBlock, TitleBlock
from gourmet_be.static_data.fetcher import fetch_recipe


router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Recipe])
async def read_recipes():
    recipes = [
        fetch_recipe("ef8612a0-9121-4c03-9ebd-01cbbb76222b"),
        fetch_recipe("cc11f617-8265-4f5e-a7cb-dfa443b7d210"),
    ]
    return Response(
        content=TypeAdapter(list[Recipe]).dump_json(recipes),
        media_type="application/json",
    )


@router.get("/{recipe_id}", response_model=Recipe)
async def read_recipe(recipe_id: uuid.UUID):
    recipe = fetch_recipe(recipe_id)
    if recipe is None:
        return Response(status_code=404)
    return Response(
        content=TypeAdapter(Recipe).dump_json(recipe),
        media_type="application/json",
    )
