b1024()
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
        rendered_txt,
        oldtop=0,
        winj=$(window);

    $('.readx').live('click',function(){
        rendered_txt.remove()
        feed_index.show() 
        winj.scrollTop(oldtop)
    })
    $('.reada').live('click',function(){
        feed_index.hide();
        rendered_txt = render_txt.tmpl()
        feeds.append(rendered_txt)
        oldtop=winj.scrollTop()
        winj.scrollTop(scrollTop)
        return false; 
    })
})();
