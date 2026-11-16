from odoo import fields, models
from odoo.exceptions import AccessError
from odoo.tools import SQL


class WmsMockOperation(models.Model):
    _name = "wms.mock.operation"
    _description = "Операция WMS Mock"
    _auto = False
    _table = "wms_mock_operation_view"
    _order = "planned_at desc, id desc"

    external_id = fields.Char(readonly=True)
    operation_type = fields.Selection(
        [("inbound", "Приёмка"), ("outbound", "Отгрузка")],
        readonly=True,
    )
    document_state = fields.Char(readonly=True)
    planned_at = fields.Datetime(readonly=True)
    customer_code = fields.Char(readonly=True)

    def init(self) -> None:
        self.env.cr.execute(SQL("DROP VIEW IF EXISTS %s", SQL.identifier(self._table)))
        self.env.cr.execute(SQL(
            "CREATE VIEW %s AS SELECT id, external_id, operation_type, "
            "document_state, planned_at AT TIME ZONE 'UTC' AS planned_at, customer_code "
            "FROM wms_mock.operation",
            SQL.identifier(self._table),
        ))

    def create(self, vals_list):
        raise AccessError("WMS Mock доступен только для чтения.")

    def write(self, vals):
        raise AccessError("WMS Mock доступен только для чтения.")

    def unlink(self):
        raise AccessError("WMS Mock доступен только для чтения.")
