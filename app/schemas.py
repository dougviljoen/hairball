from pydantic import BaseModel

from typing import Sequence


class Stylist(BaseModel):
    id: int
    name: str
    experience_years: int
    favourite_haircut: str


class StylistSearchResults(BaseModel):
    results: Sequence[Stylist]


class StylistCreate(BaseModel):
    name: str
    experience_years: int
    favourite_haircut: str
    submitter_id: int
