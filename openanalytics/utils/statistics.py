from collections import Counter
from openanalytics.database import database
from openanalytics.models import Site, Client


async def avg_views_per_visitor() -> float:
    avg_views = 0
    sites = await database.fetch_all(Site.select())

    for site in sites:
        clients = await database.fetch_all(Client.select().where(Client.c.id == site.id))

        ips = [client['ip'] for client in clients]
        ip_counts = Counter(ips)
        views = [count for _, count in ip_counts.items()]

        if sum(views) > 0:
            avg_views = round(sum(views) / len(views), 2)

    return avg_views
