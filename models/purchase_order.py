# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        if res.user_id and self.env.company.sh_disable_follower_pr_purchase:
            res.message_unsubscribe([res.user_id.partner_id.id])
        return res

    def write(self, vals):
        if vals.get('user_id',False):
            user_id = self.env['res.users'].sudo().search([('id','=',vals.get('user_id',False))],limit=1)
            if user_id and self.env.company.sh_disable_follower_pr_purchase:
                res = super(PurchaseOrder, self).write(vals)
                if self:
                    for rec in self:
                        rec.message_unsubscribe([user_id.partner_id.id])
                return res
        return super(PurchaseOrder, self).write(vals)

    def message_subscribe(
            self,
            partner_ids=None,
            channel_ids=None,
            subtype_ids=None
            ):
        if self.env.company.sh_disable_follower_email and 'manually_added_follower' not in self.env.context:
            return False
        else:
            return super(PurchaseOrder, self).message_subscribe(
                partner_ids,
                channel_ids,
                subtype_ids
                )
