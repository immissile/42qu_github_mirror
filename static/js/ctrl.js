IE6 = $.browser.msie && $.browser.version < 7 && ! window.XMLHttpRequest

_gaq = [['_setAccount', 'UA-18596900-1'], ['_trackPageview'], ['_trackPageLoadTime']];

(function() {

	var ga = document.createElement('script');
	var s = document.getElementsByTagName('script')[0];
	ga.type = 'text/javascript';
	ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl': 'http://www') + '.google-analytics.com/ga.js';
	s.parentNode.insertBefore(ga, s);

})()

function _rm(prefix, url) {
	return function(id) {
		if (confirm('删除 , 确定 ?')) {
			var t = $(prefix + id)
			t.fadeOut(function() {
				t.remove()
			})
			$.postJSON(url + id)
		}
	}
}
jQuery.fn.extend({
	elastic_login: function() {
		function _() {
			if (!$.cookie.get('S')) {
				login()
				return false
			}
		}
		this.find('input').focus(_)
		this.find('textarea').elastic().focus(_)
		return this.submit(_)
	}
})

function login() {
	$.fancybox({
		href: '/j/login',
		onComplete: function() {
			$("#login").attr('action', "/auth/login?next=" + encodeURIComponent(location.href))
			login_autofill("_pop")
		}
	});
}
function login_autofill(suffix) {
	suffix = suffix || ''
	var mail = $("#login_mail" + suffix).focus(),
	password = $("#login_password" + suffix),
	mail_val = $.cookie.get("E");
	if (mail_val && mail.val() == '') {
		mail.val(mail_val).select();
	}
	mail_val = mail.val();
	if (mail_val && mail_val.length) {
		password.focus()
	}
}
/*
 var dnav = $("#dnav").show(), dmore = $("#dmore").addClass('dmore').hide(),body=$('html,body');
 function _(){
     dmore.hide()
     body.unbind('click',_)
 }
 dnav.click(function(e){
         dnav.blur()
         if(dmore.is(":hidden")){
             dmore.show()
             e.stopPropagation()
             body.click(_)
         }else{
             _()
         }
 })
 */
function init_none() {
	$(function() {
		var body = $('body'),
		back = $('<a href="#B" id="sB"></a>'),
		win = $(window);
		if ((body.height() - 128) > $(window).height()) {
			body.append($('<a class="zsite_foot" href="#B"></a>').click(function() {
				if (!IE6) {
					win.scrollTop(0)
					return false
				}
			}).html(
			$(".site").html() || location.host))
		}

		if (!IE6) {
			body.append(back)
			win.scroll(function() {
				if (win.scrollTop() >= 512) {
					back.fadeIn();
				}
				else {
					back.fadeOut();
				}
			})
			back.click(function() {
				back.hide()
				win.scrollTop(0)
				return false
			})
		}

	})
}
function init_user() {
	var html = $('html,body');

	$("#H .DA").click(function(e) {
		var t = this,
		drop = $(this.parentNode).find('div');
		t.blur();
		function _() {
			drop.hide()
			html.unbind('click', _)
		}
		if (drop.is(":hidden")) {
			drop.show()
			e.stopPropagation()
			html.click(_)
			clicked = true;
		} else {
			_()
		}
	})

	init_none()
}

CANNOT_REPLY = '<div class="fancyban"><p>啊 , 出错了 !</p><p>为了假装一本正经的讨论气氛</p><p>未认证用户没有发言权</p><p><a href="/i/verify">点此申请认证吧</a></p></div>'

function follow_a(id) {
	var a = $("#follow_a" + id),
	text = a.html(),
	url = "/j/follow",
	follow = "关注",
	follow_rm = "淡忘";

	if (text == follow) {
		text = follow_rm;
		fancybox = $.fancybox;
		fancybox({
			content: '<form id="follow_reply" class="fancyreply"><h3>你好 ...</h3><textarea name="txt"></textarea><div class="btns"><span class="btnw"><button class="btn" type="submit">此致 , 敬礼 !</button></span><span id="follow_secret_span"><input type="checkbox" name="secret" id="follow_reply_secret"><label for="follow_reply_secret">私语</label></span></div></form>',
			onComplete: function() {
				var reply = $("#follow_reply"),
				textarea = reply.find('textarea');
				reply.submit(function() {
					var txt = $.trim(textarea.val());
					if (txt && txt.length) {
						fancybox.showActivity()
						$.postJSON("/j/follow/reply/" + id, {
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
					return false
				})
				textarea.focus()
			}
		})
	} else {
		text = follow;
		url += "/rm"
	}
	$.postJSON(url + "/" + id)
	a.html(text)
}

function txt_maxlen(txt, tip, form, maxlen, update, cancel) {
	function po_word_update(value) {
		var len = cnenlen(value),
		html,
		diff = 0;
		if (len) {
			diff = len - maxlen;
			if (diff > 0) {
				html = '<span style="color:red">超出<span>' + diff + "</span>字</span>"
			} else {
				html = '<span style="color:#999"><span>' + len + "</span>字</span>"
				//为了ie6 多加一层span
			}
            update && update()
		} else {
			html = '&nbsp;'
            cancel && cancel()
		}
		tip.html(html);
		return diff
	}

	form.submit(function() {
		if (po_word_update(txt.val()) > 0) {
			txt.focus()
			return false
		}
	})
	txt.input(function() {
		po_word_update(this.value)
	})
}
