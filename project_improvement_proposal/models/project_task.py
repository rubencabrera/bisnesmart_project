# -*- coding: utf-8 -*-
##############################################################################
# (c) 2015 bisnesmart
# License AGPL-3 - See LICENSE file on root folder for details
##############################################################################
from openerp import models, fields, api


class ProjectTasks(models.Model):
    _inherit = "project.task"

    description_proposal = fields.Text(help="Proposal description.")
    proposal_ok = fields.Boolean(help="Check if this task is a improvementt proposal")
    applicant_id = fields.Many2one('res.partner', string='Apllicant', help="Person who demmand the improvement proposal")

    defaults = {
    'proposal_ok': False,
    }

    def action_proposal_send(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email, with the edi proposal template message loaded by default
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'project', 'email_template_task_proposal')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'project.task',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
