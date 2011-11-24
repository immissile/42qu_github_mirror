function apply_new(id){
    _apply("new",id)
}
function apply_rm(id){
    _apply("rm",id)
}
function _apply(action, id){
    $("#apply"+id).fadeOut()
    $.postJSON("/j/com/apply/"+action+"/"+id)
}

