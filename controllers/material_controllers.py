# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from pdb import set_trace as sstt




class material(http.Controller):
    @http.route('/material', auth='public')
    def index(self, **kw):
        return "Hello, world"



    @http.route('/material/view', type='http', auth='user', website=True, methods=["GET"])
    def tree_view(self, **kwargs):
        # Fetch data from the model
        search = kwargs.get("search")
        # sstt()
        # Render template with the data
        if search:
            records = request.env['om.materials'].search(["|","|","|","|",("code","ilike",search),("type","ilike",search),("supplier_id.name","ilike",search),("name","ilike",search),("type","ilike",search)])
# ds = request.env['om.materials'].search([("code","ilike",search)])
# ds = request.env['om.materials'].search(["|",("code","ilike",search),("name","ilike",search)])
        else:
            records = request.env['om.materials'].search([])
        return request.render('material_note.tree_template', {
            "search":search,
            'records': records
        })
    
    @http.route('/material/view', type='http', auth='user', website=True, methods=["POST"])
    def tree_view_search(self, **kwargs):
        # Fetch data from the model
        # records = request.env['om.materials'].search([])
        search = kwargs.get("search")
        # Render template with the data
        if search != None or search.strip() != "":
            return request.redirect('/material/view?search='+search)
            
        return request.redirect('/material/view')


    @http.route('/material/create_record', type='http', auth='user', website=True)
    def create_record(self, **kwargs):
       
        supplier_records = request.env['om.suppliers'].search([('status', '=', True)])
        suppliers = supplier_records.read(['id', 'name'])
        # Define type options

        errors = None
        type_options = [
            ('fabric', 'Fabric'),
            ('cotton', 'Cotton'),
            ('jeans', 'Jeans'),
        ]
        if request.session.get("errors_create_material"):
            errors = request.session.get("errors_create_material")["errors"]
            del request.session["errors_create_material"]

        if errors:
            return request.render('material_note.create_template', {
                "errors":errors,
                'suppliers': suppliers,
                'type_options': type_options,
            })
    
        return request.render('material_note.create_template', {
            'suppliers': suppliers,
            'type_options': type_options,
        })


    @http.route('/material/create_record_action', type='http', auth='user', methods=['POST'], website=True)
    def create_record_action(self, **post):
        # Perform the delete operation
        # sstt()


           # Extract POST data
        name = post.get('name')
        code = post.get('code')
        type = post.get('type')
        buy_price = post.get('buy_price')
        supplier_id = post.get('supplier_id')

        # Validation
        errors = []
        if not name or name.strip() =="":
            errors.append('Name is required.')
        
        if not code or name.strip() =="":
            errors.append('Code is required.')
        
        if  request.env['om.materials'].search([("code","ilike", code)]).exists():
            errors.append('Code is exists.')
        
        if not type or type.strip() =="" or type not in ["fabric", "cotton","jeans"]:
            errors.append('Invalid type.')

        if not buy_price or buy_price.strip() =="" :
            errors.append('Invalid price.')
            
        if buy_price:
            try:
                buy_price = float(buy_price)
                if buy_price < 100:
                    errors.append('price must at least 100.')
            except Exception:
                errors.append('Price must be a valid number.')



        if not supplier_id or supplier_id.strip() =="":
            errors.append('Invalid supplier.')

        if supplier_id:
            try:
                supplier_id = int(supplier_id)
                if not request.env['om.suppliers'].browse(supplier_id).exists():
                    errors.append('Supplier does not exist.')
            except Exception:
                errors.append('Supplier ID must be a valid integer.')

        if errors != []:


            request.session["errors_create_material"] = {"id":0, "errors":errors}
  
            return request.redirect('/material/create_record')
         
        # Create the record
        request.env['om.materials'].create({
            'name': name,
            'code': code,
            'type': type,
            'status': True,
            'buy_price': buy_price,
            'supplier_id': supplier_id,
        })

        # return request.redirect('/my_module/success_page')
        return request.redirect('/material/view')


    @http.route('/material/edit_record/<int:record_id>', type='http', auth='user', website=True)
    def edit_record(self, record_id, **kwargs):
        record = request.env['om.materials'].sudo().browse(record_id)
        if not record.exists():
            return request.not_found()
        
        # sstt()
        errors =None
        supplier_records = request.env['om.suppliers'].search([('status', '=', True)])
        suppliers = supplier_records.read(['id', 'name'])
        # Define type options
        type_options = [
            ('fabric', 'Fabric'),
            ('cotton', 'Cotton'),
            ('jeans', 'Jeans'),
        ]
        # sstt()
        if request.session.get("errors_edit_material"):
            errors = request.session.get("errors_edit_material")["errors"]
            del request.session["errors_edit_material"]

        if errors:
            return request.render('material_note.edit_template', {
            "errors" :errors,
            "record_id":record_id,
            'record': record,
            "suppliers":suppliers,
            "types":type_options
        })
        return request.render('material_note.edit_template', {
            "record_id":record_id,
            'record': record,
            "suppliers":suppliers,
            "types":type_options
        })


    @http.route('/material/edit_record_action', type='http', auth='user', methods=['POST'], website=True)
    def edit_record_action(self, **post):
        # Perform the delete operation
        # sstt()


           # Extract POST data
        record_id = post.get('record_id')
        name = post.get('name')
        code = post.get('code')
        type = post.get('type')
        buy_price = post.get('buy_price')
        supplier_id = post.get('supplier_id')

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

        record = request.env["om.materials"].browse(record_id)
        if not record:
            errors.append('no record found.')


        if not name or name.strip() =="":
            errors.append('Name is required.')
        
        if not code or name.strip() =="":
            errors.append('Code is required.')
        
        if  request.env['om.materials'].search([("code","=", code),("id", "!=",record_id )]).exists():
            errors.append('Code is exists.')
        
        if not type or type.strip() =="" or type not in ["fabric", "cotton","jeans"]:
            errors.append('Invalid type.')

        if not buy_price or buy_price.strip() =="" :
            errors.append('Invalid price.')
            
        if buy_price:
            try:
                buy_price = float(buy_price)
                if buy_price < 100:
                    errors.append('price must at least 100.')
            except Exception:
                errors.append('Price must be a valid number.')



        if not supplier_id or supplier_id.strip() =="":
            errors.append('Invalid supplier.')

        if supplier_id:
            try:
                supplier_id = int(supplier_id)
                if not request.env['om.suppliers'].browse(supplier_id).exists():
                    errors.append('Supplier does not exist.')
            except Exception:
                errors.append('Supplier ID must be a valid integer.')

        if errors != []:
            request.session["errors_edit_material"] = {"id":record_id, "errors":errors}
            # sstt()
   
            return request.redirect('/material/edit_record/'+str(record_id))
         
        # Create the record

        record.write({
            'name': name,
            'code': code,
            'type': type,
            # 'status': True,
            'buy_price': buy_price,
            'supplier_id': supplier_id,


        })

        # return request.redirect('/my_module/success_page')
        return request.redirect('/material/view')



    @http.route('/material/delete_confirm/<int:record_id>', type='http', auth='user', website=True)
    def delete_confirm(self, record_id, **kwargs):
        # Fetch the record to display in the confirmation template
        record = request.env['om.materials'].browse(record_id)
        if not record.exists():
            return request.not_found()
        
        return request.render('material_note.delete_confirm_template', {
            'record': record,
        })

    @http.route('/material/delete_record/<int:record_id>', type='http', auth='user', methods=['POST'], website=True)
    def delete_record(self, record_id, **kwargs):
        # Perform the delete operation
        record = request.env['om.materials'].browse(record_id)
        if record.exists():
            record.unlink()
        return request.redirect('/material/view')

    # @http.route('/material/update_record', type='http', auth='user', website=True, methods=['POST'])
    # def update_record(self, **post):
    #     record_id = int(post.get('record_id'))
    #     record = request.env['your.model'].sudo().browse(record_id)
    #     if record.exists():
    #         record.write({
    #             'name': post.get('name'),
    #             'field2': post.get('field2'),
    #         })
    #     # Redirect to the tree view after update
    #     return request.redirect('/my_module/view')

    # @http.route('/material/delete_record/<int:record_id>', type='http', auth='user', website=True, methods=['POST'])
    # def delete_record(self, record_id, **kwargs):
    #     record = request.env['your.model'].sudo().browse(record_id)
    #     if record.exists():
    #         record.unlink()
    #     # Redirect to the tree view after deletion
    #     return request.redirect('/my_module/view')