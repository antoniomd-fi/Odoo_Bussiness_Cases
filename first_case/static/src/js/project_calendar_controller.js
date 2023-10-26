/** @odoo-module **/

import { ProjectCalendarController } from "@project/views/project_calendar/project_calendar_controller";
import { patch } from "@web/core/utils/patch";

patch(ProjectCalendarController.prototype, 'custom_calendar_project', {
    setup() {
        this._super();
        this.displayName += this.env._t(" - Milestones by Deadline");
    }
});

