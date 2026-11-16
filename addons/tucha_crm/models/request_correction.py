from odoo import fields, models
from odoo.exceptions import UserError


class TuchaRequest(models.Model):
    _inherit = "tucha.request"

    def action_take(self) -> None:
        """Реальная гонка сохранена как Senior-задача для кандидата."""
        self.check_access("write")
        for request in self:
            if request.taken_by == self.env.user:
                raise UserError("Вы уже взяли эту заявку.")
            if request.taken_by and not self.env.user.has_group(
                "tucha_crm.group_tucha_manager"
            ):
                raise UserError("Заявку уже взял другой оператор.")
        self.write({"taken_by": self.env.uid, "taken_at": fields.Datetime.now()})

    def action_release(self) -> None:
        if not self.env.user.has_group("tucha_crm.group_tucha_manager"):
            raise UserError("Снять заявку с оператора может только менеджер.")
        self.write({"taken_by": False, "taken_at": False})
