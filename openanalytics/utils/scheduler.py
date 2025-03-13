import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from openanalytics.utils.analytics import set_avg_views_per_visitor


async def scheduler_start():
    loop = asyncio.get_running_loop()
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        lambda: asyncio.run_coroutine_threadsafe(set_avg_views_per_visitor(), loop),
        IntervalTrigger(minutes=1),
        id="avg_views_per_visitor"
    )

    scheduler.start()
