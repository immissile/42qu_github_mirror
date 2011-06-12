
function render_feed(){
    $.postJSON(
    "/j/feed",
    function(result){
        console.info(result)
/*
        $("#body").append(
            render('feed',{cid:1})
        )
*/
    })
}
