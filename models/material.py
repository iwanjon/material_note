# -*- coding: utf-8 -*-



# from odoo.odoo import api, fields, models

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from pdb import set_trace as sstt


class OmMaterial(models.Model):
    _name = "om.materials"
    _description = "Material Model"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True,  size=50)
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton'),
    ], required=True, default='fabric')
    buy_price = fields.Integer(string='Price', default=100)
    status = fields.Boolean(string="Status", default= False)
    supplier_id = fields.Many2one('om.suppliers',  string="Supplier",required=True)

    @api.model
    def create(self, vals):
        if not vals.get('buy_price')  or vals.get('buy_price') < 100:
            raise ValidationError(_("buy price cannot lower thann 100. Current value is %s" % vals.get('buy_price')))
        

        material = self.env['om.materials'].search([('code', '=', vals.get("code"))])
        if material:
            raise ValidationError(_("code already exists. current code is %s" % vals.get('code')))

        res = super(OmMaterial, self).create(vals)
        return res
    
    # @api.multi
    def write(self, vals):
        # sstt()
        if  vals.get('buy_price')  and  vals.get('buy_price') < 100:
            raise ValidationError(_("buy price cannot lower thann 100. Current value is %s" % vals.get('buy_price')))
        


        if  vals.get('code'):
            if self.code == vals.get("code"):
                res = super(OmMaterial, self).write(vals)
                return res
            
            material = self.env['om.materials'].search([('code', '=', vals.get("code"))])
            if material:
                raise ValidationError(_("code already exists. current code is %s" % vals.get('code')))

        res = super(OmMaterial, self).write(vals)
        return res
    



    # @api.constrains('code')
    # def check_code(self):
    #     for rec in self:
    #         material = self.env['om.materials'].search([('code', '=', rec.code),('id', "!=", rec.id)])
    #         if material:
    #             raise ValidationError(_("Code %s Already Exists" % rec.code))
    
    #  python odoo-bin -c ../odoo.conf  --test-enable --stop-after-init --test-tags=material_note
    # python odoo-bin -c ../odoo.conf -u material_note  
    # python odoo-bin -c ../odoo.conf -u material_note  -i material_note