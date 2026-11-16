from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    tucha_sandbox_customer = fields.Boolean(
        string="Клиент песочницы",
        default=False,
        index=True,
    )
