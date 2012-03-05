$('.fav').live('click', function(e) {
    e.stopPropagation()
	if (!$.cookie.get('S')) {
		return login();
	}
	var self = this, pnum=$(self).prev(), id=this.rel, c = 'faved fav'+id;
	self.className = 'faving'
	$.postJSON('/j/feed/fav/' + id, function() {
        
		$('.fav'+id).attr('class',c);
        self.className = c

/*
	var self = $(this), pnum=$(self).prev(),url;
    if(self.hasClass('fav_tag'))
    {
        url='/j/fav';
    }else{
        url='/j/feed/fav/';
    }
    self.removeClass('fav');
    self.addClass('faving');
	$.postJSON(url + this.rel, function() {
        self.removeClass('faving');
		self.addClass('faved');
*/
        if(pnum.hasClass("pnum")){
            pnum.html(pnum.html()-0+1)
        }
	})
})
$('.faved').live('click', function(e) {
    e.stopPropagation()
	var self = this, pnum=$(self).prev(), id=this.rel, c = 'fav fav'+id;
	self.className = 'faving'
	$.postJSON('/j/feed/unfav/' + this.rel, function() {

		$('.fav'+id).attr('class',c);
        self.className = c;
/*
$('.faved').live('click', function() {
	var self = $(this), pnum=$(self).prev(),url;
    if(self.hasClass('fav_tag'))
    {
        url='/j/fav/rm';
    }else{
        url='/j/feed/unfav/';
    }
    self.removeClass('faved');
    self.addClass('faving');

	$.postJSON(url + this.rel, function() {
        self.removeClass('faving');
		self.addClass('fav');
*/
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
        content: '<form id="vote_reply" class="fancyreply"><h3>推荐语</h3><textarea tabindex="1" style="height:140px" name="txt"></textarea><div class="btns"><span class="rec_tip share_sync"></span><span class="btnw"><button class="btn" tabindex="3" type="submit">分享</button></span><span class="syncp"><input tabindex="2" id="sync" type="checkbox" name="sync" class="sync" /><label for="sync">同时发表评论</label></span><span class="sync_show"><a href="/i/bind" target="_blank" class="share_sync">微博同步</a></span></div></form>',
		onComplete: function() {
			var reply = $("#vote_reply"),
			textarea = reply.find("textarea"),
            tip = $('.rec_tip');
            textarea.focus()
            textarea.ctrl_enter( function(){reply.submit()});

            change = function(){$('.sync_show').hide();};
            can_say = txt_maxlen(textarea, tip, 142, change);
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
                    tip.fadeOut(function(){
                        tip.fadeIn()
                    })
                    return false
                }
				return false;
			})
			textarea.focus()
		}
	})
}

