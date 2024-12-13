import asyncio
import datetime
import logging
import random
from typing import Sequence

import numpy as np
import pandas as pd

from app.base.types import UUID
from app.db.dependencies import UOWDep
from app.di import inject
from app.tasks.schemas import TaskStatus, TestStatus


def generate_timestamps(number: int) -> Sequence[datetime.datetime]:
    now = datetime.datetime.now(datetime.UTC)
    timestamps = np.random.choice(
        pd.date_range(
            start=now - datetime.timedelta(days=365 - 30), end=now, freq="D"
        ),
        number,
    )
    logging.info("Generated %d timestamps", number)
    return timestamps


def get_test_status(passed_p: float) -> TestStatus:
    if random.random() < passed_p:
        return TestStatus.passed
    return random.choice([s for s in TestStatus if s != TestStatus.passed])


def generate_statuses(
    number: int, *, done_p: float, test_p: float, passed_p: float
) -> tuple[Sequence[TaskStatus], Sequence[TestStatus]]:
    statuses = [TaskStatus.to_do for _ in range(number)]
    test_statuses = [TestStatus.no_status for _ in range(number)]

    done_count = int(number * done_p)
    done_indices = random.sample(range(number), done_count)

    for i in done_indices:
        statuses[i] = TaskStatus.done
        if random.random() < test_p:
            test_statuses[i] = get_test_status(passed_p)
    logging.info("Generated %d statuses (%d done)", number, done_count)
    return statuses, test_statuses


def get_df(user_id: UUID, checklist_id: int, number: int) -> pd.DataFrame:
    timestamps = generate_timestamps(number)
    statuses, test_statuses = generate_statuses(
        number, done_p=0.9, test_p=0.8, passed_p=0.6
    )
    df = pd.DataFrame(
        {
            "checklist_id": checklist_id,
            "user_id": user_id,
            "name": "Test task",
            "created_at": timestamps,
            "updated_at": timestamps,
            "status": statuses,
            "test_status": test_statuses,
        }
    )
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])
    return df


@inject
async def fill_tasks_table(
    user_id: UUID, checklist_id: int, number: int, uow: UOWDep
) -> None:
    df = get_df(user_id, checklist_id, number)
    conn = await uow.session.connection()
    await conn.run_sync(
        lambda sync_conn: df.to_sql(
            "tasks", con=sync_conn, if_exists="append", index=False
        ),
    )
    logging.info("Filled tasks table with %d tasks", number)


def get_valid_integer(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    user_id = get_valid_integer("Enter user ID: ")
    checklist_id = get_valid_integer("Enter checklist ID: ")
    number = get_valid_integer("Enter number of tasks: ")
    await fill_tasks_table(user_id, checklist_id, number)  # type: ignore[call-arg]
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
