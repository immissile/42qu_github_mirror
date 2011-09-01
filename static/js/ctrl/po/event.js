$(function(){
    $("#event_form").submit(function(){
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
    });
    $("#rm").click(function(){
        if(!confirm("删除，确定？")){
            return false
        }
    })
})
function select_event(id, value , hour, minute){
    var date=new Date(), today=new Date();
    date.setDate(date.getDate() + 5)
    var year=today.getFullYear(), month=today.getMonth()+1;

    select_date(id, value, year+100, year-1, true, 
        function(year_val, month_val){
            if(year_val==year&&month_val==month){
                return today.getDay()
            }
            return 1
    },true);

    var prefix='#'+id, year_elem=$(prefix+"_year"), month_elem=$(prefix+"_month"), day_elem=$(prefix+"_day");

    year_elem.change(function(){
        var r=[],val=this.value-0,i=1;
        if(val==year){
            i = date.getMonth()+1
        }
        for(;i<13;++i){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        if(!value){
            month_elem.html(r.join('')).change()
        }
    }).change()
    
    if(!value){
        year_elem.val(date.getFullYear()).change()        
        month_elem.val(date.getMonth()+1).change()
        day_elem.val(date.getDate()).change()
    }
    $(prefix+"_hour").val(hour||12)
    $(prefix+"_minute").val(minute||30)
    
}
