from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import supabase

app = FastAPI()


# Pydantic model for request validation
class UserStatsCreate(BaseModel):
    user_id: int
    reviews_done: int


@app.get("/reviews/{user_id}")
def get_reviews(user_id: int):
    """Fetch all rows from the 'reviews_done' table in Supabase for a user"""
    response = supabase.table("user_stats").select("*").eq("user_id", user_id).execute()
    return {"data": response.data}


@app.post("/post-reviews")
def post_reviews(payload: UserStatsCreate):
    try:
        response = (
            supabase.table("user_stats")
            .insert(payload.model_dump(mode="json"))
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=400, detail="Failed to insert into Supabase"
            )

        return {"message": "Review stats saved successfully", "data": response.data[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
