$('#zsite_link a').click(function() {
	if (!$.cookie.get('S')) {
		login()
		return false
	} else if ($("#i_verify").length) {
		$.fancybox({
			content: '<div class="tc f16 pd16" style="width:250px"><p>想浏览此链接吗?<p><p><a href="/i/verify">先点此申请认证吧 , 亲</a></p></div>'
		})
		return false
	} else {
		this.target = "_blank"
	}
})
$('#event_join_btn').submit(function() {
	if (!$.cookie.get('S')) {
		login()
		return false
	} else if ($("#i_verify").length) {
		$.fancybox({
			content: '<div class="tc f16 pd16" style="width:250px"><p>想报名吗?<p><p><a href="/i/verify">先点此申请认证吧 , 亲</a></p></div>'
		})
		return false
	}
})

function nav2_touch(){
    if(!islogin())return;
    var html = $('html,body'),
        e=$("#nav2_touch").blur(),  
        drop = $(e[0].parentNode).find('div');

        function _() {
            drop.hide()
            html.unbind('click', _)
        }

        if (drop.is(":hidden")) {
            drop.show()
            html.click(_)
            clicked = true;
        } else {
            _()
        }
};




/* 显示全部 */
 function fdtxt(e, id) {
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
 function fdvideo(e, id) {
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

