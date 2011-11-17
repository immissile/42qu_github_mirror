rm_job = function(id,isold){
    var hint = isold==0?'确定停止该职位的招聘?':'确定删除该职位?'
    var url = isold==0?'url1':'url2'
    if(confirm(hint)){
        $.postJSON(
            url,
            {'id':id}
        )
        $('#job_'+id).parent().remove()
    }
}
