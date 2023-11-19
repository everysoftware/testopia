import matplotlib.pyplot as plt
import pandas as pd
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from sqlalchemy import text

from src.bot.encryption import Verifying
from src.bot.keyboards.tasks import TASK_STATES_TRANSLATIONS
from src.db import Database

router = Router()


async def pie_plot(db: Database, user_id: int) -> str:
    async with db.session.begin():
        result = await db.session.execute(text(
            f'SELECT state FROM tasks WHERE user_id = {user_id}'
        ))
        df = pd.DataFrame(result.scalars().all())

    lst = df.value_counts().index.tolist()
    class_names = [TASK_STATES_TRANSLATIONS[x[0]] for x in lst]
    class_values = df.value_counts().values

    colors = {
        'PASSED': 'lightseagreen',
        'IMPOSSIBLE': 'gold',
        'FAILED': 'lightcoral',
        'SKIPPED': 'turquoise'
    }

    colors = [colors[x[0]] for x in lst]

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

    hsh = Verifying.get_hash(str(user_id), Verifying.generate_salt())
    plt.savefig(f'static/pie_{hsh}.png')

    plt.clf()

    return f'static/pie_{hsh}.png'


@router.message(Command('stats'))
@router.message(F.text == 'Статистика 📊')
async def show(message: types.Message, db: Database) -> None:
    await message.answer_photo(
        photo=FSInputFile(await pie_plot(db, message.from_user.id)),
        caption='Ваша статистика по задачам'
    )
