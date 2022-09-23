from fastapi import FastAPI, APIRouter, Query, HTTPException

from typing import Optional

from app.schemas import Stylist, StylistSearchResults, StylistCreate
from app.stylist_data import STYLISTS


app = FastAPI(title="Hairball API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello World"}


@api_router.get("/stylist/{stylist_id}", status_code=200)
def fetch_stylist(*, stylist_id: int) -> dict:  # 3
    """
    Fetch a single stylist by ID
    """
    result = [stylist for stylist in STYLISTS if stylist["id"] == stylist_id]
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Stylist with ID {stylist_id} not found"
        )
    return result[0]


@api_router.get("/search/", status_code=200, response_model=StylistSearchResults)
def search_stylists(keyword: Optional[str] = Query(None, min_length=3, example="Karen"), max_results: Optional[int] = 10) -> dict:
    """
    Search for stylists based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": STYLISTS[:max_results]}

    results = filter(lambda stylist: keyword.lower() in stylist["name"].lower(), STYLISTS)
    return {"results": list(results)[:max_results]}


@api_router.post("/stylist/", status_code=201, response_model=Stylist)
def create_stylist(*, stylist_in: StylistCreate) -> dict:
    """
    Create a new recipe (in memory only)
    """
    new_entry_id = len(STYLISTS) + 1
    stylist_entry = Stylist(
        id=new_entry_id,
        name=stylist_in.name,
        experience_years=stylist_in.experience_years,
        favourite_haircut=stylist_in.favourite_haircut,
    )
    STYLISTS.append(stylist_entry.dict())  # 3
    return stylist_entry


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
