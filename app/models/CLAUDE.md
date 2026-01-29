# SQLAlchemy Models

## Conventions
- All models inherit from `Base` (from app/db.py)
- Use `__tablename__` for explicit table names
- Primary keys: `id = Column(Integer, primary_key=True, index=True)`
- Timestamps: Use `TIMESTAMP(timezone=True)` with `server_default=func.now()`
- JSON fields: Use `JSONB` type for PostgreSQL
- Foreign keys: Always add index on FK columns

## Patterns
- Keep models simple - business logic goes in DAOs
- Use relationships sparingly; prefer explicit joins in DAOs
- Import all models in __init__.py for Alembic autodiscovery
