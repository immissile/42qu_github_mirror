function rm(id){
    $("#reply"+id).fadeOut()
    $.postJSON("/wall/reply/rm/"+id)
}
