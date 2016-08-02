# -*- coding: utf-8 -*-
# © 2015 Roel Adriaans - B-Informed B.V.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.osv import osv
from openerp import SUPERUSER_ID


class stock_move(osv.osv):
    _inherit = "stock.move"

    def product_price_update_before_done(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        product_dict = {}
        for move in self.browse(cr, uid, ids, context=context):
            # adapt standard price on incomming moves if the product cost_method is 'average'
            if (move.location_id.usage == 'supplier') and (move.product_id.cost_method == 'average'):
                product = move.product_id
                prod_id = move.product_id.id
                # New Functionality, use qty_available from product.product, not the product template
                qty_available = move.product_id.qty_available
                if product_dict.get(prod_id):
                    product_avail = qty_available + product_dict[prod_id]
                else:
                    product_dict[prod_id] = 0
                    product_avail = qty_available
                if product_avail <= 0:
                    new_std_price = move.price_unit
                else:
                    # Get the standard price
                    amount_unit = product.standard_price
                    new_std_price = ((amount_unit * product_avail) + (move.price_unit * move.product_qty)) / (
                    product_avail + move.product_qty)
                product_dict[prod_id] += move.product_qty
                # Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
                ctx = dict(context or {}, force_company=move.company_id.id)
                product_obj.write(cr, SUPERUSER_ID, [product.id], {'standard_price': new_std_price}, context=ctx)
