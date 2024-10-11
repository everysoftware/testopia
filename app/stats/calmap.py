import calendar
import datetime
from typing import Sequence, Any, Literal, assert_never

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap, ColorConverter
from matplotlib.patches import Polygon
from pandas import Series


def get_ticks(ticks: bool | Sequence[int] | int, labels: Sequence[str]) -> Sequence[int]:
    if ticks is True:
        return range(len(labels))
    elif ticks is False:
        return range(0)
    elif isinstance(ticks, int):
        return range(0, len(labels), ticks)
    return ticks


def get_polygon(x0: float, x1: float) -> Polygon:
    p = [
        (x0, 0),
        (x0, 7),
        (x1 + 1, 7),
        (x1 + 1, 0),
        (x0, 0),
    ]
    return Polygon(
        p,
        edgecolor="black",
        facecolor="None",
        linewidth=1,
        zorder=20,
        clip_on=False,
    )


def set_ticks(ax: Axes, xticks: dict[str, float], yticks: dict[str, float]) -> Axes:
    ax.set_xlabel("")
    ax.set_xticks(list(xticks.values()))
    ax.set_xticklabels(xticks.keys())
    ax.set_ylabel("")

    ax.yaxis.set_ticks_position("right")
    ax.set_yticks([6 - i + 0.5 for i in yticks.values()])
    ax.set_yticklabels(
        yticks.keys(), rotation="horizontal", va="center"
    )
    return ax


def _yearplot(
        by_day: pd.DataFrame,
        vmin: float,
        vmax: float,
        cmap: str,
        fillcolor: str,
        daylabels: Sequence[str],
        dayticks: Sequence[int],
        monthlabels: Sequence[str],
        monthticks: Sequence[int],
        monthly_border: bool,
        ax: Axes,
        **kwargs: Any
) -> Axes:
    plot_data = by_day.pivot(index="day", columns="week", values="data").values[::-1]
    fill_data = by_day.pivot(index="day", columns="week", values="fill").values[::-1]

    plot_data = np.ma.masked_where(np.isnan(plot_data), plot_data)
    fill_data = np.ma.masked_where(np.isnan(fill_data), fill_data)

    ax.pcolormesh(fill_data, vmin=0, vmax=1, cmap=ListedColormap([fillcolor]))
    ax.pcolormesh(plot_data, vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)

    ax.set(xlim=(0, plot_data.shape[1]), ylim=(0, plot_data.shape[0]))
    ax.set_aspect("equal")

    # Remove spines & tick marks
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.xaxis.set_tick_params(which="both", length=0)
    ax.yaxis.set_tick_params(which="both", length=0)

    xticks = {}
    months_reverse_order = [(by_day.index.max().month - i - 1) % 12 + 1 for i in range(12)]
    for i, month in enumerate(months_reverse_order):
        first = datetime.datetime(by_day.index.max().year, month, 1)
        last = first + relativedelta(months=1, days=-1)
        x0 = (int(first.strftime("%j")) - 1) // 7
        x1 = (int(last.strftime("%j")) - 1) // 7
        xticks[monthlabels[month - 1]] = x0 + (x1 - x0 + 1) / 2
        if monthly_border:
            ax.add_artist(get_polygon(x0, x1))

    return set_ticks(ax, xticks, {day: i for i, day in enumerate(daylabels)})


