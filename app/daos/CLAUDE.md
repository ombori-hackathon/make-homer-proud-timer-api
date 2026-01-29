# Data Access Objects (DAOs)

## Pattern
- Each model has a corresponding DAO class
- DAOs inherit from BaseDAO for common CRUD operations
- DAOs receive `db: Session` in constructor
- All database queries go through DAOs, not in routers

## BaseDAO Methods
- `get(id)` - Get by primary key
- `get_all()` - Get all records
- `create(obj_in: dict)` - Create new record
- `update(id, obj_in: dict)` - Update existing
- `delete(id)` - Delete record

## Usage Example
```python
from app.daos.god_dao import GodDAO
god_dao = GodDAO(db)
gods = god_dao.get_all()
```
