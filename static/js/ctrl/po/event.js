$(function(){
    $("#po_form").submit(function(){
        var error;
        if( $.trim($("#pic").val()) == '' && !$("#pic_id")[0]){
            error = "请选择宣传图片"
        }else if( $.trim($("#address").val()) == ''){
            error = "请输入详细地址"
        }else if( $.trim($("#phone").val()) == ''){
            error = "请输入联系电话"
        }else if( $.trim($("#event_cid").val()) == ''){
            error = "请选择活动类型"
        }else if( $("input[name=pid]").val() == 1){
            error = "请选择所在城市"
        }

        if(error){
            alert(error)
            return false
        }
    })
})
