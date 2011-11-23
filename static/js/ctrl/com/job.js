
rm_job = function(id,isold){
    var hint = isold==5?'确定停止该职位的招聘?':'确定删除该职位?'
    var url = '/job/rm/'+isold
    if(confirm(hint)){
        $.postJSON(
            url,
            {'id':id}
        )
        $('#job_'+id).parent().remove()
    }
}
