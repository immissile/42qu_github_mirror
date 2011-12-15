;$(function(){

    function loadrec(id){
        $.postJSON("/site/rec/new",{},function(r){
            if(r!='')
        {
            site={
                "id":r[0],
        "link":r[1],
        "name":r[2],
        "ico":r[3],
        "motto":r[4]
            };
            $("#site_rec").tmpl(site).appendTo("#rec_wrapper");
            refreshState();
        }
        });
    }
    loadrec(0);

    function _(id, state, callback){
        $.postJSON( '/j/site/rec/'+id+'-'+state,{},function(r)
                {
                    callback&&callback();
                }
                )
    }

    function refreshState()
    {
        $(".site_li").mouseenter(
                function(r){
                    i=$(this).find(".delbtn");
                    i.addClass("show_x")
                }
                );
        $(".site_li").mouseleave(
                function(r){
                    $(this).find(".delbtn").removeClass("show_x")
                }
                );

        del=function(r){
            i = $('#rec_'+r);
            i.hide("slow");

            callback=function(){
                loadrec(0);
            };
            _(r, 1,callback);
        };

        fav=function(id){
            $("#rec_id"+id).addClass("fav_loading");
            callback=function(){
                $("#rec_id"+id).removeClass("fav_loading");
                $("#rec_id"+id).addClass("site_faved");
                $("#rec_id"+id).attr("href","javascript:unfav("+id+")");
                loadrec(0);
            };
            _(id, 2,callback);
        };



        unfav=function(id){
            callback=function(){};
            _(id, 0,callback);
            $("#rec_id"+id).removeClass("site_faved");
        };
    }
});

