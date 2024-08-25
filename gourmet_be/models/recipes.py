import uuid
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator


class TextSize(StrEnum):
    EXTRA_SMALL = "xs"
    SMALL = "sm"
    MEDIUM = "md"
    LARGE = "lg"
    EXTRA_LARGE = "xl"


class BlockType(StrEnum):
    IMAGE = "image"
    TITLE = "title"
    SUBTITLE = "subtitle"
    TEXT = "text"
    LIST = "list"
    INDENTED_BLOCK = "indented_block"


class Block(BaseModel):
    type: BlockType

    class Config:
        orm_mode = True


class ImageBlock(Block):
    type: Literal[BlockType.IMAGE]
    url: str

    class Config:
        orm_mode = True


class TitleBlock(Block):
    type: Literal[BlockType.TITLE]
    size: TextSize = TextSize.LARGE
    bold: bool = False
    text: str

    class Config:
        orm_mode = True


class SubtitleBlock(Block):
    type: Literal[BlockType.SUBTITLE]
    size: TextSize = TextSize.MEDIUM
    bold: bool = False
    text: str

    class Config:
        orm_mode = True


class TextBlock(Block):
    type: Literal[BlockType.TEXT]
    size: TextSize = TextSize.MEDIUM
    bold: bool = False
    text: str

    class Config:
        orm_mode = True


class ListType(StrEnum):
    NUMBERED = "numbered"
    BULLETED = "bulleted"
    CHECKLIST = "checklist"


class IngredientListItem(BaseModel):
    text: str
    quantity: float | None = None
    unit: str | None = None
    note: str | None = None

    class Config:
        orm_mode = True


class ListBlock(Block):
    type: Literal[BlockType.LIST]
    list_type: ListType
    header: str | None = None
    items: list[str | IngredientListItem]

    class Config:
        orm_mode = True


class IndentedBlock(Block):
    type: Literal[BlockType.INDENTED_BLOCK]
    block: Block

    class Config:
        orm_mode = True


SupportedBlocks = Annotated[
    ImageBlock
    | TitleBlock
    | SubtitleBlock
    | TextBlock
    | ListBlock
    | IndentedBlock,
    Discriminator("type"),
]


class Recipe(BaseModel):
    id: uuid.UUID
    creator_id: uuid.UUID
    language: str
    title: str
    description: str
    image_url: str
    thumb_image_url: str
    steps: list[list[SupportedBlocks]]
    ingredients: list[IndentedBlock | ListBlock | TitleBlock]
    rating: float = 0
    likes: int = 0

    class Config:
        orm_mode = True
