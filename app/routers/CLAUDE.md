# API Routers

## Conventions
- One router file per resource (gods.py, sessions.py, etc.)
- Use `APIRouter(prefix="/resource", tags=["resource"])`
- Register in main.py: `app.include_router(router)`
- Always specify `response_model` on endpoints
- Use dependency injection for database: `Depends(get_db)`

## HTTP Methods
- GET for retrieval (list, detail)
- POST for creation
- PATCH for partial updates
- DELETE for removal

## DAO Usage
- Instantiate DAOs inside endpoint functions
- Pass the injected db session to DAO constructor
