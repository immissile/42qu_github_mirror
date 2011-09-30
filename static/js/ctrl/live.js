/*
61 word
62 note
*/

(function() {
	var feed_loader = feed_load_maker( "id rt_list"),
	DATE_ATTR = "name link unit title pic".split(' ')
    ;

	function array2zsite(a) {
		return {
			name: a[0],
			link: a[1]
		}
	}

	function init(result, site_dict) {
		var data = {
			"item": []
		},
		i = 0,
		j,
		attr,
		item = result[5],
		t,
		rt_list,
        site_id;

		for (; i < DATE_ATTR.length; ++i) {
			data[DATE_ATTR[i]] = result[i]
		}


		for (i = 0; i < item.length; ++i) {
            t = feed_loader(item[i]);

			rt_list = t.rt_list;
			if (rt_list.length) {
				if (! (rt_list.length == 1 && rt_list[0][0] == 0)) {
					t.rt_list = []
					for (j = 0; j < rt_list.length; ++j) {
						if (rt_list[j][0]) {
							t.rt_list.push(rt_list[j])
						}
					}
					t.rt_list = $.map(t.rt_list, array2zsite);
				} else {
					t.rt_list = [0]
				}
			}

			t.create_time = $.timeago(t.create_time);
            
            site_id = t.site_id;
            if(site_id){
                t.site_name = site_dict[site_id];
                t.site_url = site_id+HOST_SUFFIX
            }

			data.item.push(t)
			//console.info(t)
		}

		return data
	}

	function init_result(result) {
		var site_dict = result.pop(),
        length = result.length,
		item = [],
		i = 0,
		data,
		pre_zsite_id;

		for (; i < length; ++i) {
			data = init(result[i], site_dict)
			if (data.zsite_id == pre_zsite_id) {
				data.zsite_same_as_pre = true
			} else {
				pre_zsite_id = data.zsite_id
			}
			item.push(data)
		}
		return item
	}

	var feed_load = $("#feed_load").click(function() {
		render_feed()
		feed_load.hide()
		autocount = 0;
	}),
	feed_loading = $("#feed_loading"),
	begin_id = $("#begin_id").val(0),
	is_loading = 0,
	autocount = 0;
	function render_feed() {
		if (is_loading) return;
		is_loading = 1;
		feed_load.hide()
		feed_loading.show()
		$.postJSON("/j/feed/" + begin_id.val(), function(result) {
			if (result.length == 1) {
				feed_load.hide()
				feed_loading.hide()
				return
			}
			is_loading = 0;
			begin_id.val( result.pop())
			$('#feed').tmpl(init_result(result)).appendTo("#feeds");
			feed_loading.slideUp(function() {
				feed_load.show()
			});
			//console.info(result.length)
			var prebottom, top, diff, self;
			$("#feeds .G3").each(function() {
				self = $(this)
				top = self.offset().top;
				if (self.hasClass('G3_AS_PRE') && prebottom !== undefined) {
					diff = prebottom - top
					if (diff) {
						this.style.marginTop = diff + "px"
					}
				}
				prebottom = self.offset().top + this.offsetHeight;
			})

		})
	}
	render_feed()
	var win = $(window)
	win.scroll(function() {
		if (autocount < 5 && ! is_loading && win.scrollTop() > ($(document).height() - win.height() * 2)) {
			autocount += 1;
			render_feed();
		}

	});
	/* 发微博 */
	var po_word_txt = $("#po_word_txt"),
	po_word_txt_bg = "po_word_txt_bg";
	po_word_txt.blur().val('').focus(function() {
		$(this).removeClass(po_word_txt_bg)
	}).blur(function() {
		var self = $(this),
		val = self.val();
		if (!val || ! val.length) {
			self.addClass(po_word_txt_bg)
		}
	}).addClass(po_word_txt_bg);
    
    function po_all_show_ext_hide(){
            po_all.show()
            po_ext.hide()
    }
    var po_all=$("#po_all"),po_ext=$('<a href="javascript:void(0)" id="po_ext"></a>').click(po_all_show_ext_hide);
    po_all.after(po_ext)
	$("#po_word_form").submit(
        txt_maxlen(
            po_word_txt, 
            $("#po_word_tip"), 
            142, 
            function(){
                po_all.hide()
                po_ext.show()
            },
            po_all_show_ext_hide
        )
    )
    
})()



$(function(){
    $('#po_word_txt').pop_at()
})

