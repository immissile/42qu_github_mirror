function init(result){
console.info(result)
var rt_list=[],
    data = {},
    attr = "id zsite rt_list zsite_id cid reply_total vote name", i=0, cid=result[4];
    switch(cid){
/*
62 : note
*/
        case 62:attr+=" txt";
    }
    attr = attr.split(" ")
    for(;i<attr.length;++i){
        data[attr[i]] = result[i]
    }
    var zsite = data.zsite;
    data.zsite = {
        name: zsite[0],
        link: zsite[1]
    }
    return data
}

function render_feed(){
    $.postJSON(
    "/j/feed",
    function(result){
        console.info(init(result[0]))
/*
        $("#body").append(
            render('feed',{cid:1})
        )
*/
    })
}
render_feed()
