(function (jQuery) {
    jQuery.fn.extend({
        elastic: function () {
            return this.each(function () {
                var self = this;
                if (self.type !== 'textarea') {
                    return false;
                }
                function check() {
                    var inp = $(self),
                        textarea_clone,
                        h;
                
                    if (!textarea_clone) {

                        textarea_clone = inp.clone().css({
                            position: 'absolute',
                            top: '-9999px',
                            left: '-9999px',
                            width: inp.width()
                        }).appendTo('body');
                    }

                    inp.css('overflow','hidden')
                    h = textarea_clone.val(inp.val()).height(0).scrollTop(999).scrollTop();
                    
                    inp.css('height', Math.max(h+7, 80));

                }
                check();

                jQuery(this).keyup(check)
            })
        }
    });
})(jQuery);
