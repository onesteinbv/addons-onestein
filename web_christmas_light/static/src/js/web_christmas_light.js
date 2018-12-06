odoo.define('christmas_light', function(require) {
    var core = require('web.core');
    var ajax = require('web.ajax');
    var christmas = require('christmas');

    if (!christmas.isItChristmas()) return;

    var qweb = core.qweb;

    christmas.user.done(function(user) {
        if(user.show_christmas_light) {
            ajax.loadXML('/web_christmas_light/static/src/xml/web_christmas_light.xml', qweb).done(function() {
                var html = qweb.render('web_christmas_light.Lightrope');
                $('.navbar-collapse').after(html);
            });
        }
    });
});