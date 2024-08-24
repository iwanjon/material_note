# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from pdb import set_trace as sstt




class supplier(http.Controller):


    @http.route('/supplier/view', type='http', auth='user', website=True, methods=["GET"])
    def tree_view(self, **kwargs):
        # Fetch data from the model
        search = kwargs.get("search")
        # sstt()
        # Render template with the data
        if search:
            records = request.env['om.suppliers'].search(["|",("code","ilike",search),("name","ilike",search)])
# ds = request.env['om.suppliers'].search([("code","ilike",search)])
# ds = request.env['om.suppliers'].search(["|",("code","ilike",search),("name","ilike",search)])
        else:
            records = request.env['om.suppliers'].search([])
        return request.render('material_note.tree_template_supplier', {
            "search":search,
            'records': records
        })
    
    @http.route('/supplier/view', type='http', auth='user', website=True, methods=["POST"])
    def tree_view_search(self, **kwargs):
        # Fetch data from the model
        # records = request.env['om.suppliers'].search([])
        search = kwargs.get("search")
        # Render template with the data
        if search != None or search.strip() != "":
            return request.redirect('/supplier/view?search='+search)
            
        return request.redirect('/supplier/view')


    @http.route('/supplier/create_record', type='http', auth='user', website=True)
    def create_record(self, **kwargs):
        # Render the create template (you need to create this template)

        errors = None
        if request.session.get("errors_create_supplier"):
            errors = request.session.get("errors_create_supplier")["errors"]
            del request.session["errors_create_supplier"]

        if errors:
            return request.render('material_note.create_template_supplier', {
                "errors":errors,
                # 'suppliers': suppliers,
                # 'type_options': type_options,
            })
    
        return request.render('material_note.create_template_supplier', {
            # 'suppliers': suppliers,
            # 'type_options': type_options,
        })


    @http.route('/supplier/create_record_action', type='http', auth='user', methods=['POST'], website=True)
    def create_record_action(self, **post):
        # Perform the delete operation
        # sstt()


           # Extract POST data
        name = post.get('name')
        code = post.get('code')


        # Validation
        errors = []
        if not name or name.strip() =="":
            errors.append('Name is required.')
        
        if not code or name.strip() =="":
            errors.append('Code is required.')
        
        if  request.env['om.suppliers'].search([("code","ilike", code)]).exists():
            errors.append('Code is exists.')
        


        if errors != []:


            request.session["errors_create_supplier"] = {"id":0, "errors":errors}

            return request.redirect('/supplier/create_record')
         
        # Create the record
        request.env['om.suppliers'].create({
            'name': name,
            'code': code,
            'status': True,
        })

        # return request.redirect('/my_module/success_page')
        return request.redirect('/supplier/view')


    @http.route('/supplier/edit_record/<int:record_id>', type='http', auth='user', website=True)
    def edit_record(self, record_id, **kwargs):
        record = request.env['om.suppliers'].sudo().browse(record_id)
        if not record.exists():
            return request.not_found()
        
        # sstt()
        errors =None

        # sstt()
        if request.session.get("errors_edit_supplier"):
            errors = request.session.get("errors_edit_supplier")["errors"]
            del request.session["errors_edit_supplier"]

        if errors:

            return request.render('material_note.edit_template_supplier', {
            "errors" :errors,
            "record_id":record_id,
            'record': record,
       
        })

        return request.render('material_note.edit_template_supplier', {
            "record_id":record_id,
            'record': record,
    
        })


    @http.route('/supplier/edit_record_action', type='http', auth='user', methods=['POST'], website=True)
    def edit_record_action(self, **post):
        # Perform the delete operation
        # sstt()


           # Extract POST data
        record_id = post.get('record_id')
        name = post.get('name')
        code = post.get('code')


        # Validation
        errors = []
        # sstt()
        if not record_id or record_id.strip() =="" :
            errors.append('Invalid record_id.')
            
        if record_id:
            try:
                record_id = int(record_id)

            except Exception:
                errors.append('record_id must be a valid int.')

        record = request.env["om.suppliers"].browse(record_id)
        if not record:
            errors.append('no record found.')


        if not name or name.strip() =="":
            errors.append('Name is required.')
        
        if not code or name.strip() =="":
            errors.append('Code is required.')
        
        if  request.env['om.suppliers'].search([("code","=", code),("id", "!=",record_id )]).exists():
            errors.append('Code is exists.')
        


        if errors != []:
            request.session["errors_edit_supplier"] = {"id":record_id, "errors":errors}
            # sstt()

            return request.redirect('/supplier/edit_record/'+str(record_id))
         
        # Create the record

        record.write({
            'name': name,
            'code': code,
            # 'status': True,
     

        })

        # return request.redirect('/my_module/success_page')
        return request.redirect('/supplier/view')



    @http.route('/supplier/delete_confirm/<int:record_id>', type='http', auth='user', website=True)
    def delete_confirm(self, record_id, **kwargs):
        # Fetch the record to display in the confirmation template
        record = request.env['om.suppliers'].browse(record_id)
        if not record.exists():
            return request.not_found()
        
        errors =None

        # sstt()
        if request.session.get("errors_delete_supplier"):
            errors = request.session.get("errors_delete_supplier")["errors"]
            del request.session["errors_delete_supplier"]

            return request.render('material_note.delete_confirm_template_supplier', {
                'record': record,
                'errors':errors
            })

        return request.render('material_note.delete_confirm_template_supplier', {
            'record': record,
        })

    @http.route('/supplier/delete_record/<int:record_id>', type='http', auth='user', methods=['POST'], website=True)
    def delete_record(self, record_id, **kwargs):
        # Perform the delete operation
        record = request.env['om.suppliers'].browse(record_id)
        record_relate = request.env['om.materials'].search([("supplier_id", "=", record_id)])
        # sstt()
        errors=[]
        if record.exists() and not record_relate :
            # try:
            record.unlink()
            # except Exception as e:
        if record_relate:
            errors.append("cant delete this data, may be is used by other record")
        # sstt()
        if errors != []:
            request.session["errors_delete_supplier"] = {"id":record_id, "errors":errors}
            return request.redirect('/supplier/delete_confirm/'+str(record_id))
        
        return request.redirect('/supplier/view')

