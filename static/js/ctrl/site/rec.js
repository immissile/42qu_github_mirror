$(function(){
    close_site = function(){
        $('.site_rec,.arrow_pic,.close_site').remove()
    }
    fav_site = function(){
        $('.site_fav').css({'background':'url("http://s4.42qu.us/img/gif/icons/gif/black/to_size/check.gif") 20% 50%  no-repeat','color':'#000'})
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
})
$("#site_rec").tmpl({}).prependTo("#H")

