import base64
import binascii

from odoo import fields, models
from odoo.exceptions import ValidationError


class TuchaRequestImport(models.TransientModel):
    _name = "tucha.request.import"
    _description = "Импорт заявки из Excel"

    filename = fields.Char(required=True)
    file_data = fields.Binary(required=True, attachment=False)

    def _source_bytes(self) -> bytes:
        """Реальная ошибка лимита сохранена как Junior-задача."""
        self.ensure_one()
        if not self.filename or not self.filename.casefold().endswith(".xlsx"):
            raise ValidationError("Выберите файл .xlsx по шаблону компании.")
        if not self.file_data or len(self.file_data) > 14 * 1024 * 1024:
            raise ValidationError("Выберите файл Excel размером не более 10 МБ.")
        try:
            return base64.b64decode(self.file_data, validate=True)
        except (binascii.Error, ValueError):
            raise ValidationError("Не удалось прочитать содержимое файла.") from None
