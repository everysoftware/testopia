# Testopia - таск-трекер с ИИ

**Интеллектуальный таск-трекер для ведения проектов**

[![Lint](https://github.com/everysoftware/testopia/actions/workflows/ci.yml/badge.svg)](https://github.com/everysoftware/testopia/actions/workflows/ci.yml)

Testopia представляет собой мощный инструмент для управления задачами, который составляет для вас статистику
продуктивности и предлагает решения задач на основе ИИ.

<img src="/assets/onboarding.jpg" width="300" alt=""/><img src="/assets/checklists.PNG" width="300" alt=""/>

<img src="/assets/task.jpg" width="300" alt=""/><img src="/assets/solution.jpg" width="300" alt=""/>

<img src="/assets/stats.PNG" width="300" alt=""/>

## Руководство пользователя

Пользователь заходит в бот и создает новый чек-лист. В чек-листе он добавляет задачи, которые нужно выполнить.

Для помощи в выполнении задачи пользователь может получить решение от ИИ. ИИ анализирует задачу и предлагает
эффективное решение.

После выполнения задачи пользователь отмечает ее
как выполненную. После тестирования задачи пользователь может прикрепить отчет и отметить статус тестирования.

В любой момент пользователь может получить статистику по выполненным задачам в течение года и по состояния прохождения
тестов.

## Стек технологий

Python • Aiogram • PostgreSQL • SQLAlchemy • Redis • NumPy • Pandas • Matplotlib

## Сборка

1. Получите токен бота в Telegram у [@BotFather](https://t.me/BotFather)
2. Получите Client ID и Client Secret на [Sber Developers](https://developers.sber.ru/studio/workspaces)
3. Создайте файл окружения `.env` на основе `.env.example`
4. Запустите проект: `make up`

[Макеты Figma](https://www.figma.com/file/iJ7SMg6DCuCaDhNlieh3kd/Untitled?type=design&node-id=0-1&mode=design)

**Made with ❤️**
