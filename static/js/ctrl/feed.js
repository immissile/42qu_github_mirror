/*
 0 -1 -1
 1 -1 -2
-1 -1  1
 0  1  1
 1  1 -1
-1  1  2
*/
(function() {

	$(".reply,.down,.up,.num,.rt,.rted").poshytip({
		className: 'tip-twitter',
		showTimeout: 100,
		alignTo: 'target',
		alignX: 'center',
		offsetY: 5,
		allowTipHover: false,
		fade: false,
		slide: false,
		liveEvents: true
	});

	var down = "down",
	up = "up",
	vote = "vote";
	function _(a, b, id, v) {
		var wj = $("#" + vote + id),
		w = wj[0],
		state = w.className.slice(4) - 0,
		num = wj.find('.num'),
		numv = num.text() - 0,
		c = v,
		notsame = (v != state) - 0;
		if (notsame) {
			v -= state
		} else {
			c = 0;
			v = - v
		}
		$.postJSON("/j/feed/" + a + notsame + "/" + id)
		w.className = vote + c;
		wj.find('a').blur()
		num.text(numv + v)

		var fancybox = $.fancybox;
		fancybox({
			content: '<form id="vote_reply" class="fancyreply"><h3>我认为 ...</h3><textarea name="txt"></textarea><div class="btns"><span class="btnw"><button class="btn" type="submit">表态</button></span></div></form>',
			onComplete: function() {
				var reply = $("#vote_reply"),
				textarea = reply.find("textarea");

				reply.submit(function() {
					var txt = $.trim(textarea.val());
					if (txt && txt.length) {
						fancybox.showActivity()
						$.postJSON("/j/po/reply/" + id, {
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
					} else {
						fancybox.close()
					}
					return false;
				})
				textarea.focus()
			}
		})

	}
	vote_up = function(id) {
		_(up, down, id, 1)
	}
	vote_down = function(id) {
		_(down, up, id, - 1)
	}
	$('.fav').live('click', function() {
		this.className = 'faving'
		$.postJSON('/j/feed/fav/' + this.rel, function() {
			this.className = 'faved'
		}
	})
	$('.faved').live('click', function() {
		this.className = 'faving'
		$.postJSON('/j/feed/unfav/' + this.rel, function() {
			this.className = 'fav'
		}
	})
})()
