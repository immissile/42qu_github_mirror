$.template(
    'note',
    '<div class="readl c">'+
        '<a rel="${$data[0]}" href="javascript:void(0)" id="fav${$data[0]}" class="fav{{if $data[5]}}ed{{/if}}"></a>'+
        '<div id="reado${$data[0]}" class="reado">'+
            '<span class="reada">'+
                '<span class="title">${$data[1]}</span>'+
                '<span class="rtip">${$data[2]}</span>'+
            '</span>'+
        '</div>'+
        '<div class="zname">'+
            '<a href="#" rel="${$data[3]}" class="TPH" target="_blank">${$data[4]}</a>'+
        '</div>'+
    '</div>'
)


function _render_note(elem, data){
    var result = $.tmpl('note', data)
    result.find('.TPH').each(function(){
        this.href="//"+this.rel+HOST_SUFFIX
    })
    result.appendTo(elem);
}

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

