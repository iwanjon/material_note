# -*- coding: utf-8 -*-




# from odoo import api, fields, models

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from pdb import set_trace as sstt

class OmSupplier(models.Model):
    _name = "om.suppliers"
    _description = "Supplier Model"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', size= 50,  required=True)
    status = fields.Boolean(string="Status", default = False)

   
    @api.constrains('code')
    def check_code(self):
        for rec in self:
            # sstt()
            material = self.env['om.suppliers'].search([('code', '=', rec.code),('id', "!=", rec.id)])
            if material:
                raise ValidationError(_("Code %s Already Exists" % rec.code))
            
   # @api.multi
    def write(self, vals):
        if  vals.get('code'):
            if self.code == vals.get("code"):
                res = super(OmSupplier, self).write(vals)
                return res
            
            material = self.env['om.materials'].search([('code', '=', vals.get("code"))])
            if material:
                raise ValidationError(_("code already exists. current code is %s" % vals.get('code')))

        res = super(OmSupplier, self).write(vals)
        return res
    