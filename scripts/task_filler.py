import asyncio
import datetime
import logging
from typing import Sequence

import numpy as np
import pandas as pd

from app.db.dependencies import UOWDep
from app.db.types import ID
from app.di import inject
from app.tasks.schemas import TaskStatus


def generate_timestamps(
        number: int
) -> Sequence[datetime.datetime]:
    now = datetime.datetime.now()
    timestamps = np.random.choice(pd.date_range(
        start=now - datetime.timedelta(days=365), end=now, freq="D"
    ), number)
    logging.info("Generated %d timestamps", number)
    return timestamps


def generate_statuses(
        number: int
) -> Sequence[TaskStatus]:
    statuses = np.random.choice(
        list(TaskStatus), number
    )
    logging.info("Generated %d statuses", number)
    return statuses


def get_df(user_id: ID, checklist_id: int, number: int) -> pd.DataFrame:
    timestamps = generate_timestamps(number)
    statuses = generate_statuses(number)
    df = pd.DataFrame(
        {
            "checklist_id": checklist_id,
            "user_id": user_id,
            "name": "Test task",
            "created_at": timestamps,
            "updated_at": timestamps,
            "status": statuses,
        }
    )
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])
    return df


@inject
async def fill_tasks_table(
        user_id: ID, checklist_id: int, number: int, uow: UOWDep
) -> None:
    df = get_df(user_id, checklist_id, number)
    conn = await uow.session.connection()
    await conn.run_sync(
        lambda sync_conn: df.to_sql(
            "tasks",
            con=sync_conn,
            if_exists="append",
            index=False
        ),
    )
    logging.info("Filled tasks table with %d tasks", number)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    user_id = int(input("Enter user ID: "))
    checklist_id = int(input("Enter checklist ID: "))
    number = int(input("Enter number of tasks: "))
    await fill_tasks_table(user_id, checklist_id, number)  # type: ignore[call-arg]
    print("Done!")


if __name__ == '__main__':
    asyncio.run(main())
