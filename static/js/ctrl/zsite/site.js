





function fav(){
    if(!islogin())return;
    $.postJSON(
        '/j/fav',
        function(){
            $("#fav_a").text('设置').attr('href','/mark')
        }
    )
    fancybox_word(
        '备注 :',
        '/j/fav',
        function(){},
        function(){return 1} 
    )
}

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


