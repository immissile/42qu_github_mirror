
(function(){
    function parse_result(result){
        var r=[],result_length=result.length,i=0,t, m, tt, item, cid, pcid, mm, id,site_id, className;
        for(;i<result_length;++i){
            m={};
            t=result[i],
            tt=t[0];
            site_id=tt[0]
            m.site = {
                "id" : site_id,
                "name" : tt[1],
                "link":tt[2],
                "ico": tt[3] 
            };
            t=t[1];
            m.item = item = []
            for(var j=0;j<t.length;++j){
                tt=t[j]
                //[266, 61, "1317615877.01", "//zuroc.zuroc.xxx", "张沈鹏"]
                id=tt[0]
                cid=tt[1]

                if(
                    j && (  (pcid==61 && pcid!=cid)||cid==61   )
                ){
                    className = "sfpword"
                }else{
                    className = "mb4"
                }
                pcid = cid

                mm = {
                    "id":id,
                    "link":"//"+site_id+HOST_SUFFIX+"/"+id,
                    "cid":cid,
                    "name": tt[2]
                    "className":className
                }
                if(tt.length>2){
                    mm.user_link = tt[3]
                    mm.user_name = tt[4]
                }
                item.push(mm)
            }
            r.push(m)
        }
        return r
    }
    feed_page("/j/site/feed/", "#site_feed", parse_result, 0, function(){

           $("#site_feed").append(
            '<div class="tc mt32" style="margin-bottom:64px"><p>没有内容了啊</p><p><a href="/show">请你点击这里</a></p><p>收藏更多站点</p></div>'
          ) 
    });

})();

/*
<div class="c site_po">
    <a href="http://42qu-exam.42qu.com/"><img
    class="site_img" src="http://p4.42qu.us/96/88/52312.jpg"></a>

    <div class="site_txt c">
        <div class="mb4"><a class="c0" href="http://42qu-exam.42qu.com/">42区笔试题</a></div>
        <div class="mb4"><a href="#">讨论：长文的数字排版与阅读</a></div>
        <div class="mb4"><a href="#">讨论：长文的数字排版与阅读</a></div>
        <div class="sfpword">买了一个air，终于不用背3kg的石头到处跑了。买的时候纠结了好久，是买11还是13的，觉得13看电视会方便，只贵几百块。看了13的air 又觉得差不多加几百就可以买 13的pro高配了。然后又在13的air 和pro纠结。最后还是买了11的air，想起我最初的需求买个便携性好的。。关键的时刻脑袋还是很能用的哈哈<span class="split">-</span><a style="color: rgb(0, 0, 0);" href="#">张沈鹏</a> <a href="http://site.42qu.com/10097628" class="zsite_reply"></a> </div>
    </div>
</div>
*/
