function feed_page(feed_url, feeds_id, parse_result, loaded, end){

    var begin_id = $("#begin_id").val(0),
        autocount=0,
        feed_load = $("#feed_load").click(function() {
            render_feed()
            feed_load.hide()
            autocount = 0;
        }),
        feed_loading = $("#feed_loading"),
        is_loading = 0;

	function render_feed() {
		if (is_loading) return;
		is_loading = 1;

		feed_load.hide();
		feed_loading.show();

		$.postJSON(
            feed_url + begin_id.val(),
        function(result){ 
            if (result.length < 2) {
                feed_load.hide()
                feed_loading.hide()
                end && end()
                return
            }
            is_loading = 0;
            begin_id.val( result.pop());

            $('#feed').tmpl(
                parse_result(result)
            ).appendTo(feeds_id);
			feed_loading.slideUp(function() {
				feed_load.show()
			});
            loaded&&loaded()
        })
    }
    $(function(){
        render_feed()
        var win = $(window)
        win.scroll(function() {
            if (autocount < 5 && ! is_loading && win.scrollTop() > ($(document).height() - win.height() * 2)) {
                autocount += 1;
                render_feed();
            }
        })
    })
};



