;$(function(){

    data = $.parseJSON($("#site_data").html());

    function addRec(){
        if(data&&data.length){
            site = data.pop();
            $("#rec_wrapper").html($("#site_rec").tmpl());

            $("#rec_wrapper").show();
            $("#rec_"+ site[0]).hide().show("slow");
            $("#rec_title").show();

            refreshState();
        }else{
                $("#rec_title").hide("fast");
                $("#rec_wrapper").hide("fast");
        }
    }
    addRec();

    function loadrec(id){
        $.postJSON("/j/site/rec/new",{},function(r){
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

    function _(id, state, callback){
        $.postJSON( '/j/site/rec/'+id+'-'+state,{},function(r)
                {
                    callback&&callback();
                }
                )
    }

        del=function(r){
            i = $('#rec_'+r);
            i.hide("slow",addRec);
            callback=function(){
                loadrec(0);
            };
            _(r, 1,callback);
        };

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
        };

        fav=function(id){
            $("#rec_id"+id).addClass("fav_loading");
            callback=function(){
                $("#rec_id"+id).removeClass("fav_loading");
                $("#rec_id"+id).addClass("site_faved");
                $("#rec_id"+id).attr("href","javascript:unfav("+id+")");
            };
            _(id, 2,callback);
        }

        unfav=function(id){
            callback=function(){};
            _(id, 0,callback);
            $("#rec_id"+id).removeClass("site_faved");
            $("#rec_id"+id).attr("href","javascript:fav("+id+")");
        }
        $(".right_title").hover(function(){$(this).find("a").show()},function(){$(this).find("a").hide()});
        $(".buzz_w").hover(function(){$(this).find('.bzr').show()},function(){$(this).find(".bzr").hide()});


});

