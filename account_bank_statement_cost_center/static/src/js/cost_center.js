/*
 * Copyright © 2016 ICTSTUDIO <http://www.ictstudio.eu>
 * License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
 */

openerp.account_bank_statement_cost_center = function (instance) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;

    instance.web.account.bankStatementReconciliation.include({

        init: function(parent, context) {
            this._super.apply(this, arguments);

            this.create_form_fields['cost_center_id'] = {
                id: "cost_center_id",
                index: 5,
                label: _t("Cost Center"),
                corresponding_property: "cost_center_id",
                tabindex: 15,
                constructor: instance.web.form.FieldMany2One,
                field_properties: {
                    relation: "account.cost.center",
                    string: _t("Cost Center"),
                    type: "many2one",
                },
            };

        },

    });

    instance.web.account.bankStatementReconciliationLine.include({

        initializeCreateForm: function() {
            this._super.apply(this, arguments);
            var self = this;
            self.cost_center_id_field.set("value", self.st_line.cost_center_id)
        },

        prepareCreatedMoveLineForPersisting: function(line) {
            var dict = this._super.apply(this, arguments);
            var self = this;
            if (line.cost_center_id) dict['cost_center_id'] = line.cost_center_id;
            return dict;
        },

    });

};