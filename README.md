# pulmorad_fastapi_v3

### Database migration
###### Initialize alembic
`alembic init alembic`
###### Create first migration
`alembic revision --autogenerate -m "first migration"`
###### Apply migration to the database
`alembic upgrade head`
