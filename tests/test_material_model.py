# tests/test_task_views.py
from odoo.tests import common
from odoo.exceptions import ValidationError

# class TestTaskViews(common.TransactionCase):

#     def setUp(self):
#         super(TestTaskViews, self).setUp()
#         # Create a test task
#         self.Task = self.env['task.task']
#         self.task = self.Task.create({
#             'name': 'Test Task',
#             'status': 'draft',
#             'type': 'bug'
#         })

#     def test_tree_view(self):
#         """ Test the tree view to ensure it displays the task correctly """
#         tree_view = self.env.ref('your_module.view_task_tree')
#         self.assertTrue(tree_view, "Tree view not found")
        
#         # Access the tree view via the web interface
#         # Check if the created task is listed
#         tasks = self.env['task.task'].search([])
#         self.assertGreater(len(tasks), 0, "No tasks found in the tree view")

#     def test_form_view(self):
#         """ Test the form view to ensure it displays and saves data correctly """
#         form_view = self.env.ref('your_module.view_task_form')
#         self.assertTrue(form_view, "Form view not found")
        
#         # Access the form view via the web interface
#         task = self.env['task.task'].browse(self.task.id)
#         self.assertEqual(task.name, 'Test Task', "Task name does not match")
#         self.assertEqual(task.status, 'draft', "Task status does not match")
#         self.assertEqual(task.type, 'bug', "Task type does not match")

#     def test_create_task_via_form(self):
#         """ Test creating a new task via the form view """
#         task = self.Task.create({
#             'name': 'New Task',
#             'status': 'in_progress',
#             'type': 'feature'
#         })
#         self.assertTrue(task.id, "Task was not created")
#         self.assertEqual(task.name, 'New Task', "Task name does not match")
#         self.assertEqual(task.status, 'in_progress', "Task status does not match")
#         self.assertEqual(task.type, 'feature', "Task type does not match")

class TestMaterialViews(common.TransactionCase):

    def setUp(self):

        super(TestMaterialViews, self).setUp()
        self.env.cr.execute("TRUNCATE TABLE om_suppliers RESTART IDENTITY CASCADE;")
        self.env.cr.execute("TRUNCATE TABLE om_materials RESTART IDENTITY CASCADE;")
        # Create a test task
        self.Task = self.env['om.suppliers']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'fabric',
            })

        # self.Task = self.env['om.materials']
        # self.task = self.Task.create({
        #     'name': 'Test Task',
        #     'status': 1,
        #     'code': 'draft',
        #     'type': 'fabric',
        #     "buy_price":120,
        #     "supplier_id":1
        # })

    def test_insert_material_success(self):
        # Check if the created task is listed

        self.Task = self.env['om.materials']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'draft',
            'type': 'fabric',
            "buy_price":120,
            "supplier_id":1
        })
        material = self.env['om.materials'].search([])
        self.assertEqual(len(material), 1, "No tasks found in the tree view")



    def test_insert_material_failed_price_below_100(self):
        # Check if the created task is listed
        with self.assertRaises(ValidationError) as context:
            self.Task = self.env['om.materials']
            self.task = self.Task.create({
                'name': 'Test Task',
                'status': 1,
                'code': 'draft',
                'type': 'fabric',
                "buy_price":12,
                "supplier_id":1
            })
            # print(context.exception)
        self.assertTrue('buy price cannot lower thann 100. Current value is 12' == str(context.exception))


    def test_insert_material_failed_code_already_exists(self):
        # Check if the created task is listed
        with self.assertRaises(ValidationError) as context:
            self.Task = self.env['om.materials']
            self.task = self.Task.create({
                'name': 'Test Task',
                'status': 1,
                'code': 'draft',
                'type': 'fabric',
                "buy_price":120,
                "supplier_id":1
            })
            self.task = self.Task.create({
                'name': 'Test Task',
                'status': 1,
                'code': 'draft',
                'type': 'fabric',
                "buy_price":102,
                "supplier_id":1
            })
            # print(context.exception)
        self.assertTrue('code already exists. current code is draft' == str(context.exception))

    def test_insert_material_failed_type(self):
        # Check if the created task is listed
        with self.assertRaises(Exception) as context:
            self.Task = self.env['om.materials']
            self.task = self.Task.create({
                'name': 'Test Task',
                'status': 1,
                'code': 'draft',
                'type': 'fabricer',
                "buy_price":120,
                "supplier_id":1
            })

            # print(context.exception)
        self.assertTrue("Wrong value for om.materials.type: 'fabricer'" == str(context.exception))


    def test_update_material_success(self):
        # Check if the created task is listed
        # with self.assertRaises(ValidationError) as context:
        self.Task = self.env['om.materials']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'draft',
            'type': 'fabric',
            "buy_price":120,
            "supplier_id":1
        })
        self.task.write({
            "buy_price":1200,
            'code': 'drafter',
        })
            # print(context.exception)
        self.assertTrue('drafter' == self.task.code)
        self.assertTrue(1200 == self.task.buy_price)


    def test_update_material_failed_price_below_100(self):
        # Check if the created task is listed
        self.Task = self.env['om.materials']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'draft',
            'type': 'fabric',
            "buy_price":120,
            "supplier_id":1
        })
        with self.assertRaises(ValidationError) as context:

            self.task.write({
                "buy_price":12,
                'code': 'drafter',
            })
            # print(context.exception)
        self.assertTrue('buy price cannot lower thann 100. Current value is 12' == str(context.exception))

        # self.assertTrue('code already exists. current code is draft' == str(context.exception))
        # self.assertTrue(1200 == self.task.buy_price)

    def test_update_material_failed_code_already_exists(self):
        # Check if the created task is listed
        self.Task = self.env['om.materials']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'draft',
            'type': 'fabric',
            "buy_price":120,
            "supplier_id":1
        })

        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'drafter',
            'type': 'fabric',
            "buy_price":120,
            "supplier_id":1
        })
        with self.assertRaises(ValidationError) as context:

            self.task.write({
                "buy_price":120,
                'code': 'draft',
            })
            # print(context.exception)
        # self.assertTrue('buy price cannot lower thann 100. Current value is 12' == str(context.exception))

        self.assertTrue('code already exists. current code is draft' == str(context.exception))
        # self.assertTrue(1200 == self.task.buy_price)

    def test_update_material_failed_type(self):
        # Check if the created task is listed
        self.Task = self.env['om.materials']
        self.task = self.Task.create({
            'name': 'Test Task',
            'status': 1,
            'code': 'draft',
            'type': 'fabric',
            "buy_price":120,
            "supplier_id":1
        })

        with self.assertRaises(Exception) as context:

            self.task.write({
                "buy_price":120,
                'type': 'fabricer',
            })
            # print(context.exception)
        # self.assertTrue('buy price cannot lower thann 100. Current value is 12' == str(context.exception))

        self.assertTrue("Wrong value for om.materials.type: 'fabricer'" == str(context.exception))
        # self.assertTrue(1200 == self.task.buy_price)


    def test_delete_material(self):
        # Check if the created task is listed
        self.Task = self.env['om.materials'].create({
            'name': 'Test Task',
            'status': 1,
            'code': 'draft',
            'type': 'fabric',
            "buy_price":120,
            "supplier_id":1
        })
        from pdb import set_trace as sstt
        self.assertEqual(len(self.Task), 1, "not equal")
        self.Task.unlink()
        # sstt()
        self.Task = self.env['om.materials'].search([])
        self.assertEqual(len(self.Task), 0, "not equal")
