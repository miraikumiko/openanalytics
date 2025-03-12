from sqlalchemy import Table, Column, Integer, String, ForeignKey
from openanalytics.database import metadata

Site = Table(
    "sites",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("domain", String, nullable=False, unique=True, index=True),
    Column("token", String, nullable=False, unique=True, index=True),
    Column("unique_visitors", Integer),
    Column("total_views", Integer)
)

Client = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("ip", String, index=True),
    Column("country", String, index=True),
    Column("os", String, index=True),
    Column("browser", String, index=True),
    Column("referrer", String, index=True),
    Column("page_url", String, index=True),
    Column("site_id", Integer, ForeignKey("sites.id"), nullable=False)
)