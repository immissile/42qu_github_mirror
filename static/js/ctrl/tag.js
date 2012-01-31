b1024();
function render_note(data){
    _render_note("#item_list", data);
    $(".com_main,.com_side").show();
}
;$(function(){

    var data = $.parseJSON($("#site_data").html()),
        rec_wrapper=$("#rec_wrapper"),
        site_rec=$("#site_rec");


    if(data&&data.length){
        rec_wrapper.append(site_rec.tmpl(data));
    }

    function fav(id){
        $("#rec_id"+id).addClass("fav_loading");
        callback=function(){
            $("#rec_id"+id).removeClass("fav_loading");
            $("#rec_id"+id).addClass("site_faved");
            $("#rec_id"+id).attr("href","javascript:unfav("+id+")");
        };
        _(id, 2,callback);
    }

    function unfav (id){
        callback=function(){};
        _(id, 0,callback);
        $("#rec_id"+id).removeClass("site_faved");
        $("#rec_id"+id).attr("href","javascript:fav("+id+")");
    }
    $(".buzz_h1").hover(function(){$(this).find("a").show()},function(){$(this).find("a").hide()});
    $(".buzz_w").hover(function(){$(this).find('.bzr').show()},function(){$(this).find(".bzr").hide()});

});

(function(){
    var feeds=$("#feeds"), 
        feed_index=$("#feed_index"), 
        render_txt=$("#render_txt"), 
        scrollTop=feeds.offset().top-14,
        oldtop=-1,
        winj=$(window),
        txt_loading=$('<div><div class="main_nav" id="main_nav_txt"><div id="main_nav_in"><a href="javascript:void(0)" class="readx"></a><span id="main_nav_title"></span></div></div><div id="feed_loading"></div></div>'),
        txt_title=txt_loading.find('#main_nav_title'),
        main_nav_txt = txt_loading.find('#main_nav_txt'),
        feed_loading=txt_loading.find('#feed_loading'),
        txt_body;

    function readx(){
        txt_loading.remove()
        feed_index.show() 
        winj.scrollTop(oldtop)
        oldtop=-1
        var fav=txt_body.find(".fav,.faved")[0];
        if(fav){
            $("#fav"+fav.rel)[0].className = fav.className;
        }

        txt_body.replaceWith(feed_loading)
    }

    $('.readx').live('click',readx)
    $(document).bind("keyup",function(e){
        if(e.keyCode == 27 && oldtop>=0){
            readx()
        }
    })

    $('.reado').live('click',function(){
        feed_index.hide();
        var self=$(this), 
            title=self.find('.title').addClass('c9'), 
            id=this.id.slice(5), 
            user=$(this.parentNode).find('.TPH'),
            user_link=user[0].href
            ;
        txt_title.html(title.html());
        feeds.append(txt_loading);
        oldtop=winj.scrollTop();
        winj.scrollTop(scrollTop);
        $.get(
        "/j/po/json/"+id,
        function(r){

            r.id=id
            r.user_name=user.html()
            r.link = user_link+id
            r.time = $.timeago(r.create_time)
            r.fav = $('#fav'+id)[0].className

            txt_body = render_txt.tmpl(r)
            feed_loading.replaceWith(txt_body)
            winj.scrollTop(scrollTop)
        })

        return false; 
    })



    if(!IE6){
        if(main_nav_txt[0]){
            var top = main_nav_txt.offset().top, win=$(window).scroll(function() {
                if(win.scrollTop() >= scrollTop+14){
                    main_nav_txt.css({'position':'fixed',"marginTop":-scrollTop-14})
                }else{
                    main_nav_txt.css({'position':'absolute',"marginTop":"0"})
                }
            })
        }
    }

})();
