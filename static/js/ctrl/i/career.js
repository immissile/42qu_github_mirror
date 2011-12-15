
(function(){
var job = "job";
function select_workday(prefix, elem, val, year_end){
    val = val||0;
    var date=new Date(), year=date.getFullYear();
    year_end=year_end||year-99
    select_span(elem, prefix+"_"+elem[0].className, val, year, year_end)
}

function career(
    unit, title, txt, begin_val, end_val, id
){
    var unit_placeholder, title_placeholder, date_year = '.date_year', name="job";
    unit_placeholder = "单位"
    title_placeholder = "头衔"

    var result = {
            "name" : name, 
            "unit_placeholder" : unit_placeholder,
            "title_placeholder" : title_placeholder,
            "unit":unit,
            "title":title,
            "txt":txt,
            "id":id
        },
        div = $("#career_"+name);
    
     data = []

     var
        career = $('#career_tmpl').tmpl(result).appendTo(div),
        end = career.find("span.end"),
        begin = career.find("span.begin"),
        uid = uuid(),
        now = career.find('input.now').attr("id",uid),
        label = career.find(".label_now").attr("for",uid),
        unit_placeholder ,
        title_placeholder;



        now.change(function(){
            if(this.checked){
                end.fadeOut()
            }else{
                end.fadeIn()
            }
            end.find("input[type=hidden]").val("0")
        }).attr('checked',false)

        career.find('.rm').click(function(){
            career.fadeOut(function(){
                career.remove()
            })
            if(id){
                $.postJSON("/j/career/rm/"+id);
            }
        });
        

        div.find(".rm").show();
        div.find(".rm:last").hide(); 
        select_workday(name, begin, begin_val)
        select_workday(name, end, end_val)
        if(end_val==0){
            end.hide()
            now.click()
        }
}


$(".career").delegate('.unit:last,.title:last', "change", function(){
    var val = $.trim(this.value);
    if(val&&val.length&&val!=this.placeholder){
        career();
    }
})


$("#career_form").submit(function(){
    $("input[placeholder]").each(function(){
        if(this.value==this.placeholder){
            this.value=''
        }
    })
})

function loads(name){
    var data = $.parseJSON($("#career_data_"+name).html()),i=0,t;
    for(;i<data.length;++i){
        t=data[i];
        t.unshift(name)
        career.apply(this,t)
    }
    career()
}

loads(job)

})()
