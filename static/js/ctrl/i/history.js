
(function(){
var edu = "edu", job = "job";
function select_workday(prefix, elem, val){
    val = val||0;
    var date=new Date(), year=date.getFullYear();
    select_span(elem, prefix+"_"+elem[0].className, val, year, year-99)
}

function history(
    name,
    unit, title, txt, begin, end, id
){
    var unit_placeholder, title_placeholder;
    if(name == edu){
        unit_placeholder = "学校"
        title_placeholder = "专业"
    }else{
        unit_placeholder = "单位"
        title_placeholder = "头衔"
    }

    var result = {
            "name" : name, 
            "unit_placeholder" : unit_placeholder,
            "title_placeholder" : title_placeholder,
            "unit":unit,
            "title":title,
            "txt":txt,
            "id":id
        },
        div = $("#history_"+name);
    
     data = []

     var
        history = $('#history_tmpl').tmpl(result).appendTo(div),
        end = history.find("span.end"),
        begin = history.find("span.begin"),
        uid = uuid(),
        now = history.find('input.now').attr("id",uid),
        label = history.find(".label_now").attr("for",uid),
        unit_placeholder ,
        title_placeholder;


        history.find('[placeholder]').placeholder()

        now.change(function(){
            if(this.checked){
                end.fadeOut()
            }else{
                end.fadeIn()
            }
            end.find("input[type=hidden]").val("-1")
        }).attr('checked',false)

        history.find('.rm').click(function(){
            history.fadeOut(function(){
                history.remove()
            })
        });

        div.find(".rm").show();
        div.find(".rm:last").hide(); 
        select_workday(name, begin)
        select_workday(name, end)
        if(end==-1){
            now.click()
        }
}


$(".history").delegate('.unit:last,.title:last', "change", function(){
    var val = $.trim(this.value);
    if(val.length&&val!=this.placeholder){
        history(this.name.split("_")[0]);
    }
})


$("#history_form").submit(function(){
    $("input[placeholder]").each(function(){
        if(this.value==this.placeholder){
            this.value=''
        }
    })
})

history(job, "测试", "ccx", "zzbw", 0, 20091010, 12)


history(edu)
history(job)

})()
