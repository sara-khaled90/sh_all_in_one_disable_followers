# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.user_id and self.env.company.sh_disable_follower_responsible_picking:
            res.message_unsubscribe([res.user_id.partner_id.id])
        return res

    def write(self, vals):
        if vals.get('user_id',False):
            user_id = self.env['res.users'].sudo().search([('id','=',vals.get('user_id',False))],limit=1)
            if user_id and self.env.company.sh_disable_follower_responsible_picking:
                res = super(StockPicking, self).write(vals)
                if self:
                    for rec in self:
                        rec.message_unsubscribe([user_id.partner_id.id])
                return res
        return super(StockPicking, self).write(vals)

    def message_subscribe(
            self,
            partner_ids=None,
            channel_ids=None,
            subtype_ids=None
            ):
        if self.env.company.sh_disable_follower_create_picking and 'manually_added_follower' not in self.env.context:
            return False
        else:
            return super(StockPicking, self).message_subscribe(
                partner_ids,
                channel_ids,
                subtype_ids
                )