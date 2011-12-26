$(".buzz_li").live("click",function(){
    $(this.parentNode).find(".buzz_x")[0].visited = 1;

})
$(".buzz_x").live("click", function(){
    if(this.visited){
        $.postJSON( '/j/reply/rm/'+id)
    }
        $("#bz"+id).hide('slow');
})
}
$(".buzz_block_x").click(function(){
    $.postJSON(
        '/j/buzz/block/x/'+this.rel,
        function(){
            $(this).fadeOut() 
    })
})
