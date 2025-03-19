from collections import Counter
from urllib.parse import urlparse
from openanalytics.database import database
from openanalytics.models import Client


async def get_total_site_views(clients) -> int:
    total_site_views = len(clients)

    return total_site_views


async def get_unique_visitors(clients) -> int:
    ips = [client["ip"] for client in clients]
    ip_counts = Counter(ips)
    visitors = [ip for ip, _ in ip_counts.items()]
    unique_visitors = len(visitors)

    return unique_visitors


async def get_views_per_visitor(clients) -> float:
    ips = [client["ip"] for client in clients]
    ip_counts = Counter(ips)
    views = [count for _, count in ip_counts.items()]

    if sum(views) > 0:
        views_per_visitor = round(sum(views) / len(views), 2)
    else:
        views_per_visitor = 0

    return views_per_visitor


async def get_sources(clients) -> dict:
    referrers = [client["referrer"] for client in clients]
    referrer_counts = Counter(referrers)
    sources = {urlparse(referrer).netloc: count for referrer, count in referrer_counts.items()}

    return sources


async def get_pages(clients) -> dict:
    page_urls = [client["page_url"] for client in clients]
    page_url_counts = Counter(page_urls)
    pages = dict(page_url_counts.items())

    return pages


async def get_locations(clients) -> dict:
    countries = [client["country"] for client in clients]
    country_counts = Counter(countries)
    locations = dict(country_counts.items())

    return locations


async def get_devices(clients) -> dict:
    browser = [client["browser"] for client in clients]
    browser_counts = Counter(browser)
    browsers = dict(browser_counts.items())
    os = [client["os"] for client in clients]
    os_counts = Counter(os)
    operating_systems = dict(os_counts.items())

    return {"browsers": browsers, "operating_systems": operating_systems}


async def get_stats(site_id: int) -> dict:
    clients = await database.fetch_all(Client.select().where(Client.c.site_id == site_id))

    total_site_views = await get_total_site_views(clients)
    unique_visitors = await get_unique_visitors(clients)
    views_per_visitor = await get_views_per_visitor(clients)
    sources = await get_sources(clients)
    pages = await get_pages(clients)
    locations = await get_locations(clients)
    devices = await get_devices(clients)

    data = {
        "total_site_views": total_site_views,
        "unique_visitors": unique_visitors,
        "views_per_visitor": views_per_visitor,
        "sources": sources,
        "pages": pages,
        "locations": locations,
        "devices": devices
    }

    return data
