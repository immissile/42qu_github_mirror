
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
    i = $('#'+r);
    i.hide("slow");
}
$(".site_fav_a").click(function(){
    $(this).addClass("fav_loading");
});

change = function(){
    textarea.addClass('saying')
};
calcel = function(){
    textarea.removeClass('saying')
};

tip = $('#txt_tip');
can_say = txt_maxlen(textarea, tip, 142, change,calcel);

$('#po_ext').click(function(){
    $('#po_ext').hide();
    tip.hide();
    $('.say_type').show();
});

function visit(link,id){
$("#rp_"+id).attr("href","javascript: closeBuzz("+id+",0)");
window.open(link,"_blank");
}

function closeBuzz(id,state){
        if (state>0)
        {
            $.postJSON(
                    '/j/reply/rm/'+state+'/'+id,
                    function(result){
                        
                    })
        }
        $("#bz_"+id).hide('slow');
}
function clear_part(id)
{
    $.postJSON(
            '/j/buzz/clean/'+id,
            function(result){
                location.reload(true);
            })
}
