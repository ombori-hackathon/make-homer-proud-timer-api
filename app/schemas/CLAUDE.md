# Pydantic Schemas

## Conventions
- Use Pydantic v2 style with `model_config = ConfigDict(from_attributes=True)`
- Base schema for shared fields
- Create schema for POST request body
- Response schema includes `id` and timestamps
- Use `list[Schema]` for collections (not `List[Schema]`)

## Naming Pattern
- `GodBase` - shared fields
- `GodCreate` - for POST body
- `God` - full response with id
- `GodUpdate` - for PATCH body (all fields Optional)
