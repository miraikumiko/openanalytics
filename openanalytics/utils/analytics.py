from sqlalchemy.sql import select, func
from openanalytics.database import database
from openanalytics.models import Site, Stat, Client


async def set_avg_views_per_visitor():
    sites = await database.fetch_all(Site.select())

    for site in sites:
        result = await database.fetch_all(
            select(Client.c.ip, func.count(Client.c.id).label("count_per_ip"))
            .where(Client.c.site_id == site.id)
            .group_by(Client.c.ip)
        )
        views = [row.count_per_ip for row in result]
        avg_views_per_visitor = round(sum(views) / len(views), 2)

        stat = await database.fetch_one(Stat.select().where(Stat.c.site_id == site.id))

        if stat:
            await database.execute(
                Stat.update().where(Stat.c.site_id == site.id).values(
                    avg_views_per_visitor=avg_views_per_visitor
                )
            )
        else:
            await database.execute(
                Stat.insert().values(
                    avg_views_per_visitor=avg_views_per_visitor,
                    site_id=site.id
                )
            )
