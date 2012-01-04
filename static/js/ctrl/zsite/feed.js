
/*
61 word
62 note
*/
$(".buzz_li").live("click",function(){
    $(this.parentNode).find(".buzz_x")[0].visited = 1;
    var content = $(
'<div class="fcmpop" id="reply_reply_pop"><a target="_blank" id="reply_name"></a><div id="reply_reply_body" class="reply_reply_loading"></div><textarea></textarea><div class="tr"><span class="btnw"><button type="submit" class="button">回复</button></span></div></div>'
    ), self = $(this), 
    href = this.href, 
    cbody = content.find('#reply_reply_body'), t=cbody[0],
    textarea = content.find('textarea'),
    fancybox = $.fancybox,
    id = href.split("/")[4].split("#")[0];

    self.css({color:"#99a"});

    content.find('#reply_name').html(self.html()).attr('href',href)
    content.find('button').click(function(){
        post_reply(id, textarea.val(),function(data){
            textarea.val('')
            textarea.focus()
            _(data)
        })
    })
    function _(data){
        cbody.removeClass('reply_reply_loading').append(render_reply(data))
        codesh()
        var height = t.scrollHeight+2, 
            winheight=$(window).height() - 260;

        if(height>winheight){
            height = winheight;
        }else{
            cbody.css("padding","0")
        }

        cbody.css({
            height:height
        })
        t.scrollTop=t.scrollHeight-t.offsetHeight-5

        fancybox.resize()

    }
    fancybox({
        content:content, 
        onComplete:function(){
            textarea.focus()
            $.getJSON( '/j/po/reply/json/'+id, _)
        }
    })
    return false

})

;(function() {
    function winresize(){
        var body=$("#B")
        if(body.width() < 1024){
            body.addClass('b1024') 
        }else{
            body.removeClass('b1024')
        }
    }
    winresize()
    $(window).resize(winresize)

    /*消息流*/
	var feed_loader = feed_load_maker( "id rt_list"),
	DATE_ATTR = "zsite_cid zsite_name zsite_link unit title pic".split(' ');

	function array2zsite(a) {
		return {
			name: a[0],
            link:a[1],
            txt: a[3]
		}
	}

	function init(result, site_dict) {
		var data = {
			"item": []
		},
		i = 0,
		j,
		attr,
		item = result[6],
		t,
		rt_list,
        site_id,
        rter,
        exist_rter;

		for (; i < DATE_ATTR.length; ++i) {
			data[DATE_ATTR[i]] = result[i]
		}


		for (i = 0; i < item.length; ++i) {
            t = feed_loader(item[i]);

			rt_list = t.rt_list;
			if (rt_list.length) {
				if (! (rt_list.length == 1 && rt_list[0][0] == 0)) {
					t.rt_list = []
					for (j = 0; j < rt_list.length; ++j) {
						if (rt_list[j][0]) {
							t.rt_list.push(rt_list[j])
						}
					}
                    t.rter=rter={};
                    exist_rter={};
					t.rt_list = $.map(t.rt_list, array2zsite);
                    for(j=0;j<rt_list.length;j++)
                    {
                        var rter_id=rt_list[j][1]
                        if(rt_list[j][3][1]==''&&!exist_rter[rter_id]&&rt_list[j][2]!=0){
                            rter[rter_id]=[rt_list[j][0],rt_list[j][2]];
                        }else{
                            delete rter[rter_id]
                            exist_rter[rter_id] = 1
                        }
                    }
                    t.rtL=rtL=[];
                    t.rtC=rtC=0;
                    for(j in rter){
                        t.has_rter = 1;
                        rtC++;
                        rtL.push([j,rter[j]]);
                    }
                } else {
                        t.rt_list = [0]
                }
			}

			t.create_time = $.timeago(t.create_time);
            
            site_id = t.site_id;
            if(site_id){
                t.site_name = site_dict[site_id];
                t.site_url = site_id+HOST_SUFFIX
            }
			data.item.push(t)	
		}
		return data
	}

	function init_result(result) {
		var site_dict = result.pop(),
        length = result.length,
		item = [],
		i = 0,
		data,
		pre_zsite_id;

		for (; i < length; ++i) {
			data = init(result[i], site_dict)
			if (data.zsite_id == pre_zsite_id) {
				data.zsite_same_as_pre = true
			} else {
				pre_zsite_id = data.zsite_id
			}
			item.push(data)
		}
        
		return item
	}
    feed_page(
        "/j/feed/", "#feeds" , init_result, function(){
			var prebottom, top, diff, self;
			$("#feeds .G3").each(function() {
				self = $(this)
				top = self.offset().top;
				if (self.hasClass('G3_AS_PRE') && prebottom !== undefined) {
					diff = prebottom - top
					if (diff) {
						this.style.marginTop = diff + "px"
					}
				}
				prebottom = self.offset().top + this.offsetHeight;
			})
        }
    )

	/* 发微博 */
	var po_word_txt = $("#po_word_txt"),
	po_word_txt_bg = "po_word_txt_bg",
    txt_tip=$("#txt_tip"),
    saying=$('<div id="saying"></div>'),
    po_word_form=$('#po_word_form').submit(
        function(){
            if(can_say()){
                var val = po_word_txt.val(); 
                if($.trim(val)=='')return false;
                txt_tip.html('')
                say_btn.hide().after(saying)

                $.postJSON(
                    '/j/po/word',
                    {
                        txt:val
                    },
                    function(result){
                        if(result){
                            $('#feed').tmpl(init_result(result)).prependTo("#feeds")
                        }
                        po_word_txt.val('').attr(
                            "class","po_word_txt po_word_txt_sayed"
                        ).removeAttr('disabled')
                        say_btn.show();
                        saying.remove() 
                    }
                )
            } else{
                txt_tip.fadeOut(function(){txt_tip.fadeIn()})
            }
            return false
        }),
    say_btn = $(".say_btn").click(
        function(){
            po_word_form.submit()
        });
    
    $(function(){
        keyboard_shortcut(
            $("#po_word_txt"),
            function(){$(".say_btn").trigger("click")}
            );
    })


    txt_tip.html('Ctrl + Enter 直接发布')
	po_word_txt.blur().val('').focus(function() {
        txt_tip.show()
		this.className="po_word_txt"
	}).blur(function() {
		var self = $(this),
		val = self.val();
		if (!val || ! val.length) {
			self.addClass(po_word_txt_bg)
		}
	}).addClass(po_word_txt_bg).click(
    function(){
        po_word_txt.animate({"height":"78px"},"fast");
    }).blur(function(){
        if(po_word_txt.val()==''){
            txt_tip.html('Ctrl + Enter 直接发布')
            po_word_txt.animate({"height":"44px"},"fast");
            txt_tip.hide();
        }
    }).pop_at("/j/at")
    ;
    
    var can_say = txt_maxlen(
        po_word_txt, 
        txt_tip, 
        142
    )

    /* 站点推荐 */
    
    $(".site_li").hover(
        function(r){
            $(this).find(".delbtn")
                   .addClass("show_x")
        },
        function(r){
            $(this).find(".delbtn")
                   .removeClass("show_x")
        }
    );
    
    $(".site_fav_a").click(function(){
        $(this).addClass("fav_loading");
    });

})()






