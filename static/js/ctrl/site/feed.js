
;(function(){
var html;
fdh_close = function(id){
    $('#G'+id).replaceWith(html)
    html.find('a:first').addClass('c0')
    $(window).scrollTop(html.offset().top-7)
    html = null
}
fdh_open = function (e){
    var node = $('.cid62').parent().parent().parent()
    if(node[0])fdh_close(node.attr('id').substring(1))
    html = $(e).parent()
    $(window).scrollTop($(e).parent().offset().top - 7)
}
})();
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
                    "name": tt[2],
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


$(".dcid62 .fdh_open").live('click',function(){
    var self=$(this), prh=$('<div class="sdw"><div class="sd cid62"><pre class="fdh"></pre><div class="fdbarload"></div></div></div>'), href=this.href,pn=$(this.parentNode.parentNode.parentNode), fdnt=pn.find('.fdnt')
    if(!fdnt.hasClass('adot')){
        fdnt.addClass("adot")
    }
    pn.find(".site_img").hide()
    $(this.parentNode).replaceWith(prh)
    prh.find(".fdh").text(self.text())
    pn.find(".site_txt").css("width","auto")

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
        prh.replaceWith($("#feed61").tmpl(result))
    }) 
    return false
})


