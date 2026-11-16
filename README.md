# Tucha Trial Day

Изолированная тестовая песочница для технического собеседования Python/Odoo-разработчиков в TuchaML.

Репозиторий содержит небольшой рабочий срез CRM: заявки, клиентов, локальные
начисления и мок складской системы. Задачи взяты из реальных проблем TuchaCRM,
но весь код, учётные записи и данные здесь учебные.

## Для кого этот репозиторий

- **Кандидату** — чтобы за 3–4 часа выполнить три небольших практических
  задания уровня Junior, Middle и облегчённого Senior и отправить Pull Request.
- **Проверяющему** — чтобы воспроизвести решение одной командой, прочитать
  тесты и оценить Python, SQL, Odoo ORM, безопасность и работу с Git.

Это не рабочая CRM и не копия production. Репозиторий не содержит SSH-доступа,
`.env`, токенов, клиентских выгрузок, рабочих адресов или deploy-скриптов.

## Что находится внутри

- Odoo Community 18;
- PostgreSQL 18;
- модуль `addons/tucha_crm`;
- 5 фейковых клиентов и 50 фейковых заявок;
- 25 тестовых начислений;
- 20 операций склада в схеме `wms_mock`;
- CI с Ruff и `compileall`;
- три задания в [TASKS.md](TASKS.md).

Складская система заменена на мок. Прикладная роль `crm_sandbox` может только
читать `wms_mock.*`; PostgreSQL запрещает ей `INSERT`, `UPDATE` и `DELETE`.

## Что потребуется

- Git;
- Docker Desktop или Docker Engine с Compose v2;
- свободный локальный порт `18069`;
- 4–6 ГБ свободного места для Docker-образов и volumes.

Python и PostgreSQL отдельно устанавливать не нужно.

## Как запустить

```bash
git clone https://github.com/tuchaML/tucha_TrialDay.git
cd tucha_TrialDay
docker compose up --build
```

Первый запуск загружает официальные образы и может занять несколько минут.
Дождитесь строки о запуске HTTP-сервиса Odoo, затем откройте:

<http://127.0.0.1:18069>

Учебная учётная запись:

```text
База:   tucha_sandbox
Логин:  candidate@example.test
Пароль: candidate-sandbox-2026
```

PostgreSQL не публикуется на хост. Odoo доступен только через localhost.

## Полезные команды

Запустить в фоне:

```bash
docker compose up -d --build
```

Посмотреть состояние и журнал:

```bash
docker compose ps
docker compose logs -f odoo
```

Остановить без удаления данных:

```bash
docker compose down
```

Полностью сбросить учебную базу и создать seed заново:

```bash
docker compose down -v
docker compose up -d --build
```

`down -v` удаляет только volumes Compose-проекта `tucha-trial-day`, но все
сделанные через интерфейс учебные данные будут потеряны.

## Проверки перед сдачей

```bash
ruff check addons tests
python -m compileall -q addons tests
python -m unittest discover -s tests -v
docker compose config -q
```

Дополнительно кандидат должен добавить Odoo-тесты для изменённого поведения и
описать команды их запуска в Pull Request.

Запустить добавленные Odoo-тесты на локальной фейковой базе:

```bash
docker compose build odoo
docker compose stop odoo
docker compose run --rm --no-deps --entrypoint odoo odoo \
  --config=/etc/odoo/odoo.conf --database=tucha_sandbox \
  --update=tucha_crm --test-enable --test-tags /tucha_crm \
  --stop-after-init --no-http
docker compose up -d odoo
```

## Как выполнять и сдавать

1. Сделайте fork репозитория.
2. Создайте ветку `feature/test-day-<фамилия>` от `sandbox-main`.
3. Выполните задания из [TASKS.md](TASKS.md).
4. Добавьте тесты для каждого исправления.
5. Запустите проверки.
6. Откройте Pull Request в ветку `sandbox-main` исходного репозитория.
7. Заполните PR-шаблон: решение, проверки, изменения модели и риски.

Не добавляйте в PR секреты, реальные данные, дампы БД, `.env`, сторонние
сетевые интеграции или адреса рабочих систем.

## Структура

```text
addons/tucha_crm/   учебный Odoo-модуль
docker/             образ, конфигурация и фейковый seed
tests/              быстрые проверки состава песочницы
.github/            CI и шаблон Pull Request
compose.yaml        локальные Odoo и PostgreSQL
TASKS.md            задания кандидату
```

## Что оцениваем

- умение читать существующий код до изменения;
- корректность Python и Odoo ORM;
- понимание индексов и частых ORM-запросов;
- аккуратность работы со статусами и датами;
- серверную защиту, а не только ограничения интерфейса;
- регрессионные тесты;
- понятную историю Git и описание архитектурного выбора.

Время выполнения всех заданий: ориентир 3–4 часа. Если времени не хватило,
оставьте рабочий результат и честно опишите в PR, что сделали бы следующим.
