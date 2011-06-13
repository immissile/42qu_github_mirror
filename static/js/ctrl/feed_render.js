(function (){
/*
61 word
62 note
*/
var FEED_ATTR_BASE = "id zsite rt_list zsite_id cid reply_total name is_rt vote_state vote",
    FEED_ATTR = {
        61:FEED_ATTR_BASE,
        62:FEED_ATTR_BASE+" txt"
    };

    for(var i in FEED_ATTR){
        FEED_ATTR[i]=FEED_ATTR[i].split(' ')
    }

    function array2zsite(a){
        return {
            name: a[0],
            link: a[1]
        } 
    }

    function init(result){
        var rt_list=[],
        data = {},
        i=0,
        attr=FEED_ATTR[result[4]];

        for(;i<attr.length;++i){
            data[attr[i]] = result[i]
        }
        data.zsite = array2zsite(data.zsite);
        data.link = "/po/"+data.id;
        
        $.each(data.rt_list, function(){
            rt_list.push(array2zsite(this))
        })
        data.rt_list = rt_list
        return data
    }

    function init_result(result){
        var length = result.length, item=[], i=0;

        for(;i<length;++i){
            item.push(init(result[i]))
        }
        return item 
    }

    function render_feed(){
        $.postJSON(
        "/j/feed",
        function(result){
            $('#feed').tmpl(init_result(result)).appendTo("#feeds")
        })
    }
    render_feed()
})()
