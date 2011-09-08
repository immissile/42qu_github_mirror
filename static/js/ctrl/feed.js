$('.fav').live('click', function() {
	if (!$.cookie.get('S')) {
		return login();
	}
	var self = this, pnum=$(self).prev();
	self.className = 'faving'
	$.postJSON('/j/feed/fav/' + this.rel, function() {
		self.className = 'faved';
        if(pnum.hasClass("pnum")){
            pnum.html(pnum.html()-0+1)
        }
	})
})
$('.faved').live('click', function() {
	var self = this, pnum=$(self).prev();
	self.className = 'faving'
	$.postJSON('/j/feed/unfav/' + this.rel, function() {
		self.className = 'fav';
        if(pnum.hasClass("pnum")){
            pnum.html(pnum.html()-1)
        }
	})
})

function share(id) {
	if (!$.cookie.get('S')) {
		return login();
	}
	var fancybox = $.fancybox;
	fancybox({
		content: '<form id="vote_reply" class="fancyreply"><h3>推荐语</h3><textarea name="txt"></textarea><div class="btns"><span class="btnw"><button class="btn" type="submit">分享</button></span></div></form>',
		onComplete: function() {
			var reply = $("#vote_reply"),
			textarea = reply.find("textarea");

			reply.submit(function() {
				var txt = $.trim(textarea.val());
				fancybox.showActivity()
				$.postJSON("/j/feed/up/" + id, {
					'txt': txt
				},
				function(r) {
					if (r.can_not_reply) {
						fancybox({
							content: CANNOT_REPLY
						})
					} else {
						fancybox.close()
					}
				})
				return false;
			})
			textarea.focus()
		}
	})
}
