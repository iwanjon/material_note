# tests/test_task_views.py
from odoo.tests import common
from odoo.exceptions import ValidationError
from pdb import set_trace as sstt

class TestMaterialViews(common.TransactionCase):

    def setUp(self):

        super(TestMaterialViews, self).setUp()
        self.env.cr.execute("TRUNCATE TABLE om_suppliers RESTART IDENTITY CASCADE;")
        # self.env.cr.execute("TRUNCATE TABLE om_materials RESTART IDENTITY CASCADE;")
        # Create a test task
        # self.Task = self.env['om.suppliers']
        # self.task = self.Task.create({
        #     'name': 'Test Task',
        #     'status': 1,
        #     'code': 'fabric',
        #     })

        # self.Task = self.env['om.materials']
        # self.task = self.Task.create({
        #     'name': 'Test Task',
        #     'status': 1,
        #     'code': 'draft',
        #     'type': 'fabric',
        #     "buy_price":120,
        #     "supplier_id":1
        # })

    def test_insert_supplier_success(self):
        # Check if the created task is listed

        self.Task = self.env['om.suppliers']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'fabric',
            })
        
        suppliers = self.env['om.suppliers'].search([])
        self.assertEqual(len(suppliers), 1, "No tasks found in the tree view")



    def test_insert_supplier_failed_code_already_exists(self):
        # Check if the created task is listed
        with self.assertRaises(ValidationError) as context:
            self.Task = self.env['om.suppliers']
            self.task = self.Task.create({
                'name': 'Test Task',
                'status': 1,
                'code': 'fabric',
                })
            # sstt()

            self.task = self.Task.create({
                'name': 'Test Task',
                'status': 1,
                'code': 'fabric',
                })
            # print(context.exception)
            # raise(context.exception)
        self.assertTrue('Code fabric Already Exists' == str(context.exception))

 


    def test_update_material_success(self):
        # Check if the created task is listed
        # with self.assertRaises(ValidationError) as context:
        self.Task = self.env['om.suppliers']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'fabric',
            })
        self.task.write({

            'code': 'drafter',
        })
            # print(context.exception)
        self.assertTrue('drafter' == self.task.code)



    def test_update_material_failed_code_already_exists(self):
        # Check if the created task is listed
        self.Task = self.env['om.suppliers']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'fabric',
            })

        self.Task = self.env['om.suppliers']
        self.task = self.Task.create({
            'name': 'Test Task2',
            'status': 1,
            'code': 'fabricer',
            })
        self.assertTrue('fabricer' == self.task.code)
        
        with self.assertRaises(ValidationError) as context:

            self.task.write({

                'code': 'fabric',
            })
            # print(context.exception)
        # self.assertTrue('buy price cannot lower thann 100. Current value is 12' == str(context.exception))

        self.assertTrue('Code fabric Already Exists' == str(context.exception))
        # self.assertTrue(1200 == self.task.buy_price)




    def test_delete_material(self):
        # Check if the created task is listed
        self.Task = self.env['om.suppliers'].create({
            'name': 'Test Task2',
            'status': 1,
            'code': 'fabricer',
            })
        # from pdb import set_trace as sstt
        self.assertEqual(len(self.Task), 1, "not equal")
        self.Task.unlink()
        # sstt()
        self.Task = self.env['om.suppliers'].search([])
        self.assertEqual(len(self.Task), 0, "not equal")
