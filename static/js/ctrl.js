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
function b1024(){
    function winresize(){
        var body=$("body")
        if(body.width() < 1024){
            body.addClass('b1024') 
        }else{
            body.removeClass('b1024')
        }
    }
    winresize()
    $(window).resize(winresize)
}
jQuery.fn.extend({
	elastic_login: function() {
        var self=this;
        $(function(){
            self.find('input').focus(islogin)
            self.find('textarea').elastic().focus(islogin)
        })
		return this.submit(islogin)
	},
    ctrl_enter : function (callback){
        $(this).keydown(function(event){
            event = event.originalEvent;
            if(event.keyCode == 13 && (event.metaKey||event.ctrlKey)) {
                callback&&callback()
                return false;
            }
        })
    }
})

function islogin(){
    if (!$.cookie.get('S')) {
        login()
        return false
    }
    return true
}

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
            var foot = $('<div class="zsite_foot"><a href="#B"></a></div>')
			body.append(foot)
            foot.find('a').click(function() {
				if (!IE6) {
					win.scrollTop(0)
					return false
				}
			}).html(
                $(".site").html() || location.host
            )
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

CANNOT_REPLY = '<div class="fancyban"><p>抱歉 ...</p><p>为了维护讨论的气氛</p><p>未认证用户不能发言</p><p><a href="/i/verify">点此补充您的资料吧</a></p></div>'


function follow_a(id) {
	var a = $("#follow_a" + id),
	text = a.html(),
	url = "/j/follow",
	follow = "关注",
	follow_rm = "淡忘";
	if (text == follow) {
		text = follow_rm;
	} else {
        text = follow;
        url += "/rm"
	}
	$.postJSON(url + "/" + id)
	a.html(text)
}

function fav_com(){
    var a = $('#fav_a'),
    text = a.html(),
    url = '/j/fav',
    fav = '收藏',
    fav_rm = '淡忘'
    if(text == fav){
        text = fav_rm,
        fancybox = $.fancybox
        fancybox({
            content:'<form id="fav_reply" class="fancyreply"><h3>写写你对它的看法吧 ...</h3><textarea name="txt" class="fav_txt"></textarea><div class="btns"><span class="btnw"><button class="btn" type="submit">确定</button></span><span class="R fav_tip c9"></span></div></form>',
            onComplete: function() {
                var reply = $('#fav_reply'),
				textarea = $('.fav_txt'),
                tip = $('.fav_tip'),
                can_say = txt_maxlen(textarea, tip, 142)
   				reply.submit(function() {
					var txt = $.trim(textarea.val());
					if (txt && txt.length) {
                        if(can_say()){
						    fancybox.showActivity()
						    $.postJSON("/j/fav", {
							    'txt': txt
						    })
						    fancybox.close()
                        }else{
                            tip.fadeOut(function(){tip.fadeIn()})
                            return false
                        }
					} else {
						fancybox.close()
					}
					return false
				})
				textarea.focus()
            }
        })
    } else {
        if(confirm("取消收藏 , 确定 ?")){
    		text = fav;
	    	url += "/rm"
        }
	}
	$.postJSON(url)
	a.html(text)
}

function txt_maxlen(txt, tip,  maxlen, update, cancel) {
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

	//form.submit(
	txt.input(function() {
		po_word_update(this.value)
	})
	
    return function() {
		if (po_word_update(txt.val()) > 0) {
			txt.focus()
			return false
		}
        return true
	}
}

function feed_load_maker(FEED_ATTR_BASE ){
    FEED_ATTR_BASE+=" fav cid rid site_id reply_count create_time name txt txt_more"

	var FEED_ATTR_TXT_BASE = FEED_ATTR_BASE + " tag_id tag_name",
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
		69: FEED_ATTR_BASE,
        72: FEED_ATTR_BASE,
        73: FEED_ATTR_BASE
	}
	for (var i in FEED_ATTR) {
		FEED_ATTR[i] = (FEED_ATTR[i] + "").split(' ')
	}
    function _(result){
        var t = {}, attr = FEED_ATTR[result[3]], j=0;
        result_length = result.length;
        for (; j < result_length; ++j) {
            t[attr[j]] = result[j]
        }
        return t
    }
    return _
}



/*
        var isCtrl = false;
        element.keyup(function (e) {
            if(e.which == 17) isCtrl=false;
        }).keydown(function (e) {
            if(e.which == 17) isCtrl=true;
            if(e.which == 13 && isCtrl == true) {
                callback && callback()
            }
        });*/
