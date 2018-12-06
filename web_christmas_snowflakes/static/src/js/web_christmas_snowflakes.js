odoo.define('christmas_snowflakes', function(require) {
    var christmas = require('christmas');

    if (!christmas.isItChristmas()) return;

    christmas.user.done(function(user) {
        if (user.show_christmas_snowflakes) {
            $(document).ready(function() {
                $.fn.snow();
            });
        }
    });
});