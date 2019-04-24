/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('connector_office_365', function(require) {
    var CalendarRenderer = require('web.CalendarRenderer');
    var CalendarController = require('web.CalendarController');
    var CalendarModel = require('web.CalendarModel');
    var core = require('web.core');
    var time = require('web.time');
    var session = require('web.session');
    var qweb = core.qweb;

    CalendarController.include({
        custom_events: _.extend({}, CalendarController.prototype.custom_events, {
            syncOffice365Calendar: '_syncOffice365Calendar',
        }),

        _syncOffice365Calendar: function () {
            var self = this;
            return this._rpc({
                model: 'calendar.event',
                method: 'office_365_fetch',
                args: [this.model.data.start_date, this.model.data.end_date],
            }).done(function(result) {
                if (result && result.type === 'ir.actions.act_url') {
                    return self.trigger_up('do_action', {
                        action: result
                    });
                } else {
                    self.reload();
                }
            });
        },
    });

    CalendarRenderer.include({
        events: _.extend({}, CalendarRenderer.prototype.events, {
            'click .office_365_sync_button': '_onSyncOffice365Calendar',
        }),

        _initSidebar: function () {
            this._super.apply(this, arguments);

            if (this.model === 'calendar.event') {
                this.$syncButton = $(qweb.render('office_365.SyncButton'));
                this.$syncButton.appendTo(this.$sidebar);
            }
        },

        _onSyncOffice365Calendar: function () {
            this.trigger_up('syncOffice365Calendar');
        },
    });

    CalendarModel.include({
        setDate: function () {
            var res = this._super.apply(this, arguments);
            if (this.modelName === 'calendar.event') {
                this.trigger_up('syncOffice365Calendar');
            }
            var self = this;
        },
    });
});

