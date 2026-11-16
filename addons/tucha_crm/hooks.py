from datetime import datetime, timedelta

from odoo import Command, api


def post_init_hook(env: api.Environment) -> None:
    """Создаёт только синтетические данные при первой установке модуля."""
    russian = env.ref("base.lang_ru")
    if not russian.active:
        russian.active = True

    if env["tucha.request"].search_count([]):
        return

    group = env.ref("tucha_crm.group_tucha_candidate")
    user = env["res.users"].with_context(no_reset_password=True).create({
        "name": "Кандидат Sandbox",
        "login": "candidate@example.test",
        "email": "candidate@example.test",
        "lang": "ru_RU",
        "password": "candidate-sandbox-2026",
        "groups_id": [Command.link(group.id)],
    })
    manager_group = env.ref("tucha_crm.group_tucha_manager")
    env["res.users"].with_context(no_reset_password=True).create({
        "name": "Менеджер Sandbox",
        "login": "manager@example.test",
        "email": "manager@example.test",
        "lang": "ru_RU",
        "password": "manager-sandbox-2026",
        "groups_id": [Command.link(manager_group.id)],
    })
    customers = env["res.partner"].create([
        {
            "name": f"ООО Тестовый клиент {number}",
            "is_company": True,
            "tucha_sandbox_customer": True,
            "ref": f"FAKE-{number}",
        }
        for number in range(1, 6)
    ])

    start = datetime(2026, 11, 16, 8)
    stages = ("new", "processing", "completed", "cancelled")
    requests = env["tucha.request"].with_user(user).create([
        {
            "name": f"TEST-{number:03d}",
            "customer_id": customers[(number - 1) % len(customers)].id,
            "request_type": "inbound" if number % 2 else "outbound",
            "planned_from": start + timedelta(hours=number),
            "planned_to": start + timedelta(hours=number + 1),
            "stage": stages[(number - 1) % len(stages)],
        }
        for number in range(1, 51)
    ])
    env["tucha.billing.line"].with_user(user).create([
        {
            "name": f"Начисление {number:03d}",
            "request_id": request.id,
            "customer_id": request.customer_id.id,
            "service_date": request.planned_from.date(),
            "amount": 1000 + number * 37.5,
        }
        for number, request in enumerate(requests[:25], start=1)
    ])
