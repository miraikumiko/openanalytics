from sqlalchemy import Table, Column, Integer, String, Boolean, Date, ForeignKey
from openanalytics.database import metadata

User = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("username", String, nullable=False, unique=True, index=True),
    Column("password", String, nullable=False),
    Column("token", String, unique=True, index=True),
    Column("is_admin", Boolean, nullable=False)
)

Site = Table(
    "sites",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("domain", String, nullable=False, unique=True, index=True),
    Column("token", String, nullable=False, unique=True, index=True),
    Column("visitors", Integer),
    Column("views", Integer)
)

Page = Table(
    "pages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("url", String, nullable=False, unique=True, index=True),
    Column("visitors", Integer),
    Column("views", Integer),
    Column("site_id", Integer, ForeignKey("sites.id"), nullable=False)
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
    Column("visited_at", Date, index=True),
    Column("site_id", Integer, ForeignKey("sites.id"), nullable=False)
)
