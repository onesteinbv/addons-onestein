odoo.define('christmas', function(require) {
    var session = require('web.session');
    var rpc = require('web.rpc');

    var christmas = $.deparam($.param.querystring()).christmas !== undefined;

    var isItChristmas = function() {
        var now = new Date();
        return (now.getMonth() == 11 && now.getDate() > 7 ||
                now.getMonth() == 0 && now.getDate() < 7 ||
                christmas);
    };

    var userLoad = $.Deferred();
    if (isItChristmas()) {
        var user = rpc.query({
            model: 'res.users',
            method: 'search_read',
            domain: [
                ['id', '=', session.uid]
            ],
            fields: [
                'show_christmas_light',
                'play_christmas_music',
                'show_christmas_santa',
                'show_christmas_snowflakes'
            ] // TODO: Make inheritable for sub modules
        }).then(function (result) {
            userLoad.resolve(result[0]);
        });
    }


    return {
        isItChristmas: isItChristmas,
        user: userLoad.promise()
    }
});