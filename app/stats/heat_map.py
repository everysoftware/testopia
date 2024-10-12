import datetime
import uuid

import pandas as pd
from matplotlib import pyplot as plt

from app.stats.calmap import yearplot


def paint_heat_map(
    stats: dict[datetime.datetime, int], *, title: str = "Total done: {count}"
) -> str:
    data = pd.Series(stats)
    data.index = pd.to_datetime(data.index)
    plt.figure(figsize=(7, 3))
    yearplot(
        data,
        months={
            1: "Янв",
            2: "Фев",
            3: "Мар",
            4: "Апр",
            5: "Май",
            6: "Июн",
            7: "Июл",
            8: "Авг",
            9: "Сен",
            10: "Окт",
            11: "Ноя",
            12: "Дек",
        },
        days={1: "Пн", 3: "Ср", 5: "Пт"},
    )
    plt.title(title.format(count=data.sum()))
    save_path = f"heatmap_{uuid.uuid4().hex}.png"
    plt.savefig(save_path)
    plt.close()

    return save_path
