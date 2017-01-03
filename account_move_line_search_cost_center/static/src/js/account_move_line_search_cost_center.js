openerp.account_move_line_search_cost_center = function (instance) {
    var QWeb = instance.web.qweb;

    instance.account_move_line_search_extension.ListSearchView.include({

        init: function() {
            var self = this;
            this._super.apply(this, arguments);
            this.current_cost_center;
        },

        set_change_events: function() {
            var self = this;
            this._super.apply(this, arguments);
            this.$el.parent().find('.oe_account_select_cost_center').change(function() {
                    self.current_cost_center = this.value === '' ? null : this.value;
                    self.do_search(self.last_domain, self.last_context, self.last_group_by);
                });
        },

        aml_search_domain: function() {
            var self = this;
            var domain = this._super.apply(this, arguments);
            if (self.current_cost_center) domain.push(['cost_center_id.name', 'ilike', self.current_cost_center]);
            return domain;
        },

    });
};
