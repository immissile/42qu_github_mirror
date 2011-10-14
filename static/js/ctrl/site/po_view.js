$(".site_note a").live('click',function(){
    var self=$(this), prh=$('<div class="sdw"><div class="sd cid62"><pre class="fdh"></pre><div class="fdbarload"></div></div></div>');
    $(this.parentNode).replaceWith(prh)
    prh.find(".fdh").text(self.text())
    
    var r = {
        name:"2011年第2次BPUG活动",
        id:1234,
        fav:true,
        reply_count:1,
        zsite:{
            name:"w",
            unit:"xx",
            title:"zz"
        },
        tag_id:232,
        tag_name:"sss"
    }
    prh.replaceWith($("#feed61").tmpl(r))
    return false
})

function render_site(data){
	var feed_loader = feed_load_maker( "zsite_id id")
	,
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

