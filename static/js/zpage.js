HOST_SUFFIX=location.host.slice(location.host.indexOf("."));
HOST = HOST_SUFFIX.slice(1);

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
                if(data&&data.login){
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
        var result = [ date.getMonth() + 1, date.getDate() ], now = new Date(), full_year=date.getFullYear();
        if(now.getFullYear()!=full_year){
            result.unshift(full_year)
        } 
        return result.join("-")+" "+[ hour,minute ].join(":") 
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
    },
/*,
    getCss: function(url){
        $("head").append($('<link type="text/css" rel="stylesheet"/>').attr('href',url));
    }
*/

    toJSON : function( o ) {

        if ( o === null ) {
            return 'null';
        }

        var type = typeof o;

        if ( type === 'undefined' ) {
            return undefined;
        }
        if ( type === 'number' || type === 'boolean' ) {
            return '' + o;
        }
        if ( type === 'string') {
            return $.quoteString( o );
        }
        if ( type === 'object' ) {
            if ( typeof o.toJSON === 'function' ) {
                return $.toJSON( o.toJSON() );
            }
            if ( o.constructor === Date ) {
                var month = o.getUTCMonth() + 1,
                    day = o.getUTCDate(),
                    year = o.getUTCFullYear(),
                    hours = o.getUTCHours(),
                    minutes = o.getUTCMinutes(),
                    seconds = o.getUTCSeconds(),
                    milli = o.getUTCMilliseconds();

                if ( month < 10 ) {
                    month = '0' + month;
                }
                if ( day < 10 ) {
                    day = '0' + day;
                }
                if ( hours < 10 ) {
                    hours = '0' + hours;
                }
                if ( minutes < 10 ) {
                    minutes = '0' + minutes;
                }
                if ( seconds < 10 ) {
                    seconds = '0' + seconds;
                }
                if ( milli < 100 ) {
                    milli = '0' + milli;
                }
                if ( milli < 10 ) {
                    milli = '0' + milli;
                }
                return '"' + year + '-' + month + '-' + day + 'T' +
                    hours + ':' + minutes + ':' + seconds +
                    '.' + milli + 'Z"';
            }
            if ( o.constructor === Array ) {
                var ret = [];
                for ( var i = 0; i < o.length; i++ ) {
                    ret.push( $.toJSON( o[i] ) || 'null' );
                }
                return '[' + ret.join(',') + ']';
            }
            var name,
                val,
                pairs = [];
            for ( var k in o ) {
                type = typeof k;
                if ( type === 'number' ) {
                    name = '"' + k + '"';
                } else if (type === 'string') {
                    name = $.quoteString(k);
                } else {
                    // Keys must be numerical or string. Skip others
                    continue;
                }
                type = typeof o[k];

                if ( type === 'function' || type === 'undefined' ) {
                    // Invalid values like these return undefined
                    // from toJSON, however those object members
                    // shouldn't be included in the JSON string at all.
                    continue;
                }
                val = $.toJSON( o[k] );
                pairs.push( name + ':' + val );
            }
            return '{' + pairs.join( ',' ) + '}';
        }
    },

    /**
     * jQuery.quoteString
     * Returns a string-repr of a string, escaping quotes intelligently.
     * Mostly a support function for toJSON.
     * Examples:
     * >>> jQuery.quoteString('apple')
     * "apple"
     *
     * >>> jQuery.quoteString('"Where are we going?", she asked.')
     * "\"Where are we going?\", she asked."
     */
    quoteString :  function( string ) {
        return '"' + string.replace(/\\/g, "\\\\")
                          .replace(/\n/g, "\\n")
                          .replace(/"/g, '\\"')
                          .replace(/\r/g, "\\r")
                          .replace(/\t/g, "\\t")
                          .replace(/\f/g, "\\f") + '"';
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
		'content': '<form method="POST" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip"></div><div id="po_pop_main"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns"><span id="po_pop_error"></span><span class="btnw"><button type="submit">确认</button></span></div></form>',
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
        codesh()
    })
}



function doc_height(){
    return document.documentElement.clientHeight ? document.documentElement.clientHeight : document.body.clientHeight
}

