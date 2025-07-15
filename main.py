from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from router.recommend_routes import router
import uvicorn
app = FastAPI()

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173"   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Course Recommendation API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
