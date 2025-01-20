# Copyright 2025 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestProjectTaskRequiredProject(common.TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(TestProjectTaskRequiredProject, cls).setUpClass()
        cls.partner_1 = cls.env['res.partner'].create({
            'name': 'Test Parner',
            'email': 'test.partner@test.com'})

        cls.project_test = cls.env['project.project'].with_context({'mail_create_nolog': True}).create({
            'name': 'Project Test',
            'partner_id': cls.partner_1.id})
        
        cls.task_created = cls.env['project.task'].create({
            'name': 'Task Already Created',
            'project_id': cls.project_test.id})

    def test_edit_existing_task(self):
        with self.assertRaises(UserError, msg="'ERROR! A project has not been selected for the task."):
            self.task_created.write({'project_id': None})

    def test_create_new_task(self):
        with self.assertRaises(UserError, msg="'ERROR! A project has not been selected for the task."):
            self.env['project.task'].create({'name': 'Test Task 1'})
        # with Form(self.env['project.task']) as task_form:
        #     task_form.name = 'Test Task 1'
        # self.assertRaises(UserError, task_form.save())
