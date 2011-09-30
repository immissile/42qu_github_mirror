HOST_SUFFIX=location.host.slice(location.host.indexOf("."));

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
        all.remove()
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


(function(){
var doc=$(document);

fcm = function (id,count){
    var self = $('#fdtxt'+id), fcml='<div class="fcml" id="fcml_'+id+'"></div>',t,html;
    self.append('<div id="fcmpop_'+id+'" class="fcmpop"><textarea class="fcmtxt" id="txt_'+id+'"></textarea><div class="fcmbtn"><a href="/'+id+'" target="_blank" class="fcm2">链接</a><span class="btnw"><button onclick="fcmcbtn('+id+')">回复</button></span></div></div>')
    var self_a = self.parent().find($(".fcma")).hide(),fcmtxt=self.find('.fcmtxt');
    self_a.replaceWith('<a id="fcmx_'+id+'" href="javascript:fcmc('+id+','+count+');void(0)">收起</a>')
    if(count){
        fcmtxt.before('<div class="fcmload"></div>')
        $.postJSON(
        "/j/po/reply/json/"+id,
        function(data){
            self.find($('.fcmload')).replaceWith(fcml)
            for(i=0;i<data.length;i++){
                t=data[i]
                html = $('<div class="fcmi"><a target="_blank" class="fcmname c9" href="//'+t[0]+HOST_SUFFIX+'"></a><a href="javascript:void(0)" rel="'+t[0]+'" class="reply_at"></a><pre>'+t[1]+'</pre></div>')
                $('#fcml_'+id).append(html)
                html.find(".fcmname").text(t[2])
            }
            $('#fcml_'+id).slideDown(function(){$(this).show()})
            var e = $('#txt_'+id)
            h = document.documentElement.clientHeight ? document.documentElement.clientHeight : document.body.clientHeight
            if(e.offset().top-doc.scrollTop()>h){
                scrolls(id)             
            } 
        })
    }else{
        fcmtxt.before(fcml)
    }
    self.find('textarea').focus().elastic()
}

function scrolls(id){
    doc.scrollTop(
        $('#fdtxt'+id).height()>h-250?  $('#fcml_'+id).offset().top-250:$('#fdtxt'+id).offset().top-80
    )
}

fcmc = function (id,count){
    scrolls(id)
    $('#fcml_'+id).hide()
    $('#fcmpop_'+id).remove();
    $('#fcmx_'+id).replaceWith('<a href="javascript:fcm('+id+','+count+');void(0)" class="fcma"><span class="mr3">'+count+'</span>评论</a>')
}
fcmcbtn = function (id){
    var textarea=$('#txt_'+id) , cont = textarea.val()
    var my = $('<div class="fcmi" ><div class="c9">我</div><pre></pre></div>')
    if(!cont.length){
        return;
    }

    $.postJSON(
        '/j/po/reply/'+id,
        {
            "txt":cont
        },function(r){
            if(r.can_not_reply){
                $.fancybox({
                    content: CANNOT_REPLY
                })
            } 
            textarea.focus().val('').height(100)
            my.find('pre').text(cont)
            $('#fcml_'+id).append(my)
    
        }
    )
}
$("#feeds .reply_at").live("click", function(){
    var self=$(this),
        txt= self.parents('.fcmpop').find('textarea').focus(),
        val=txt.val(),
        name=$(this.previousSibling).text(),
        add;

    add =  "@"+name+'('+this.rel+') '
    if(val.length){
        if($.trim(val)==val){
            val+=" "
        }
        val+=add;
    }else val=add;

    txt.val(val)
})
})()
