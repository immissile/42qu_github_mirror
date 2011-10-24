$(".site_note .fdh_open").live('click',function(){
    var self=$(this), prh=$('<div class="sdw"><div class="sd cid62"><pre class="fdh"></pre><div class="fdbarload"></div></div></div>'), href=this.href;
    $(this.parentNode).replaceWith(prh)
    prh.find(".fdh").text(self.text())

    $.getJSON("/j/po"+href.slice(href.lastIndexOf("/")),function(r){
        var zsite=r.pop(), result = {
            zsite : {
                name:zsite[0],
                link:zsite[1],
                unit:zsite[2],
                title:zsite[3]
            }
        },
        attr="id user_id cid rid zsite_id reply_count create_time name txt".split(' '), j=0;

        for (; j < attr.length; ++j) {
            result[attr[j]]=r[j]
        }
        prh.replaceWith(
            $("#feed61").tmpl(result)
        )
    }) 
    return false
})

function render_site(data){
	var feed_loader = feed_load_maker( "zsite_id id"),
    zsite_dict = data[1],
    career_dict = data[2],
    data = data[0],
    i,
    length = data.length,
    result,
    t,
    o,
    r = [],
    z
;

    for (i=0;i < length; ++i) {
        t=feed_loader(data[i])
        t.zsite = z= {}
        o = zsite_dict[t.zsite_id]
        if(o){
            z.name = o[0] 
            z.link = o[1] 
        }
        o = career_dict[t.zsite_id]
        if(o){
            z.unit = o[0]
            z.title = o[1] 
        }

        r.push(t)
    }
    $('#feed').tmpl(r).appendTo("#feeds");
}

;(function(){
var html;
fdh_close = function(id){
    $('#G'+id).replaceWith(html)
    html.find('a:first').addClass('c0')
    $(window).scrollTop(html.offset().top-7)
    html = null
}
fdh_open = function (id){
    var node = $('.cid62').parent().parent().parent()
    if(node[0])fdh_close(node.attr('id').substring(1))
    html = $('#sn'+id)
    $(window).scrollTop($('#sn'+id).offset().top - 7)
}
})();
