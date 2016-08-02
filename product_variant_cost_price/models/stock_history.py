# -*- coding: utf-8 -*-
# © 2016 Marcelo Pickler - Sistema Social
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields as fields2
import logging

_logger = logging.getLogger(__name__)


class StockHistory(models.Model):
    _inherit = 'stock.history'

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(StockHistory, self).read_group(
            domain, fields, groupby, offset=0,
            limit=None, orderby=False, lazy=True)
        for line in res:
            product = self.env['product.product'].browse(line['product_id'][0])
            if product.cost_method == 'average':
                line['inventory_value'] = product.standard_price*product.qty_available
        return res