$(".buzz_x").live("click", function(){
    var id=this.rel, buzz=$("#buzz"+id)
    if($("#buzz_win_reply .buzz_li").length<=1){
        $("#buzz_win_reply").hide()
    }else{
        buzz.hide(buzz.remove);
    }
    if(!this.visited){
        $.postJSON( '/j/buzz/reply/x/'+id)
    }

})
$(".buzzX").click(function(){
    var rel=this.rel
    if(rel){
        $.postJSON( '/j/buzz/'+rel+"/x")
    }
    $(this).parents('.buzz_box').hide() 
})
;$(function(){

    var data = $.parseJSON($("#site_data").html()),
        rec_wrapper=$("#rec_wrapper"),
        site_rec=$("#site_rec");

    function addRec(){
        if(data&&data.length){
            site = data.pop();
            rec_wrapper.append(site_rec.tmpl());

            rec_wrapper.show();
            $("#rec_"+ site[0]).hide().show("slow");
            $("#rec_title").show();

        }
        if(!rec_wrapper.find("").html()){
            $("#rec_title").hide("fast");
            rec_wrapper.hide("fast");
        }
    }
    addRec();
/*

    function loadrec(id){
        $.postJSON("/j/site/rec/new",{},function(r){
            if(r!='')
        {
            site={
                "id":r[0],
            "link":r[1],
            "name":r[2],
            "ico":r[3],
            "motto":r[4]
            };
            $("#site_rec").tmpl(site).appendTo("#rec_wrapper");
            refreshState();
        }
        });
    }

    function _(id, state, callback){
        $.postJSON( '/j/site/rec/'+id+'-'+state,{},function(r)
                {
                    callback&&callback();
                }
                )
    }

    del=function(r){
        i = $('#rec_'+r);
        i.hide("slow",addRec);
        callback=function(){
            loadrec(0);
        };
        _(r, 1,callback);
    };

    fav=function(id){
        $("#rec_id"+id).addClass("fav_loading");
        callback=function(){
            $("#rec_id"+id).removeClass("fav_loading");
            $("#rec_id"+id).addClass("site_faved");
            $("#rec_id"+id).attr("href","javascript:unfav("+id+")");
        };
        _(id, 2,callback);
    }

    unfav=function(id){
        callback=function(){};
        _(id, 0,callback);
        $("#rec_id"+id).removeClass("site_faved");
        $("#rec_id"+id).attr("href","javascript:fav("+id+")");
    }
    $(".buzz_h1").hover(function(){$(this).find("a").show()},function(){$(this).find("a").hide()});
    $(".buzz_w").hover(function(){$(this).find('.bzr').show()},function(){$(this).find(".bzr").hide()});
*/
});
