/*
61 word
62 note
*/

(function (){
var FEED_ATTR_BASE = "id rt_list cid rid reply_count create_time name vote txt txt_more vote_state",
    FEED_ATTR_TXT_BASE = FEED_ATTR_BASE+" tag_id tag_name",
    QUESTION_ATTR_BASE = " question_id question_user question_user_link",
    FEED_ATTR = {
        61:FEED_ATTR_BASE+QUESTION_ATTR_BASE,
        62:FEED_ATTR_TXT_BASE,
        63:FEED_ATTR_TXT_BASE,
        64:FEED_ATTR_TXT_BASE+QUESTION_ATTR_BASE,
        65:FEED_ATTR_TXT_BASE,
        66:FEED_ATTR_TXT_BASE,
        67:FEED_ATTR_TXT_BASE,
        68:FEED_ATTR_BASE+" place_name address time_row1 time_row2 time_diff_day",
        69:FEED_ATTR_BASE
    },
    DATE_ATTR = "name link unit title pic".split(' ');
    for(var i in FEED_ATTR){
        FEED_ATTR[i]=(
            FEED_ATTR[i]+""
        ).split(' ')
    }

    function array2zsite(a){
        return {
            name: a[0],
            link: a[1]
        } 
    }

    function init(result){
        var data = {
            "item":[]
        },
        i=0,
        j,
        attr,
        item=result[5],
        t,
        rt_list;
        for(;i<DATE_ATTR.length;++i){
            data[DATE_ATTR[i]]=result[i]
        }
        for(i=0;i<item.length;++i){
            result=item[i];
            t={
            };
            attr=FEED_ATTR[result[2]];
            result_length = result.length;
            for(j=0;j<result_length;++j){
                t[attr[j]] = result[j]
            }
            rt_list = t.rt_list;
            if(rt_list.length){
                if(!(rt_list.length==1&&rt_list[0][0]==0)){
                    t.rt_list = []
                    for(j=0;j<rt_list.length;++j){
                        if(rt_list[j][0]){
                            t.rt_list.push(rt_list[j])
                        }
                    }
                    t.rt_list = $.map(t.rt_list, array2zsite);
                }else{
                    t.rt_list = [0]
                }
            }


            t.create_time = $.timeago(t.create_time);
            data.item.push(t)
            //console.info(t)
        }
    
        return data
    }

    function init_result(result){
        var length = result.length, item=[], i=0, data, pre_zsite_id;

        for(;i<length;++i){
            data = init(result[i])
            if(data.zsite_id == pre_zsite_id){
                data.zsite_same_as_pre = true
            }else{
                pre_zsite_id = data.zsite_id
            }
            item.push(data)
        }
        return item 
    }

    var feed_load=$("#feed_load").click(function(){
        render_feed()
        feed_load.hide()
        autocount=0;
    }), feed_loading=$("#feed_loading"), begin_id = $("#begin_id").val(0),is_loading=0, autocount=0;
    function render_feed(){
        if(is_loading)return;
        is_loading = 1;
        feed_load.hide()
        feed_loading.show()
        $.postJSON(
        "/j/feed/"+begin_id.val(),
        function(result){
            if(result.length==1){
                feed_load.hide()
                feed_loading.hide()
                return
            }
            is_loading=0;
            begin_id.val(
                result.pop()
            )
            $('#feed').tmpl(init_result(result)).appendTo("#feeds");
            feed_loading.slideUp(function(){
                feed_load.show()
            });
            //console.info(result.length)

            var prebottom,top,diff,self;
            $("#feeds .G3").each(function(){
                self=$(this)
                top=self.offset().top;
                if(self.hasClass('G3_AS_PRE')&&prebottom!==undefined){
                    diff=prebottom-top
                    if(diff){
                        this.style.marginTop=diff+"px"
                    }
                }
                prebottom = self.offset().top+this.offsetHeight;
            })



        })
    }
    render_feed()
    var win = $(window)
    win.scroll(function() {
        if (
           autocount < 5 && !is_loading && win.scrollTop() > ($(document).height() - win.height() * 2)
        ){
            autocount += 1;
            render_feed();
        }

    });
    /* 发微博 */
    var  po_word_txt = $("#po_word_txt"), po_word_txt_bg="po_word_txt_bg";
    po_word_txt.blur().val('').focus(function(){
        $(this).removeClass(po_word_txt_bg)
    }).blur(function(){
        var self=$(this), val=self.val();
        if(!val||!val.length){
            self.addClass(po_word_txt_bg)
        }
    })
    .addClass(po_word_txt_bg)
    ;

    txt_maxlen(po_word_txt,  $("#po_word_tip"), $("#po_word_form"), 142)

    /* 显示全部 */
    fdtxt = function(e,id){
        var txt=$(e).parents('.fdtxt'),all=txt.find(".fdall");
        all.addClass("fdloading").find('.fdext').remove()
        $.get("/j/fdtxt/"+id,function(htm){
            txt.find('.fdtxtin').html('<pre class="fdpre">'+htm+"</pre>")
            if(all.find('a').length){
                all.removeClass('fdloading')
            }else{
                all.remove()
            }
        }) 
    }
    fdvideo = function(e, id){
        var div=$('<div class="fdswf"><div class="fdloading"/></div>')
        $(e).replaceWith(div)
        $.get("/j/fdvideo/"+id, function(html){
            div.html(html)
            var win=$(window),
                winst = win.scrollTop(),
                offset = div.offset().top+div.height()-winst-win.height();
            
            if(offset>0){
                win.scrollTop(winst+offset)
            }
        })
    }
})()
