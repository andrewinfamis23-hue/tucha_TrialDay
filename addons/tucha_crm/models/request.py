from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TuchaRequest(models.Model):
    _name = "tucha.request"
    _description = "Заявка TuchaCRM Sandbox"
    _order = "planned_from, id"

    active = fields.Boolean(default=True, index=True)
    name = fields.Char(string="Номер", required=True, index=True)
    customer_id = fields.Many2one(
        "res.partner",
        string="Клиент",
        required=True,
        ondelete="restrict",
        index=True,
    )
    request_type = fields.Selection(
        [("inbound", "Приёмка"), ("outbound", "Отгрузка")],
        string="Тип заявки",
        required=True,
        default="inbound",
        index=True,
    )
    # Реальная проблема сохранена: поле участвует в частых диапазонных запросах,
    # но индекс для очереди отсутствует.
    planned_from = fields.Datetime(string="Окно с", required=True)
    planned_to = fields.Datetime(string="Окно по", required=True)
    stage = fields.Selection(
        [
            ("new", "Новая"),
            ("processing", "В работе"),
            ("completed", "Завершена"),
            ("cancelled", "Отменена"),
        ],
        string="Статус",
        required=True,
        default="new",
        index=True,
    )
    taken_by = fields.Many2one(
        "res.users",
        string="Взял в работу",
        readonly=True,
        copy=False,
        index=True,
    )
    taken_at = fields.Datetime(string="Взята", readonly=True, copy=False)

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "Номер заявки должен быть уникальным."),
    ]

    @api.constrains("planned_from", "planned_to")
    def _check_window(self) -> None:
        for request in self:
            if request.planned_to <= request.planned_from:
                raise ValidationError("Конец окна должен быть позже начала.")