var TMPL_REPLY;

function render_reply(data, begin){
    TMPL_REPLY = TMPL_REPLY||$('<script type="text/x-jquery-tmpl"><div class="fcmi">{{if $data[3]}}<a target="_blank" href="//${$data[0]}'+HOST_SUFFIX+'" ><img class="fcico" src="${$data[3]}"></a>{{else}}<div class="fcico"></div>{{/if}}<div class="fcrb">{{each $data[4]}}<pre class="fcpre fcpre${$index}">{{html $value[0]}}{{if $value[2]}}<a href="javascript:void(0)" rel="${$value[3]}" class="rm"></a>{{/if}}</pre>{{/each}}<div class="fcname"><a href="//${$data[0]}'+HOST_SUFFIX+'" class="fcmname c9 TPH" target="_blank"><span>${$data[1]}</span>{{if $data[2]}} ( ${$data[2]} ){{/if}}</a><a class="zsite_reply reply_at" rel="${$data[0]}" href="javascript:void(0)"></a></div></div></div></script>');
    var d4, j, k, t, result, i=0;
    begin = begin||0
    for(;i<data.length;++i){
        d4=data[i][4]
        for(j=0;j<d4.length;++j){
            k = d4[j]
            t = k[1]
            if(i>=begin){
                t = "reply/"+t
            }
            k.push(t)
        }
    }
    var result = TMPL_REPLY.tmpl(data);

    result.find(".rm").click(function(){
        if(confirm("删除 , 确定 ?")){
            var fcmi = $(this).parents('.fcmi'),fcpre=$(this).parents('.fcpre');
            ((fcmi.find('.fcpre').length>1)?fcpre:fcmi).fadeOut(function(){fcpre.remove()});
            $.postJSON("/po/rm/"+this.rel)
        }
        return false
    })
    return result
}
(function(){
var doc=$(document), h=doc_height();
fcm = function (id,count){
    if(!$('#fcmpop_'+id)[0]){
        var self = $('#fdtxt'+id), fcml='<div class="fcml" id="fcml_'+id+'"></div>', self_parent=self.parent(), fcmload=$('<div class="fcmload"/>');
        self_parent.find('.fdbar').before('<div id="fcmpop_'+id+'" class="fcmpop"><div class="fcmtxt"><textarea class="txta" id="txt_'+id+'"></textarea></div><div class="fcmbtn"><a href="/'+id+'" target="_blank" class="fcm2">链接</a><span class="btnw"><button onclick="fcmcbtn('+id+')">回复</button></span></div></div>')
        var self_a = self_parent.find($(".fcma")).hide(),fcmtxt=self_parent.find('.fcmtxt');
        self_a.replaceWith('<a id="fcmx_'+id+'" href="javascript:fcmc('+id+','+count+');void(0)">收起</a>')
        if(count){
            fcmtxt.before(fcmload)
            $.postJSON(
            "/j/po/reply/json/"+id,
            function(data){
/*
                for(i=0;i<data.length;i++){
                    t=data[i]
                    html = $('<div class="fcmi"><a target="_blank" class="fcmname c9 TPH" href="//'+t[0]+HOST_SUFFIX+'"></a><a href="javascript:void(0)" rel="'+t[0]+'" class="reply_at"></a><pre>'+t[1]+'</pre></div>')
                    $('#fcml_'+id).append(html)
                    html.find(".fcmname").text(t[2])
                }
*/
                fcml = $(fcml)
                fcmload.replaceWith(fcml)
                fcml.append(render_reply(data)) ; codesh();
                fcml.slideDown(function(){fcml.show()})

                var e = $('#txt_'+id)
                if(e.offset().top-doc.scrollTop()>h){
                    doc.scrollTop(fcml.offset().top-50)             
                }
                
            })
        }else{
            fcmtxt.before(fcml)
        }
        $("#txt_"+id).pop_at("/j/at/reply/"+id)
        self_parent.find('textarea').focus().elastic()
        button = self_parent.find('button')
        $("#txt_"+id).ctrl_enter( function(){ button.click()});
    }
}

function scrolls(id){
    doc.scrollTop(
        $('#fdtxt'+id).height()>doc_height()-250?  $('#fcml_'+id).offset().top-250:$('#fdtxt'+id).offset().top-80
    )
}

fcmc = function (id,count){
    scrolls(id)
    $('#fcml_'+id).hide()
    $('#fcmpop_'+id).remove();
    $('#fcmx_'+id).replaceWith('<a href="javascript:fcm('+id+','+count+');void(0)" class="fcma"><span class="mr3">'+count+'</span>评论</a>')
}
fcmcbtn = function  (id){
    var textarea=$('#txt_'+id) , 
        cont = textarea.val(),
        fcmload=$('<div class="fcmload"/>');

    if(!cont.length){
        return;
    }
    $('#fcml_'+id).append(fcmload)
    textarea.focus().val('').height(80)
    post_reply(id, cont, function(r){
            fcmload.replaceWith(render_reply(r)) ; 
            codesh()

    })
}
$(".reply_at").live("click", function(){
    var self=$(this),
        txt= self.parents('.fcmpop').find('textarea').focus(),
        val=txt.val(),
        name=$(this.previousSibling).find('span').text(),
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

function post_reply(id, txt ,recall){
    $.postJSON(
        '/j/po/reply/'+id,
        {
            "txt":txt
        },function(r){
            if(r.can_not_reply){
                $.fancybox({
                    content: CANNOT_REPLY
                })
                return
            } 
            recall && recall(r); 
        }
    )
}

function nav2_touch(){
    if(!islogin())return;
    var html = $('html,body'),
        e=$("#nav2_touch").blur(),  
        drop = $('#nav2drop');

        function _() {
            drop.hide()
            html.unbind('click', _)
        }

        if (drop.is(":hidden")) {
            drop.show()
            html.click(_)
            clicked = true;
        } else {
            _()
        }
};
function init_say(){
    document.write('<div class="say"><div class="say_txt">现在 ,  想说什么?</div></div><div class="pop_say"><textarea class="pop_txt"></textarea><div class="pop_banner"><a class="pop_submit" href="javascript:post_say();void(0)">发表</a><div class="pop_tip"></div><a class="pop_close" href="javascript:close_pop();void(0)"></a></div></div>')
    $(function(){
        var say = $('.say')
        var pop_say = $(".pop_say")
        var txt = $('.say_txt')
        var pop_txt = $('.pop_txt')
        var txt_tip = txt.text()
        var  pop_tip = $('.pop_tip') 
        
        can_say = txt_maxlen(pop_txt,pop_tip,142)

        txt.click(function(){
            if(pop_say.is(":hidden")){
                pop_say.show();
                pop_say.css("marginTop",0).css("marginTop",Math.max(txt.offset().top-pop_say.offset().top-98,-62))
                pop_txt.focus()
            }  
        })
        
        close_pop = function (){
            var cont = $('.pop_txt').val()
            pop_say.hide()
            if($.trim(cont)=='') txt.text(txt_tip)
            else txt.text(cont)
        }


        post_say = function (){
            if(!can_say()){
                pop_tip.fadeOut(function(){pop_tip.fadeIn()})
                return false
            }
            var val=pop_txt.val()
            pop_txt.attr('disabled',true)
            pop_tip.replaceWith('<div class="say_loading pop_tip"></div>')
            $('.pop_close,.pop_submit').hide()
            $.postJSON(
                '/j/po/word',
                {
                    "txt":val
                },
                function(){
                    $('.pop_tip').replaceWith('<div class="pop_ok pop_tip">发表成功</div>')
                    var pop_ok = $('.pop_ok')  
                    pop_ok.fadeIn(function(){
                        location="/word"
                    })
                }
            )
        }
    })
}

(function(){
    var tt;
    function pop_hero(elem){
        var pop_hero_remove = function(){$('.pop_hero').remove()}
        elem.live('mouseenter',function(e){
            var self = $(this)
            tt=setTimeout(function(){
            if($('.pop_hero')[0]) pop_hero_remove()
            clearTimeout(tt)
            var href = self.attr('href')
            $.getJSON(
            '/j/hero/'+href.slice(href.indexOf('\/\/')+2).split('.')[0],
            function(result){
                if(!result)return;
                if(!$('.pop_hero')[0]){
                        var pop = $('<div class="pop_hero"><div class="pop_hero_to"></div><div class="pop_hero_banner"><a href="'+result[3]+'" target="_blank"><img class="pop_hero_avatar" src="'+result[2]+'"></a><a href="javascript:follow_a('+result[4]+');void(0)" id="follow_a'+result[4]+'" class="xa pop_hero_follow">'+result[5]+'</a></div><div class="pop_hero_txt"><a href="'+result[3]+'" target="_blank" class="pop_hero_name"></a><div class="pop_hero_bio"></div><div class="pop_hero_motto"></div></div>')

                        pop.find('.pop_hero_bio').text(result[1])
                        pop.find('.pop_hero_motto').text(result[6])
                        pop.find('.pop_hero_name').text(result[0])

                        $('body').prepend(pop)
                       
                        var left = 30,base_left=self.offset().left;
                        if(base_left*1.5>$('body').width()){ 
                            left = pop.width()-50;
                            pop.addClass("pop_heroR")
                            pop.find('.pop_hero_to').css('marginLeft',IE6?left-62:left)
                        }
                        pop.offset({top:self.offset().top-126,left:base_left-left}).mouseleave(
                                pop_hero_remove
                        ).mouseenter(
                            function(){
                                clearTimeout(tt)
                            }
                        )
                    }
                })
            },200)
        }).live('mouseout',function(){
            clearTimeout(tt)
            tt=setTimeout(pop_hero_remove,200)
        })
            
    }
    pop_hero($('.TPH'))
})()

function auto_add(item,toadd,wrap,close,act){
    var wrap = $('.'+wrap)
    $('.'+item+':last').live(act,function(){
        wrap.append(toadd)
    })
    if(close!=''){
        $('.'+close).live('click',function(){
            $(this).parent().remove()
            if(!wrap.children()[0]){
                wrap.append(toadd)
            }
        })
    }
}

$(function(){
    if(!('placeholder' in document.createElement('input'))){
        $('[placeholder]').addPlaceholder()
    }
})

var _CODESH;
function codesh(){
    if(IE6)return;
    if($(".codebrush")[0]){
        if(_CODESH){
            SyntaxHighlighter.highlight();
        }else{
            $.ajax({
                url: "http://0.42qu.us/SyntaxHighlighter/sh.js",
                dataType: "script",
                cache: true
            })
            _CODESH=1
        }
    }
}

function fdvideo(e){
    var content = $('<embed align="middle" wmode="Opaque" type="application/x-shockwave-flash" allowscriptaccess="sameDomain" allowfullscreen="true" class="video" quality="high" src="'+e.href+'">'),
        win = $(window),
        width = win.width()-120,
        height = win.height()-90,
        mwidth = height*16/9;

    if(width<mwidth){
        height=width*9/16
    }else{
        width=mwidth
    }
    content.height(height).width(width);

    $.fancybox({content:content,hideOnOverlayClick:false});

    return false
}

RegExp.escape = function(text) {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
}

function scroll_to_fixed(id, size, style1, style2){
    if(!IE6){
        var elem = $(id), fix_css=elem[0].id+"_fix"
        if(elem[0]){
            elem.css('position','absolute')
            var wrap = elem.parent(),wraptop = wrap.offset().top,
            top = elem.offset().top, win=$(window).scroll(function() {
                var scroll = win.scrollTop(),
                limit =  wraptop + wrap.height()
                if((scroll >= top+size) && (scroll<limit-80)){
                    elem.css(style1)
                    elem.addClass(fix_css)
                }else{
                    elem.css(style2)
                    elem.removeClass(fix_css)
                }
            })
        }
    }
}

function star_fav(id,type){
    if(!islogin())return;
    var num,url
    if(type===0){
        num = 1
        url = ''
    }else{
        num = 0
        url = 'rm/'
    }
    $.postJSON(
        '/j/fav/' + url + id,
        function(){
            $("#star_fav"+id).attr('class','sitefav'+num).attr('href','javascript:star_fav('+id+','+num+');void(0)')
        }
    )
}

