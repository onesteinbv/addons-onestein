/*
 # Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
 # License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
*/
openerp.account_costcenter_policy = function (instance) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;

    instance.web.account.bankStatementReconciliation.include({

        init: function(parent, context) {
            this._super.apply(this, arguments);
            this.model_account = new instance.web.Model("account.account");
            this.map_costcenter_policy = {};
            var required_dict = {};
            _.each(this.create_form_fields, function(field) {                
                if (field['required']) {
                    required_dict[field['id']] = false;
                    };
                });
            /* 
            this.required_fields_set is used to check if all required fields 
            are filled in before showing the 'Ok' button on a line
            */
            this.required_fields_set = required_dict;
        },

        start: function() {
            var tmp = this._super.apply(this, arguments);
            var self = this;
            maps = [];
            maps.push(this.model_account
                .query(['id', 'costcenter_policy'])
                .filter([['type', 'not in', ['view', 'consolidation', 'closed']]])
                .all().then(function(data) {
                    _.each(data, function(o) {
                        self.map_costcenter_policy[o.id] = o.costcenter_policy;
                        });
                })
            );
            return $.when(tmp, maps);
        },

    });

    instance.web.account.bankStatementReconciliationLine.include({

        init: function(parent, context) {
            this._super.apply(this, arguments);
            this.map_costcenter_policy = this.getParent().map_costcenter_policy;
            this.required_fields_set = this.getParent().required_fields_set;
            },

        UpdateRequiredFields: function(elt) {
            if (elt.get('value')) {
                this.required_fields_set[elt.name] = true;
            } else {
                this.required_fields_set[elt.name] = false;
            };
            var balanceChangedFlag = this.CheckRequiredFields(elt);
            if (balanceChangedFlag) {
                this.balanceChanged();      
            } else {
                this.$(".button_ok").text("OK").removeClass("oe_highlight").attr("disabled", "disabled");
            };
        },

        CheckRequiredFields: function() {
            var flag = _.every(this.required_fields_set);
            return flag;
        },

        formCreateInputChanged: function(elt, val) {
            this._super.apply(this, arguments);
            if (elt === this.account_id_field) {
                if (this.map_costcenter_policy[elt.get('value')] === 'always') {
                    this.cost_center_id_field.modifiers = {'required': true, 'readonly': false};
                    this.required_fields_set['cost_center_id'] = false;
                    if (! this.cost_center_id_field.get('value')) {
                        this.$(".button_ok").text("OK").removeClass("oe_highlight").attr("disabled", "disabled");
                    };
                } else {
                    delete this.required_fields_set['cost_center_id'];
                    if (this.map_costcenter_policy[elt.get('value')] === 'never') {
                        this.cost_center_id_field.set('value', false);
                        this.cost_center_id_field.modifiers = {'required': false, 'readonly': true};
                    } else {
                        this.cost_center_id_field.modifiers = {'required': false, 'readonly': false};
                    };
                };
                this.cost_center_id_field.field_manager.do_show();
            };
            if (elt.name === 'cost_center_id') {
                if ('cost_center_id' in this.required_fields_set)  {
                    this.UpdateRequiredFields(elt);
                };
            };
        },

    });

};
