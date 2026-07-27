import uvicorn
import os

if __name__ == "__main__":
    # Railway provides PORT at runtime; 8080 remains the local and platform default.
    # Reload is opt-in so the production process starts exactly once.
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )
