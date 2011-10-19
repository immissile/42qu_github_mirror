
;$(function(){
    site_x = function(){
        $('.site_rec,.site_to,.site_x').remove()
    }
    site_fav = function(id){
        $('.site_unfav').slideUp()
        $('.site_fav').replaceWith('<span class="site_unfav" style="color:#000;">收藏成功</span>')
        $('.site_unfav').removeClass('site_fav')
        $('.site_more').slideDown()
        $.postJSON('/j/site/fav/'+id)
    }
    site_unfav = function(id){
        $.postJSON( '/j/site/unfav/'+id)
        $('.site_rec').remove()
    }
});
$("#site_rec").tmpl({}).prependTo(".H")
