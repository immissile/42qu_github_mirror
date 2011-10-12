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





