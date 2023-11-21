from typing import Any, Sequence

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import Row, RowMapping, select

from src.db.models import Task
from src.bot.enums.task_state import TASK_STATE_TRANSLATIONS, TASK_STATE_COLORS
from src.bot.utils import DataVerifying
from src.db import Database


async def get_data(db: Database, user_id: int) -> Sequence[Row | RowMapping | Any]:
    async with db.session.begin():
        stmt = select(Task.state).where(Task.user_id == user_id)
        result = await db.session.execute(stmt)
        return result.scalars().all()


async def pie_plot(db: Database, user_id: int) -> str:
    data = await get_data(db, user_id)
    df = pd.DataFrame(data)
    lst = df.value_counts().index.tolist()
    class_names = [TASK_STATE_TRANSLATIONS[x[0]] for x in lst]
    class_values = df.value_counts().values

    colors = [TASK_STATE_COLORS[x[0]] for x in lst]

    plt.figure()
    my_circle = plt.Circle((0, 0), 0.8, color='white')

    # Create a pie chart of the filtered data
    plt.pie(class_values,
            labels=class_names,
            autopct="%.0f%%",
            colors=colors
            )

    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.title('Состояние прохождения тестов')

    pie_id = DataVerifying.get_hash(str(user_id), DataVerifying.generate_salt())
    plt.savefig(f'static/pie_{pie_id}.png')

    plt.close()

    return f'static/pie_{pie_id}.png'
