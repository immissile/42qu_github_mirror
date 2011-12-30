function reply(id,at_txt){
	if (!$.cookie.get('S')) {
		return login();
	}
	var fancybox = $.fancybox;
	fancybox({
        content: '<form id="vote_reply" class="fancyreply"><h3>回复</h3><textarea tabindex="1" style="height:140px" name="txt"></textarea><div class="btns"><span class="rec_tip share_sync"></span><span class="btnw"><button class="btn" tabindex="3" type="submit">回复</button></span><span class="syncp"></div></form>',
		onComplete: function() {
			var reply = $("#vote_reply"),
			textarea = reply.find("textarea")
            textarea.focus().val(at_txt)
			reply.submit(function() {
				var txt = $.trim(textarea.val());
				fancybox.showActivity()
				$.postJSON("/j/po/reply/"+id, {
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
                })
			textarea.focus()
		}
	})
}
