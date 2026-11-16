from odoo import fields, models


class TuchaBillingLine(models.Model):
    _name = "tucha.billing.line"
    _description = "Локальное начисление Sandbox"
    _order = "service_date desc, id desc"

    name = fields.Char(string="Начисление", required=True)
    customer_id = fields.Many2one(
        "res.partner",
        string="Клиент",
        required=True,
        ondelete="restrict",
        index=True,
    )
    request_id = fields.Many2one(
        "tucha.request",
        string="Заявка",
        required=True,
        ondelete="restrict",
        index=True,
    )
    service_date = fields.Date(string="Дата услуги", required=True, index=True)
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    amount = fields.Monetary(string="Сумма", required=True)
