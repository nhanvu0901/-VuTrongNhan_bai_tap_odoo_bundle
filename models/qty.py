from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError


class Qty(models.Model):
    _name ="product.bundle.qty"



    Is_add_range = fields.Boolean(string="Is add range", required=False)
    Quantity = fields.Integer()
    Qty_start = fields.Integer()
    Qty_end = fields.Integer()
    Discount_value = fields.Char(string="Discount")
    bundle_id = fields.Many2one('product.bundle')

    @api.depends('Quantity','Qty_start','Qty_end')
    def check_qty(self):
     if self.Is_add_range == True:
         if(self.Qty_start > self.Qty_end):
             raise ValidationError(_("Quantity start smaller than quantity end"))
     else:
         if(self.Quantity <0):
             raise ValidationError(_("Quantity start smaller than quantity end"))



