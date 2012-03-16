
function feedrecx(){
    $("#rowrec").hide()
}

/*
61 word
62 note
*/
$(".bzlive").live("click",function(){
    $(this.parentNode).find(".buzz_x")[0].visited = 1;
    var self = $(this);

    popreply(
        self.parents('.buzz_box')[0].id.slice(9), 
        self.html(),
        this.href
    )
    self.css({color:"#99a"});
    return false
})
;(function() {
    b1024()
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
                    rter={};
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
                    t.rter=[];
                    for(j in rter){
                        t.rter.push([j,rter[j][0]]);
                    }
                    t.has_rter = t.rter.length;
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
            t.tag_list = t.tag_list||[]
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
            picwall_render()
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
        $("#po_word_txt").ctrl_enter( function(){$(".say_btn").click()});
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
/*    
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
*/

    $(".buzz_win_book").isotope({ itemSelector : '.sdw' });
    
    autocomplete_tag_hero("#search")

})()




$(".buzz_x").live("click", function(){
    var id=this.rel, buzz=$("#buzz"+id), box=buzz.parents('.buzz_box')
    if(box.find(".buzz_x").length<=1){
        box.remove()
    }else{
        buzz.hide(buzz.remove);
    }
    if(!this.visited){
        $.postJSON( '/j/buzz/'+box[0].id.slice(9)+'/x/'+id)
    }

})
$(".buzzX").click(function(){
    var rel=this.rel
    if(rel){
        $.postJSON( '/j/buzz/'+rel+"/x")
    }
    $(this).parents('.buzz_box').hide() 
})

$.template(
    'side_pic',
    '<div class="side_pic_wrap">'+
        '<div class="side_pic_main">'+
            '<img width="226" class="side_pic_img" src="http://${$data[6]}/721/342/${$data[7]}.jpg" />'+
            '<div class="side_pic_content">'+
                '<a class="TPH c9" href="http://${$data[0]}${HOST_SUFFIX}" target="_blank">${$data[1]}</a> : ${$data[4]}'+
            '</div>'+
        '</div>'+
        '<div class="side_pic_opt">'+
            '<a class="side_pic_a" href="javascript:fcm(${$data[0]},${$data[5]});void(0)">评论</a>'+
            '<a class="side_pic_a" href="javascript:void(0)">收藏</a>'+
         '<a class="side_pic_a" href="javascript:share(${$data[0]});void(0)">推荐</a>'+
        '</div>'+
    '</div>'
);

(function(){

var PICWALL_BUFF = []

function picwall_get(){
    if(PICWALL_BUFF.length)return PICWALL_BUFF.shift()
    $.getJSON(
        '/j/feed/pic',
        function(result){
            PICWALL_BUFF = result
            if(PICWALL_BUFF.length){
                picwall_render()
            }
        }
    ) 
}

function picwall_break(pic){
    var ctrl = false,
    buzz_height = $('#buzz_win_reply').height() + $('#buzz_win_at').height()
    if(($('#picwall').height()+buzz_height+200>$('#feeds').height()) || !pic){
        ctrl = true
    }
    return ctrl
}

picwall_render = function(){
    while(1){
        pic = picwall_get()
        if(picwall_break(pic))break;
        $('#picwall').append($.tmpl('side_pic',[pic]))
    }
}
})();

$('.side_pic_img').live('click',function(){
    var self = $(this),
        hei = $(window).height(),
        fancybox = $.fancybox
    
    fancybox.showActivity()
    fancybox({
        'content':'<img src='+self.attr('src')+' style="max-height:'+(Number(hei)-90)+'px;"/>'
    })
})

