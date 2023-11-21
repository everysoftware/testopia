import asyncio
import datetime

import numpy as np
import pandas as pd
from pandas import DatetimeIndex

from db.enums import TaskState
from src.config import cfg


def generate_tasks(
        state: TaskState | None = None,
        number: int = 500
) -> tuple[np.ndarray[DatetimeIndex], np.ndarray[TaskState]]:
    now = datetime.datetime.utcnow()
    updated_at = pd.date_range(
        start=now - datetime.timedelta(days=365),
        end=now,
        freq='D'
    )
    events = np.random.choice(updated_at, number)
    states = np.random.choice([state.name for state in TaskState], number) if state is None \
        else [state.name] * number

    print('Successfully generated!')

    return events, states


async def fill_db(
        user_id: int,
        checklist_id: int,
        state: TaskState | None = None,
        number: int = 500
) -> None:
    events, states = generate_tasks(state, number)

    user_id = [user_id] * len(events)
    df = pd.DataFrame({
        'checklist_id': checklist_id,
        'user_id': user_id,
        'name': 'Test task',
        'created_at': events,
        'updated_at': events,
        'state': states
    })
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    # Используем метод to_sql для загрузки DataFrame в базу данных
    df.to_sql('tasks', cfg.db.build_connection_str(False), if_exists='append', index=False)
    print('Successfully inserted!')


asyncio.run(fill_db(
    418849724,
    9,
    number=1000,
    state=TaskState.PASSED
))
