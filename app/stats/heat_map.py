import datetime
import uuid

import pandas as pd
from matplotlib import pyplot as plt

from app.stats.calmap import yearplot


def paint_heat_map(stats: dict[datetime.datetime, int], *, title: str = "Total done: {count}") -> str:
    data = pd.Series(stats)
    data = data.astype("int64")
    data.index = pd.to_datetime(data.index)

    plt.figure(figsize=(7, 3))
    yearplot(data, monthlabels=["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
             daylabels=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])

    plt.title(title.format(count=data.sum()))
    save_path = f"heatmap_{uuid.uuid4().hex}.png"
    plt.savefig(save_path)
    plt.close()

    return save_path
