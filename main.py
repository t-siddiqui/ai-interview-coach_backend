from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import interview, auth, pdf

app = FastAPI()

# ✅ FIXED CORS (allow both)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pdf.router, prefix="/api", tags=["PDF"])
app.include_router(interview.router, prefix="/api", tags=["Interview"])

@app.get("/")
def home():
    return {"message": "AI Interview Coach Running"}