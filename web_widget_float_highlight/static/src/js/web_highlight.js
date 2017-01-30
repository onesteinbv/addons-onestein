odoo.define("web.float.highlight", function (require) {
    "use strict";
    var form_widgets = require("web.form_widgets");

    form_widgets.FieldFloat.include({


        _load_my_default: function (option, parameter, load_defaults, load_value, def_value) {
            return (option && parameter) || load_defaults && load_value || def_value;
        },

        init: function () {
            this._super.apply(this, arguments);

            var internal_apply = false

            if (
                this.options && (
                    this.options.lower_threshold ||
                    this.options.upper_threshold ||
                    this.options.lower_bg_color ||
                    this.options.middle_bg_color ||
                    this.options.upper_bg_color ||
                    this.options.lower_font_color ||
                    this.options.middle_font_color ||
                    this.options.upper_font_color ||
                    this.options.load_defaults
                )
            )
                internal_apply = true;

            var load_defaults = this._load_my_default(this.options, this.options.load_defaults, false, false, false);

            var options = {
                lower_threshold: this._load_my_default(this.options, this.options.lower_threshold, false, false, 0),
                upper_threshold: this._load_my_default(this.options, this.options.upper_threshold, false, false, 0),
                lower_bg_color: this._load_my_default(this.options, this.options.lower_bg_color, load_defaults, "red", "white"),
                middle_bg_color: this._load_my_default(this.options, this.options.middle_bg_color, false, false, "white"),
                upper_bg_color: this._load_my_default(this.options, this.options.upper_bg_color, load_defaults, "green", "white"),
                lower_font_color: this._load_my_default(this.options, this.options.lower_font_color, load_defaults, "white", "#666666"),
                middle_font_color: this._load_my_default(this.options, this.options.middle_font_color, false, false, "#666666"),
                upper_font_color: this._load_my_default(this.options, this.options.upper_font_color, load_defaults, "white", "#666666"),
                always_work: this._load_my_default(this.options, this.options.always_work, false, false, false),
                load_defaults: load_defaults,
                apply: internal_apply
            };

            this.options = options;
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments);

            self.render_value();
            if (self.options.apply)
            {
                this.on("change:value", this, function () {
                    self.render_value();
                });
            }
        },

        render_value: function () {
            this._super();
            var self = this;
            if ((this.get("effective_readonly") && self.options.apply )|| self.options.always_work) {
                var bg_color = null;
                var font_color = null;
                var val = this.get("value");
                if (self.options.lower_threshold <= self.options.upper_threshold) {
                    if (val < self.options.lower_threshold) {
                        bg_color = self.options.lower_bg_color;
                        font_color = self.options.lower_font_color;
                    } else if (self.options.upper_threshold < val) {
                        bg_color = self.options.upper_bg_color;
                        font_color = self.options.upper_font_color;
                    } else {
                        bg_color = self.options.middle_bg_color;
                        font_color = self.options.middle_font_color;
                    }
                    this.$el.css({
                        "background-color": bg_color,
                        "color": font_color
                    });
                }
            }
        }
    });
});
