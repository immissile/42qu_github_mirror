function month_days(year, month) {
    year=year-0
    month=month-0 
    switch (month) { 
        case 2: return ((year%4 == 0) && (year%100 != 0) || (year%400 == 0)) ? 29 : 28; case 4: case 6: case 9: case 11: return 30; default: return 31; 
    } 
} 

function select_date(id, value, year_begin, year_end){
    document.write('<span id="'+id+'"/>')
    var r=[
        '<input type="hidden" value="0" name="'+id+'">'
    ], i, span=$("#"+id),day_option='<option value="0">- 日 -</option>';
    if(year_begin>year_end){
        i=year_begin; 
        r.push('<select class="'+id+'_year" name="year"><option value="0000">- 年 -</option>')
        for(;i>year_end;--i){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        r.push('</select>')
    }
    r.push('<select class="'+id+'_month" name="month"><option value="0">- 月 -</option>')
    for(i=1;i<13;++i){
        r.push('<option value="'+i+'">'+i+'</option>')
    }
    r.push('</select><select class="'+id+'_day" name="day">'+day_option+'</select>')
    function select(name){
        return span.find("select[name="+name+"]")
    }
    span.html(r.join(''))
    var year=select('year'), month=select('month'), day=select('day');
    function _(){
        var dv=day.val(), 
            days=month_days(year.val(),month.val()), 
            r=[day_option];

        for(i=1;i<=days;++i){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        day.html(r.join('')).val(dv>days?0:dv)
    }
    function input(){
        var mv=month.val(),dv=day.val();
        span.find('input').val(
            year.val()+(mv.length<2?"0":"")+mv+(dv.length<2?"0":"")+dv
        )
    }
    month.change(_)
    year.change(_)
    span.find('select').change(input)
    value=value-0
    if(value){
       year.val(parseInt(value/10000));
       month.val(parseInt(value/100)%100).change(); 
       day.val(value%100);
    }
}


function select_birthday(id, value){
    var date=new Date(), year=date.getFullYear();
    select_date(id, value, year, year-128)
}



