(function (){
/*
61 word
62 note
*/
var FEED_ATTR_BASE = "id zsite rt_list zsite_id cid reply_total vote name",
    FEED_ATTR = {
        61:FEED_ATTR_BASE,
        62:FEED_ATTR_BASE+" txt"
    }
    for(var i in FEED_ATTR){
        FEED_ATTR[i]=FEED_ATTR[i].split(' ')
    }

function init(result){
    var rt_list=[],
    data = {},
    i=0,
    attr=FEED_ATTR[result[4]];

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
function init_result(result){
    var data = {},length = result.length, item=[], i=0;

    if(result.length){
        data.next = result[length-1][0]
        for(;i<length;++i){
            item.push(init(result[i]))
        }
        data.item = item
    }else{
        data.next = 0
    }
    console.info(data)
    return data
}

function render_feed(){
    $.postJSON(
    "/j/feed",
    function(result){
        $("#body").append(
            render(
                'feed',
                init_result(result)
            )
        )
    })
}
render_feed()
})()
