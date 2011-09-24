(function( jQuery ){
jQuery.extend({
    cookie : {
        set:function(dict, days, path){
            if(typeof(days)=='string'){
                path=days;
                days=0;
            }
            days = days || 99;
            path = path||'/';
            var date = new Date();
            date.setTime(date.getTime()+(days*24*60*60*1000));
            var expires = "; expires="+date.toGMTString();
            for (var i in dict){
                document.cookie = i+"="+dict[i]+expires+"; path="+path;
            }
        },
        get:function(name) {
            var e = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(e) == 0) {
                    return c.substring(e.length,c.length).replace(/\"/g,'');
                }
            }
            return null;
        }
    },
    postJSON : function(url, data, callback) {
        data = data||{};
        if ( jQuery.isFunction( data ) ) {
            callback = data;
        }
        var _xsrf = jQuery.cookie.get("_xsrf");
        if(typeof data=="string"){
            data+="&_xsrf="+_xsrf
        }else{
            data._xsrf = _xsrf;
        }
        jQuery.ajax({
            url: url,
            data: data, 
            dataType: "json", 
            type: "POST",
            success: function(data, textStatus, jqXHR){
                if(data.login){
                    login()
                }else if(callback){
                    callback(data, textStatus, jqXHR)
                }
            }
        });
    },
/*
    getScript : function(url, callback, cache){
        jQuery.holdReady(false);
        jQuery.ajax({
           type: "GET",
           url: url,
           success: function(){
               jQuery.holdReady(false);
               callback&&callback();
           },
           dataType: "script",
           cache: cache||true
        })
    },
*/
    isotime : function(timestamp){
        var date = new Date(timestamp*1000),hour=date.getHours(),minute=date.getMinutes();
        if(hour<9){
            hour = "0"+hour
        }
        if(minute<9){
            minute = "0"+minute
        }
        return [
            date.getFullYear(), date.getMonth() + 1, date.getDate()
        ].join("-")+" "+[
            hour,minute 
        ].join(":") 
    },
    timeago : function(timestamp){
        var date = new Date(timestamp*1000);
        var ago = parseInt((new Date().getTime() - date.getTime())/1000);
        var minute;
        if(ago>-60&&ago<=0){
            return "刚刚"
        }else if(ago<60){
            return ago+"秒前"
        }else{
            minute = parseInt(ago/60)
            if(minute<60){
                return minute+"分钟前"
            }
        }
        return jQuery.isotime(timestamp)
    } 
})
})(jQuery);


function uuid(){
    return (""+ Math.random()).slice(2)
}

(function (){
var RE_CNCHAR = /[^\x00-\x80]/g;

function _cnenlen(str) {  
    if (typeof str == "undefined") {  
        return 0  
    }  
    var aMatch = str.match(RE_CNCHAR);  
    return (str.length + (!aMatch ? 0 : aMatch.length))  
} 
 
cnenlen = function(str) {  
        return Math.ceil(_cnenlen($.trim(str)) / 2)  
} 
})();

function fancybox_txt(tip, action, complete, post,  submit, can_post) {
    can_post = can_post|| function (txtlen, error, pop_txt){
        if(txtlen)return true; 
        error.html('请输入文字').fadeIn()
        pop_txt.focus()
    }
	var fancybox = $.fancybox;
	fancybox({
		'content': '<form method="POST" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip">　</div><div id="po_pop_main"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns"><span id="po_pop_error"></span><span class="btnw"><button type="submit">确认</button></span></div></form>',
		"onComplete": function() {
			$('.po_pop_tip').text(tip)
			var form = $('#po_pop_form'),
			pop_txt = $('#po_pop_txt').focus(),
			error = $('#po_pop_error');
            if(complete){
                complete = complete()           
            } 
            form.submit(function() {
                if(complete&&!complete()){
                    error.hide().fadeIn();
                    return false
                }
				var txt = $.trim(pop_txt.val());
				error.hide();


                if (
                    can_post(txt.length,error,pop_txt)
                ) {
					submit && submit()
					fancybox.showActivity()
					$.postJSON(
					action, {
						'txt': txt
					},
					post)
				} 
				return false
			})
		}
	})
}

function fancybox_word(title, path, finish, can_post){ 

	fancybox_txt(
        title, path,
        function(){
            return txt_maxlen(
                $("#po_pop_txt"), $('#po_pop_error'),  142
            )
        },
        function() {
            if(finish){
                if(typeof(finish)=="function"){
                    finish()
                }else{
                    $.fancybox({
                        'content': finish 
                    })
                    return
                }
            }
            $.fancybox.close() 	
        },
        0,
        can_post                    
    )
}

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

function fcm(id,count){
    var self = $('#fdtxt'+id), fcml='<div class="fcml" id="fcml_'+id+'"></div>';
    self.append('<div id="fcmpop_'+id+'" class="fcmpop"><textarea class="fcmtxt" id="txt_'+id+'"></textarea><div class="fcmbtn"><span class="txt_err L">先写点什么吧</span><span class="btnw"><button onclick="fcmcbtn('+id+')">提交</button></span></div></div>')
    var self_a = self.parent().find($(".comment_a")).hide(),fcmtxt=self.find('.fcmtxt');
    self_a.replaceWith('<a id="close_a_'+id+'" href="javascript:fcmc('+id+','+count+');void(0)">收起</a>')
    if(count){
        fcmtxt.before('<div class="fcmload"></div>')
        var data = {"comments":[{"username":"realfex","link":"http://realfex.42qu.com","content":"楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了"},{"username":"realfex","link":"http://realfex.42qu.com","content":"楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了楼主牛逼,顶死你..可能加快农机空间克隆就能看见了空间看了"}]}
        self.find($('.fcmload')).replaceWith(fcml)
        for(i=0;i<data.comments.length;i++){
            var html = '<div class="fcmi"><a class="c9" href="'+data.comments[i].link+'">'+data.comments[i].username+'</a><a href="javascript:void(0)" rel="'+data.comments[i].username+'" class="reply_at"></a><pre>'+data.comments[i].content+'</pre></div>'
                $('#fcml_'+id).append(html)
        }
        $('#fcml_'+id).slideDown(function(){$(this).show()})
    }else{
        fcmtxt.before(fcml)
    }
    self.find('textarea').focus()
}

function fcmc(id,count){
    $('#fcml_'+id).slideUp(function(){$('#fcmpop_'+id).remove();$('#close_a_'+id).replaceWith('<a href="javascript:fcm('+id+','+count+');void(0)" class="comment_a"><span class="mr3">'+count+'</span>评论</a>')})
}
function fcmcbtn(id){
    var cont = $('#txt_'+id).val()
    if($.trim(cont)==''){
        var err = $('.txt_err')
        err.fadeOut(function(){err.fadeIn()})
        return false
    }
    var my = $('<div class="fcmi" style="display:none;"><span class="L c9">我</span><pre>'+cont+'</pre></div>')
    $('#fcml_'+id).append(my)
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
