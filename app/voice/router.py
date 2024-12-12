import logging
import os

from aiogram import Router, types, F

from app.bot import bot
from app.voice.adapter import ogg_to_wav, stt

router = Router()


@router.message(F.content_type == types.ContentType.VOICE)
async def handle_voice_message(message: types.Message) -> None:
    ogg_path = f"temp/voice_{message.from_user.id}.ogg"
    wav_path = f"temp/voice_{message.from_user.id}.wav"
    try:
        try:
            file = await bot.get_file(message.voice.file_id)
            await bot.download_file(file.file_path, ogg_path)
        except Exception as e:
            await message.reply(
                "Произошла ошибка при скачивании голосового сообщения"
            )
            logging.info("Error: %s", e)
            raise

        try:
            wav_path = ogg_to_wav(ogg_path, wav_path)
        except Exception as e:
            await message.reply(
                "Произошла ошибка при конвертации голосового сообщения"
            )
            logging.info("Error: %s", e)
            raise

        try:
            text = stt(wav_path)
        except Exception as e:
            await message.reply("Произошла ошибка при распознавании речи")
            logging.info("Error: %s", e)
            raise

        lower_text = text.lower()

        if "создай задачу" in lower_text:
            task_name = lower_text.replace("создай задачу", "").strip()
            reply = f"Задача '{task_name}' создана!"
        elif "покажи задачи" in lower_text:
            reply = "Вот список ваших задач: \n1. Обновить документацию \n2. Проверить баги"
        else:
            reply = f"Я распознал ваш запрос: '{text}', но не понял, что с ним делать."

        await message.answer(reply)

    finally:
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
