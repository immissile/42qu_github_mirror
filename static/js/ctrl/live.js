/*
61 word
62 note
*/

(function() {
	var FEED_ATTR_BASE = "id rt_list fav cid rid reply_count create_time name txt txt_more",
	FEED_ATTR_TXT_BASE = FEED_ATTR_BASE + " tag_id tag_name",
	QUESTION_ATTR_BASE = " question_id question_user question_user_link",
	FEED_ATTR = {
		61: FEED_ATTR_BASE + QUESTION_ATTR_BASE,
		62: FEED_ATTR_TXT_BASE,
		63: FEED_ATTR_TXT_BASE,
		64: FEED_ATTR_TXT_BASE + QUESTION_ATTR_BASE,
		65: FEED_ATTR_TXT_BASE,
		66: FEED_ATTR_TXT_BASE,
		67: FEED_ATTR_TXT_BASE,
		68: FEED_ATTR_BASE + " place_name address time_row1 time_row2 time_diff_day",
		69: FEED_ATTR_BASE
	},
	DATE_ATTR = "name link unit title pic".split(' ');
	for (var i in FEED_ATTR) {
		FEED_ATTR[i] = (FEED_ATTR[i] + "").split(' ')
	}

	function array2zsite(a) {
		return {
			name: a[0],
			link: a[1]
		}
	}

	function init(result) {
		var data = {
			"item": []
		},
		i = 0,
		j,
		attr,
		item = result[5],
		t,
		rt_list;
		for (; i < DATE_ATTR.length; ++i) {
			data[DATE_ATTR[i]] = result[i]
		}


		for (i = 0; i < item.length; ++i) {
			result = item[i];
			t = {};
			attr = FEED_ATTR[result[3]];
			result_length = result.length;
			for (j = 0; j < result_length; ++j) {
				t[attr[j]] = result[j]
			}
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
			data.item.push(t)
			//console.info(t)
		}

		return data
	}

	function init_result(result) {
		var length = result.length,
		item = [],
		i = 0,
		data,
		pre_zsite_id;

		for (; i < length; ++i) {
			data = init(result[i])
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
			begin_id.val(
			result.pop())
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
    
	/* 显示全部 */
	fdtxt = function(e, id) {
		var txt = $(e).parents('.fdtxt'),
		all = txt.find(".fdall");
		all.addClass("fdloading").find('.fdext').remove()
		$.get("/j/fdtxt/" + id, function(htm) {
			txt.find('.fdtxtin').html('<pre class="fdpre">' + htm + "</pre>")
			if (all.find('a').length) {
				all.removeClass('fdloading')
			} else {
				all.remove()
			}
		})
	}
	fdvideo = function(e, id) {
		var div = $('<div class="fdswf"><div class="fdloading"/></div>')
		$(e).replaceWith(div)
		$.get("/j/fdvideo/" + id, function(html) {
			div.html(html)
			var win = $(window),
			winst = win.scrollTop(),
			offset = div.offset().top + div.height() - winst - win.height();

			if (offset > 0) {
				win.scrollTop(winst + offset)
			}
		})
	}

    show_comment = function(id,count){
        var self = $('#fdtxt'+id)
        self.append('<div id="com_pop_'+id+'"><textarea class="comment_txt" id="txt_'+id+'"></textarea><div class="txt_submit"><span class="txt_err L">先写点什么吧</span><span class="btnw"><button onclick="com_submit('+id+')">加上去</button></span></div></div>')
        var self_a = self.parent().find($(".comment_a")).hide()
        self_a.replaceWith('<a id="close_a_'+id+'" href="javascript:close_txt('+id+','+count+');void(0)">收起</a>')
        self.find($('.comment_txt')).before('<div class="loading"></div>')
//请求数据:
        var data = {"comments":[{"username":"realfex","link":"http://realfex.42qu.com","content":"楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了"},{"username":"realfex","link":"http://realfex.42qu.com","content":"楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了"}]}
        self.find($('.loading')).replaceWith('<div class="comment_list" id="comment_list_'+id+'"></div>')
        for(i=0;i<data.comments.length;i++){
            var html = '<div class="comment_i"><a class="L c9" href="'+data.comments[i].link+'">'+data.comments[i].username+'</a><a href="javascript:void(0)" rel="'+data.comments[i].username+'" class="reply_at L"></a><pre class="com_cont">'+data.comments[i].content+'</pre></div>'
                $('#comment_list_'+id).append(html)
            }
            $('#comment_list_'+id).slideDown(function(){$(this).show()})
        }

    close_txt=function(id,count){
        $('#comment_list_'+id).slideUp(function(){$('#com_pop_'+id).remove();$('#close_a_'+id).replaceWith('<a href="javascript:show_comment('+id+','+count+');void(0)" class="comment_a"><span class="mr3">'+count+'</span>评论</a>')})
    }
    com_submit = function(id){
        var cont = $('#txt_'+id).val()
        if($.trim(cont)==''){
            var err = $('.txt_err')
            err.fadeOut(function(){err.fadeIn()})
            return false
        }
        var my = $('<div class="comment_i" style="display:none;"><span class="L c9">我</span><pre class="com_cont">'+cont+'</pre></div>')
        $('#comment_list_'+id).append(my)
        $('#txt_'+id).val('')
        my.fadeIn("slow",function(){my.show();})
        $.postJSON(
            'url',
            {
                "cont":cont,
                "user_id":1
            }
        )
    }
})()
