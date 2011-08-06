function month_days(year, month) {
    year=year-0
    month=month-0 
    switch (month) { 
        case 2: return ((year%4 == 0) && (year%100 != 0) || (year%400 == 0)) ? 29 : 28; case 4: case 6: case 9: case 11: return 30; default: return 31; 
    } 
} 
    
function select_span(span, name, value, year_begin, year_end, no_empty){
    var r=[
        '<input type="hidden" value="0" name="'+name+'">'
    ], i, span, day_option='<option value="0">- 日 -</option>';
    if(year_begin>year_end){
        i=year_begin; 
        r.push('<select id="'+name+'_year"class="'+name+'_year date_year" name="year">')
        if(!no_empty){
            r.push('<option value="0000">- 年 -</option>')
        }
        for(;i>year_end;--i){
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
    span.html(r.join(''))
    var year=select('year'), month=select('month'), day=select('day'), hidden=span.find('input');
    function _(){
        var dv=day.val(), 
            days=month_days(year.val(),month.val()), 
            r=[];
        if(!no_empty){
            r.push(day_option)
        }
        for(i=1;i<=days;++i){
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

function select_date(id, value, year_begin, year_end, no_empty){
    document.write('<span id="'+id+'"></span>');
    select_span($("#"+id), id, value, year_begin, year_end, no_empty)
}

function select_event(id, value){
    var date=new Date(), today=new Date();
    date.setDate(date.getDate() + 5)
    var year=date.getFullYear();
    select_date(id, value, year+100, year-1, true);

    var year_elem = $("#"+id+"_year"), month_elem=$("#"+id+"_month");

    if(!value){
        year_elem.val(year)        
        month_elem.val(date.getMonth()+1).change()
        $("#"+id+"_day").val(date.getDate())
    }

    year_elem.change(function(){
        var r=[],val=this.value-0,i=1;
        if(val==today.getFullYear()){
            i = date.getMonth()+1
        }
        for(;i<13;++i){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        month_elem.html(r.join(''))
    }).change()

}

function select_birthday(id, value){
    var date=new Date(), year=date.getFullYear();
    select_date(id, value, year, year-128)
}



