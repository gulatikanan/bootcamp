import logging
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.storage.database import db
from src.api.endpoints import papers_router, figures_router, entities_router, jobs_router, export_router, admin_router

# Set up logging
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description="API for extracting and accessing figure captions from scientific publications",
        version="1.0.0",
        docs_url="/docs" if settings.api.enable_docs else None,
        redoc_url="/redoc" if settings.api.enable_docs else None
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    
    # Add error handling middleware
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    # Include routers
    app.include_router(papers_router, prefix="/api/v1")
    app.include_router(figures_router, prefix="/api/v1")
    app.include_router(entities_router, prefix="/api/v1")
    app.include_router(jobs_router, prefix="/api/v1")
    app.include_router(export_router, prefix="/api/v1")
    app.include_router(admin_router, prefix="/api/v1")
    
    # Add startup event to initialize database
    @app.on_event("startup")
    def startup():
        logger.info("Initializing database...")
        db.initialize()
    
    # Add health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}
    
    return app

def run_server():
    """Run the API server."""
    app = create_app()
    
    uvicorn.run(
        app,
        host=settings.api.host,
        port=settings.api.port,
        log_level=settings.log_level.lower(),
        workers=settings.api.workers
    )

if __name__ == "__main__":
    run_server()