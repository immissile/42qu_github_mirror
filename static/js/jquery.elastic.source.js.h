(function (jQuery) {
    jQuery.fn.extend({
        elastic: function () {
            return this.each(function () {
                if (this.type !== 'textarea') {
                    return false;
                }
                var self = this
                function check() {
                    var inp = $(self),
                        textarea_clone
                    if (!textarea_clone) {

                        textarea_clone = inp.clone().css({
                            position: 'absolute',
                            top: '-999em',
                            left: '-999em',
                            width: inp.width()
                        }).appendTo('body');
                    }
                    inp.css('overflow','hidden')
                    h = textarea_clone.val(inp.val()).height(0).scrollTop(10000).scrollTop();
                    inp.css('height', Math.min(Math.max(h, 80), 600));

                }
                check();

                jQuery(this).keyup(check)
            })
        }
    });
})(jQuery);
