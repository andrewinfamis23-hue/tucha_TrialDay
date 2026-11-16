from datetime import timedelta

from odoo import api, fields, models


class TuchaDashboard(models.Model):
    _name = "tucha.dashboard"
    _description = "Сводка заявок Sandbox"

    name = fields.Char(default="Сводка")
    open_count = fields.Integer(compute="_compute_metrics")
    today_request_ids = fields.Many2many(
        "tucha.request",
        compute="_compute_metrics",
        string="Ближайшие заявки",
    )

    @api.depends_context("uid")
    def _compute_metrics(self) -> None:
        start = fields.Datetime.now().replace(hour=0, minute=0, second=0)
        end = start + timedelta(days=1)
        domain = [
            ("active", "=", True),
            ("stage", "not in", ("completed", "cancelled")),
            ("planned_from", ">=", start),
            ("planned_from", "<", end),
        ]
        request_model = self.env["tucha.request"]
        count = request_model.search_count(domain)
        requests = request_model.search(domain, order="planned_from, id", limit=8)
        for dashboard in self:
            dashboard.open_count = count
            dashboard.today_request_ids = requests
