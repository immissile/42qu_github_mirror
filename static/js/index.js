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
