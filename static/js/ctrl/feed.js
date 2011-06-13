

(function(){
/*
 0 -1 -1
 1 -1 -2
-1 -1  1
 0  1  1
 1  1 -1
-1  1  2
*/

    $(".reply,.decr,.incr,.num,.rt,.rted").poshytip({
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

    var decr="decr",incr="incr",vote="vote";
    function _(a,b,id,v){
        var wj=$("#"+vote+id), w=wj[0],
            state=w.className.slice(4)-0,
            num=wj.find('.num'),
            numv=num.text()-0,
            c=v, 
            notsame=(v!=state)-0;
        if(notsame){
            v-=state
        }else{
            c=0;
            v=-v
        }
        $.postJSON("/j/feed/"+a+notsame+"/"+id)
        w.className = vote+c;
        num.text(numv+v)
    }
    vote_incr = function(id){
        _(incr,decr,id,1)
    }
    vote_decr = function (id){
        _(decr,incr,id,-1)
    }
})()

$(".rt").live("click", function(){
    var t=this, self=$(t);
    t.className="rted"
    $.postJSON('/j/rt/'+t.rel)
    self.poshytip('show').poshytip('update','转发成功',true)
})
$(".rted").live("click",function(){
    var t=this, self=$(t);
    t.className="rted"
    $.postJSON('/j/rt/rm/'+t.rel)
    self.poshytip('update','已转发').poshytip('show').poshytip('update','转发被取消',true)
})

