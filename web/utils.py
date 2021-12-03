import os

import requests


def get_scrapyd_jobs_length():
    # This function returns a rough indication of how many searches are left, not necessarily how many jobs.
    # It isn't very accurate due to rounding to int
    scrapyd_url = os.getenv("SCRAPYD_URL")
    scrapyd_port = os.getenv("SCRAPYD_PORT")
    scrapyd_project = os.getenv("SCRAPYD_PROJECT")

    # Kind of gross but we dont care if we cant get this
    try:
        # Get number of spiders
        list_spiders = requests.get(
            f"http://{scrapyd_url}:{scrapyd_port}/listspiders.json?project={scrapyd_project}"
        )
        list_spiders.raise_for_status()
        number_of_spiders = len(list_spiders.json().get("spiders"))
        # Get number of jobs
        list_jobs = requests.get(
            f"http://{scrapyd_url}:{scrapyd_port}/listjobs.json?project={scrapyd_project}"
        )
        list_jobs.raise_for_status()
        pending_jobs = len(list_jobs.json().get("pending"))
        running_jobs = len(list_jobs.json().get("running"))
    except:  # noqa
        return "-"

    return int((pending_jobs + running_jobs) / number_of_spiders)
