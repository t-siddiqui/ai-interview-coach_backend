from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import interview, auth, pdf

app = FastAPI()

# ✅ FIXED CORS (allow both)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins, including Vercel frontend
    allow_credentials=False, # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pdf.router, prefix="/api", tags=["PDF"])
app.include_router(interview.router, prefix="/api", tags=["Interview"])

@app.get("/")
def home():
    return {"message": "AI Interview Coach Running"}