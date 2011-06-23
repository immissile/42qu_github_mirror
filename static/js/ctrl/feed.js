/*
 0 -1 -1
 1 -1 -2
-1 -1  1
 0  1  1
 1  1 -1
-1  1  2
*/
(function() {

	$(".reply,.down,.up,.num,.rt,.rted").poshytip({
		className: 'tip-twitter',
		showTimeout: 100,
		alignTo: 'target',
		alignX: 'center',
		offsetY: 5,
		allowTipHover: false,
		fade: false,
		slide: false,
		liveEvents: true
	});

	var down = "down", up = "up", vote = "vote";
	function _(a, b, id, v) {
		var wj = $("#" + vote + id),
		w = wj[0],
		state = w.className.slice(4) - 0,
		num = wj.find('.num'),
		numv = num.text() - 0,
		c = v,
		notsame = (v != state) - 0;
		if (notsame) {
			v -= state
		} else {
			c = 0;
			v = - v
		}
		$.postJSON("/j/feed/" + a + notsame + "/" + id)
		w.className = vote + c;
        wj.find('a').blur()
		num.text(numv + v)

        var fancybox=$.fancybox;
        fancybox({
            content:'<form id="vote_reply" style="width:470px;padding:8px 16px 0 14px"><h3 style="font-size:16px;margin-bottom:7px">留下你的看法吧 ...</h3><textarea style="width:461px;height:200px;font-size:16px;padding:2px 3px;margin:5px 0 10px" name="txt"></textarea><div class="btns"><span class="btnw"><button class="btn" type="submit">确定</button></span></div></form>',
            onComplete:function(){
                $("#vote_reply").submit(function(){
                    var self=$(this), textarea=self.find("textarea"), txt = $.trim(textarea.val());
                    if(txt&&txt.length){
                        fancybox.showActivity()
                        $.postJSON(
                            "/j/po/reply/"+id, {'txt':txt},
                            function(r){
                                if(r.can_not_reply){
                                    fancybox({
                                        content:'<div class="tc f16 pd16" style="width:225px"><p>啊 , 出错了 !</p><p>为了维护一本正经的讨论气氛</p><p>未认证用户不能发表看法哦</p><p><a href="/i/verify">点此申请认证吧</a></p></div>'  
                                    }) 
                                }else{
                                    fancybox.close()
                                }
                        })
                    }else{
                        fancybox.close()
                    }
                    return false;
                })
            }
        })
        
	}
	vote_up = function(id) {
		_(up, down, id, 1)
	}
	vote_down = function(id) {
		_(down, up, id, - 1)
	}
})()
