
;$(function(){
    close_site = function(){
        $('.site_rec,.arrow_pic,.close_site').remove()
    }
    fav_site = function(){
        $('.site_unfav').slideUp()
        $('.site_fav').replaceWith('<span class="site_unfav" style="color:#000;">收藏成功</span>')
        $('.site_unfav').removeClass('site_fav')
        $('.site_more').slideDown()
        $.postJSON(
            'j',
            {}
        )
    }
    unfav_site = function(){
        $.postJSON(
            'j',
            {}
        )
        $('.site_rec,.arrow_pic,.close_site').remove()
    }
});
$("#site_rec").tmpl({}).prependTo(".H")
