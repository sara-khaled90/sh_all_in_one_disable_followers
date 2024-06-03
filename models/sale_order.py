# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if res.user_id and self.env.company.sh_disable_follower_salesperson:
            res.message_unsubscribe([res.user_id.partner_id.id])
        return res

    def write(self, vals):
        if vals.get('user_id',False):
            user_id = self.env['res.users'].sudo().search([('id','=',vals.get('user_id',False))],limit=1)
            if user_id and self.env.company.sh_disable_follower_salesperson:
                res = super(SaleOrder, self).write(vals)
                if self:
                    for rec in self:
                        rec.message_unsubscribe([user_id.partner_id.id])
                return res
        return super(SaleOrder, self).write(vals)

    def message_subscribe(
                        self,
                        partner_ids=None,
                        channel_ids=None,
                        subtype_ids=None
                        ):
        if self.env.company.sh_disable_follower_email and self.env.context.get('mark_so_as_sent') and 'manually_added_follower' not in self.env.context:
            return False
        elif self.env.company.sh_disable_follower_confirm_sale and not self.env.context.get('mark_so_as_sent') and 'manually_added_follower' not in self.env.context:
            return False
        else:
            return super(SaleOrder, self).message_subscribe(
                partner_ids, channel_ids, subtype_ids
            )
