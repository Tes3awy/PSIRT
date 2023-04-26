from datetime import date, timedelta

import requests
from flask import flash, redirect, render_template, request, session, url_for

from psiapp import limiter
from psiapp.utils import fetch_data, paginate

from . import bp
from .forms import DateRangeSearchForm


# By Date Range Search Form Page
@bp.route("/range/search", methods=["GET", "POST"])
@limiter.exempt
def dates_range(title="Search by date range"):
    form = DateRangeSearchForm()
    if form.validate_on_submit():
        date_sort = form.date_sort.data
        startDate = form.start_date.data
        endDate = form.end_date.data
        return redirect(
            url_for(
                "dates.results",
                date_sort=date_sort,
                startDate=startDate,
                endDate=endDate,
            )
        )
    return render_template(
        "dates/form.html", title=title, form=form, date=date, timedelta=timedelta
    )


# By Date Range Search Results Page
@bp.route("/all/<string:date_sort>", methods=["GET"])
def results(date_sort: str):
    pageIndex = request.args.get("pageIndex", 1, type=int)
    pageSize = request.args.get("pageSize", 10, type=int)
    startDate = request.args.get("startDate", None, type=str)
    endDate = request.args.get("endDate", None, type=str)
    title = f"Search results from {startDate} to {endDate} (by {date_sort})"
    uri = "{}?pageIndex={:n}&pageSize={:n}&startDate={}&endDate={}"
    try:
        res = fetch_data(
            uri=f"all/{uri.format(date_sort, pageIndex, pageSize, startDate, endDate)}&productNames=true",
            access_token=session.get("access_token"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", category="danger")
        return redirect(url_for(".dates_range"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session has expired! You are redirected here to refresh your session",
                category="info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code in [404, 406]:
            flash(
                f"{e.response.json().get('errorCode')} - {e.response.json().get('errorMessage')}",
                category="warning" if e.response.status_code == 404 else "danger",
            )
            return redirect(url_for(".dates_range"))
        if e.response.status_code == 503:
            flash(
                "Service is currently unavailable from Cisco! Please try again later",
                category="danger",
            )
            return redirect(url_for(".dates_range"))
        flash(str(e), category="danger")
        return redirect(url_for(".dates_range"))
    else:
        advisories = res.json().get("advisories")
        paging = paginate(
            paging=res.json().get("paging"),
            pageIndex=pageIndex,
            pageSize=pageSize,
        )
        total_count = paging.get("total_count")
        tnp = paging.get("tnp")  # total number of pages
        start = paging.get("start")
        end = paging.get("end")
        prev_url = f"{res.json().get('paging').get('prev')}&startDate={startDate}&endDate={endDate}"
        first_url = uri.format(date_sort, 1, pageSize, startDate, endDate)
        next_url = f"{res.json().get('paging').get('next')}&startDate={startDate}&endDate={endDate}"
        last_url = uri.format(date_sort, tnp, pageSize, startDate, endDate)
        pagination = res.json().get("paging")
        flash(f"Page {pageIndex} of {tnp} - {title}", "success")
        return render_template(
            "dates/results.html",
            title=title,
            advisories=advisories,
            pagination=pagination,
            prev_url=prev_url,
            next_url=next_url,
            first_url=first_url,
            last_url=last_url,
            total_count=total_count,
            start_date=startDate,
            end_date=endDate,
            tnp=tnp,
            start=start + 1,
            end=end,
        )
