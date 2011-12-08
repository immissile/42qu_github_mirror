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
        content: '<form id="vote_reply" class="fancyreply"><h3>推荐语</h3><textarea name="txt"></textarea><div class="btns"><span class="rec_tip share_sync">142字以内</span><span class="btnw"><button class="btn" type="submit">分享</button></span><span class="syncp"><input type="checkbox" name="sync" class="sync" value="同时发表评论"/></span></div></form>',
		onComplete: function() {
			var reply = $("#vote_reply"),
			textarea = reply.find("textarea"),
            tip = $('.rec_tip');
            can_say = txt_maxlen(textarea, tip, 142);
			reply.submit(function() {
				var txt = $.trim(textarea.val());
                if(can_say()){
				fancybox.showActivity()
				$.postJSON("/j/feed/up/" + id, {
					'txt': txt,
                    'sync': $(".sync").is(":checked")
				},
				function(r) {
					if (r.can_not_reply) {
						fancybox({
							content: CANNOT_REPLY
						})
					} else {
						fancybox.close()
					}
				})}else{
                    tip.fadeOut(function(){tip.fadeIn()})
                    return false
                }
				return false;
			})
			textarea.focus()
		}
	})
}
