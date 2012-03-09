function month_days(year, month) {
    switch (month) { 
        case 2: return ((year%4 == 0) && (year%100 != 0) || (year%400 == 0)) ? 29 : 28; case 4: case 6: case 9: case 11: return 30; default: return 31; 
    } 
} 
function zfill(number, length) {
    var num = '' + number;
    while (num.length < length) {
        num = '0' + num;
    }
    return num;
}

    
function select_span(span, name, value, year_begin, year_end, no_empty, month_begin, show_time){

    var r=[
        '<input type="hidden" value="0" name="'+name+'">'
    ], i, span, day_option='<option value="0">- 日 -</option>', diff=year_begin>year_end?-1:1;
    if(year_begin!=year_end){
        i=year_begin;
        r.push('<select id="'+name+'_year"class="'+name+'_year date_year" name="year">')
        if(!no_empty){
            r.push('<option value="0000">- 年 -</option>')
        }
        for(;i!=year_end;i+=diff){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        r.push('</select>')
    }
    r.push(
'<select id="'+name+'_month" class="'+name+'_month date_month" name="month">'
    )
    if(!no_empty){
        r.push('<option value="0">- 月 -</option>')
    }
    for(i=1;i<13;++i){
r.push('<option value="'+i+'">'+i+'</option>')
    }
    r.push(
'</select><select id="'+name+'_day"class="'+name+'_day date_day" name="day">'+day_option+'</select>'
    )
    function select(name){
        return span.find("select[name="+name+"]")
    }

    if(show_time){
        r.push(
            '<select id="'+name+'_hour" class="'+name+'_hour date_hour" name="'+name+'_hour">'
        )
        for(i=0;i<24;++i){
            r.push('<option value="'+i+'">'+zfill(i,2)+'</option>')
        }
        r.push('</select>:')
        r.push(
            '<select id="'+name+'_minute" class="'+name+'_minute date_minute" name="'+name+'_minute">'
        )
        for(i=0;i<60;i+=5){
            r.push('<option value="'+i+'">'+zfill(i,2)+'</option>')
        }
        r.push('</select>')
    }


    span.html(r.join(''))



    var year=select('year'), month=select('month'), day=select('day'), hidden=span.find('input');
    function _(){
        var dv=day.val(),
            year_val = year.val()-0,
            month_val = month.val()-0,
            days=month_days(year_val,month_val), 
            r=[];
        if(!no_empty){
            r.push(day_option)
        }
        for(i=month_begin?month_begin(year_val,month_val):1;i<=days;++i){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        day.html(r.join('')).val(dv>days?0:dv)
    }
    function input(){
        var mv=month.val(),dv=day.val();
        hidden.val(
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
       hidden.val(value)
    }
}

function select_date(id, value, year_begin, year_end, no_empty, month_begin, show_time){
    document.write('<span id="'+id+'"></span>');
    select_span($("#"+id), id, value, year_begin, year_end, no_empty, month_begin, show_time)
}


function select_birthday(id, value){
    var date=new Date(), year=date.getFullYear();
    select_date(id, value, year, year-128)
}



