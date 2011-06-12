

(function(){
/*
 0 -1 -1
 1 -1 -2
-1 -1  1
 0  1  1
 1  1 -1
-1  1  2
*/

    $(".decr,.incr,.num,.rt,.rted").poshytip({
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