def yearplot(
        data: Series,
        *,
        year: int | None = None,
        how: str | None = "sum",
        vmin: float | None = 0,
        vmax: float | None = None,
        cmap: str = "Greens",
        fillcolor: str = "whitesmoke",
        linewidth: float = 1,
        linecolor: str | None = None,
        daylabels: Sequence[str] = calendar.day_abbr[:],
        dayticks: bool | list[int] | int = True,
        monthlabels: Sequence[str] = calendar.month_abbr[1:],
        monthticks: bool | list[int] | int = True,
        monthly_border: bool = False,
        mode: Literal["year", "last365"] = "last365",
        ax: Axes | None = None,
        **kwargs: Any
) -> Axes:
    """
    Plot one year from a timeseries as a calendar heatmap.

    Parameters
    ----------
    data : Series
        Data for the plot. Must be indexed by a DatetimeIndex.
    year : integer
        Only data indexed by this year will be plotted. If None, the first
        year for which there is data will be plotted.
    how : string
        Method for resampling data by day. If None, assume data is already
        sampled by day and don't resample. Otherwise, this is passed to Pandas
        pandas.agg (pandas >= 0.18).
    vmin : float
        Min Values to anchor the colormap. If None, min and max are used after
        resampling data by day.
    vmax : float
        Max Values to anchor the colormap. If None, min and max are used after
        resampling data by day.
    cmap : matplotlib colormap name or object
        The mapping from data values to color space.
    fillcolor : matplotlib color
        Color to use for days without data.
    linewidth : float
        Width of the lines that will divide each day.
    linecolor : color
        Color of the lines that will divide each day. If None, the axes
        background color is used, or 'white' if it is transparent.
    daylabels : list
        Strings to use as labels for days, must be of length 7.
    dayticks : list or int or bool
        If True, label all days. If False, don't label days. If a list,
        only label days with these indices. If an integer, label every n day.
    monthlabels : list
        Strings to use as labels for months, must be of length 12.
    monthticks : list or int or bool
        If True, label all months. If False, don't label months. If a
        list, only label months with these indices. If an integer, label every
        n month.
    monthly_border : bool
        Draw black border for each month. Default: False.
    mode: "year" | "last365"
        If "year", plot the year specified by the year parameter. If
        "last365", plot the last 365 days from the last date in the data.
    ax : matplotlib Axes
        Axes in which to draw the plot, otherwise use the currently-active
        Axes.
    kwargs : other keyword arguments
        All other keyword arguments are passed to matplotlib ax.pcolormesh.

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the calendar heatmap.

    Examples
    --------

    By default, yearplot plots the first year and sums the values per day:

    .. plot::
        :context: close-figs

        calmap.yearplot(events)

    We can choose which year is plotted with the year keyword argment:

    .. plot::
        :context: close-figs

        calmap.yearplot(events, year=2015)

    The appearance can be changed by using another colormap. Here we also use
    a darker fill color for days without data and remove the lines:

    .. plot::
        :context: close-figs

        calmap.yearplot(events, cmap='YlGn', fillcolor='grey',
                        linewidth=0)

    The axis tick labels can look a bit crowded. We can ask to draw only every
    nth label, or explicitely supply the label indices. The labels themselves
    can also be customized:

    .. plot::
        :context: close-figs

        calmap.yearplot(events, monthticks=3, daylabels='MTWTFSS',
                        dayticks=[0, 2, 4, 6])

    """  # noqa: E501
    if year is None:
        year = data.index.sort_values()[-1].year
    if how is None:
        by_day = data
    else:
        # Sample by day.
        by_day = data.groupby(level=0).agg(how).squeeze()
    if vmin is None:
        vmin = by_day.min()
    if vmax is None:
        vmax = by_day.max()
    if ax is None:
        ax = plt.gca()
    if linecolor is None:
        linecolor = ax.get_facecolor()
        if ColorConverter().to_rgba(linecolor)[-1] == 0:
            linecolor = "white"
    kwargs["linewidth"] = linewidth
    kwargs["edgecolors"] = linecolor
    match mode:
        case "year":
            by_day = by_day[str(year)]
            by_day = by_day.reindex(
                pd.date_range(start=str(year), end=str(year + 1), freq="D")[:-1]
            )
        case "last365":
            end_date = data.index.max()
            start_date = end_date - pd.DateOffset(days=365)
            by_day = by_day.reindex(
                pd.date_range(start=start_date, end=end_date, freq="D")
            )
        case _:
            assert_never(mode)
    by_day = pd.DataFrame(
        {
            "data": by_day,
            "fill": 1,
            "day": by_day.index.dayofweek,
            "week": by_day.index.isocalendar().week,
        }
    )
    # There may be some days assigned to previous year's last week or
    # next year's first week. We create new week numbers for them so
    # the ordering stays intact and week/day pairs unique.
    by_day.loc[(by_day.index.month == 1) & (by_day.week > 50), "week"] = 0
    by_day.loc[(by_day.index.month == 12) & (by_day.week < 10), "week"] = (
            by_day.week.max() + 1
    )
    by_day = by_day.drop_duplicates(subset=["day", "week"])
    return _yearplot(
        by_day,
        vmin,
        vmax,
        cmap,
        fillcolor,
        daylabels,
        dayticks,
        monthlabels,
        monthticks,
        monthly_border,
        ax,
        **kwargs
    )
