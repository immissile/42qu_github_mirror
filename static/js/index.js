WINDOW_WIDTH = document.documentElement.clientWidth;
textarea = $('.say_txt');
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
    $('.say_type').hide();
    $('#po_ext').show();
    textarea.addClass('saying')
};
calcel = function(){
    $('#po_ext').hide();
    $('.say_type').show();
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
		$.postJSON(
                '/j/reply/rm/'+state+'/'+id,
                function(result){
                    alert(result);
                })
        $("#bz_"+id).hide('slow');
}
