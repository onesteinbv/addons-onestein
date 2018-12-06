odoo.define('christmas_music', function(require) {
    var christmas = require('christmas');

    if(!christmas.isItChristmas()) return;

    christmas.user.done(function(user) {
        if (user.play_christmas_music) {
            var audio = new Audio('/web_christmas_music/static/music/jingle-bells.mp3');
            audio.loop = true;
            audio.play();
        }
    });
});