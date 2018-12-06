odoo.define('christmas_santa.Santa', function(require) {
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');

    var Santa = Widget.extend({
        xmlDependencies: [
            '/web_christmas_santa/static/src/xml/web_christmas_santa.xml'
        ],
        template: 'web_christmas_santa.Santa',
        getPositions: function(toLeft) {
            var right = -this.$el.width();
            var top = $(document).height() * Math.random();
            var top1 = $(document).height() * Math.random();
            var left = $(document).width() + this.$el.width();

            var from = {'right': right, 'top': top};
            var to = {'right': left, 'top': top1};

            return {
                'from': toLeft ? from : to,
                'to': toLeft ? to : from
            }
        },
        resetPosition: function(pos) {
            this.$el.css(pos);
        },
        orientate: function(toLeft) {
            this.$el.toggleClass('santa-right', !toLeft);
        },
        move: function(toLeft) {
            this.orientate(toLeft);
            var path = this.getPositions(toLeft);
            this.resetPosition(path.from);
            var done = $.Deferred();
            this.$el.animate(path.to, {
                duration: 5000,
                easing: 'linear',
                done: function() {
                    done.resolve();
                }
            });
            return done.promise();
        }
    });

    return Santa;
});

odoo.define('christmas_santa', function(require) {
    var christmas = require('christmas');
    var Santa = require('christmas_santa.Santa');
    require('web.dom_ready');

    if(!christmas.isItChristmas()) return;

    var santa = new Santa();

    var left = false;

    var move = function() {
        santa.move(!left).done(function() {
            left = !left;
            setTimeout(move, 1000);
        });
    }

    christmas.user.done(function(user) {
        if (user.show_christmas_santa) {
            santa.appendTo($('.o_web_client'));
            move();
        }
    });
});