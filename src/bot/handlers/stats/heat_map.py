import datetime
from typing import Any, Sequence

import calmap
import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import select, func, Row

from src.bot.utils import DataVerifying
from src.db import Database
from src.db.enums import TaskState
from src.db.models import Task


async def get_data(db: Database, user_id: int) -> Sequence[Row[tuple[Any, Any]]]:
    # Получаем дату года назад от текущей даты
    now = datetime.datetime.utcnow()
    year_ago = now - datetime.timedelta(days=365)

    async with db.session.begin():
        # Запрос на получение количества выполненных задач по дням за последний год
        stmt = (
            select(
                func.count(Task.id),  # Считаем количество задач
                func.date(Task.updated_at)
            )
            .where(
                Task.user_id == user_id,  # Фильтруем по ID пользователя
                Task.state == TaskState.PASSED,  # Фильтруем по состоянию задачи
                Task.updated_at >= year_ago  # Фильтруем задачи, обновленные за последний год
            )
            .group_by(func.date(Task.updated_at))  # Группируем по дню обновления
        )
        result = await db.session.execute(stmt)
        # Получаем результаты
        task_counts = result.all()

    return task_counts


async def heat_map(db: Database, user_id: int) -> str:
    task_counts = await get_data(db, user_id)

    if task_counts:
        commits = pd.Series({date: count for count, date in task_counts})
        # Добавляем минимальное значение.
        commits = commits.add(pd.Series({
            datetime.date(2004, 2, 18): 0
        }), fill_value=0)
        commits = commits.astype('int64')
        commits.index = pd.to_datetime(commits.index)

        # Увеличиваем размер фигуры
        plt.figure(figsize=(7, 3))

        # Рисуем тепловую карту
        calmap.yearplot(
            commits,
            cmap='Greens',
            year=datetime.datetime.utcnow().year,
            monthlabels=['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
            daylabels=['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Cб', 'Вс'],
            dayticks=[1, 3, 5]
        )

        plt.title(f'{commits.sum()} пройденных тестов за последний год')

    # Сохраняем карту
    heat_map_id = DataVerifying.get_hash(str(user_id), DataVerifying.generate_salt())
    path = f'static/pie_{heat_map_id}.png'
    plt.savefig(path)

    # Очищаем фигуру
    plt.close()

    return path
