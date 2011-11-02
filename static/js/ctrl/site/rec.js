
;$(function(){
    $("#site_rec").tmpl({}).prependTo(".H")
    var site_rec=$('.site_rec')
    function _(id, state){
        $.postJSON( '/j/site/rec/'+id+'-'+state)
    }
    function site_to(id){
        var num = $('.D').length
        $('.site_to').css('margin-left',401-(num-Number(id.slice(2)))*64) 
    }
    site_x = function(id){
        site_rec.remove()
        _(id, 1)
    }
    site_fav = function(id){
        $('.site_unfav').slideUp()
        $('.site_fav').replaceWith('<span class="site_unfav" style="color:#000;">收藏成功</span>')
        $('.site_unfav').removeClass('site_fav')
        $('.site_more').slideDown()
        _(id, 2)
    }
    site_unfav = function(id){
        _(id, 0)
        site_rec.remove()
    }
    site_to('da2')

    site_rec.hide()
    setTimeout(function(){
        site_rec.slideDown('slow')
    },1000)
});

