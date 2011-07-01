
(function(){
function select_workday(prefix, elem, val){
    val = val||0;
    var date=new Date(), year=date.getFullYear();
    select_span(elem, prefix+"_"+elem[0].className, val, year, year-99)
}

function history(
    name, unit_placeholder, title_placeholder,
    unit, title, txt, begin, end
){
    var result = {
            "unit_placeholder"  : unit_placeholder,
            "title_placeholder" : title_placeholder,  
            "name" : name 
        },
        div = $("#history_"+name),
        history = $('#history_tmpl').tmpl(result).appendTo(div),
        end = history.find("span.end"),
        begin = history.find("span.begin"),
        uid = uuid(),
        now = history.find('input.now').attr("id",uid),
        label = history.find(".label_now").attr("for",uid);
        history.find('[placeholder]').placeholder();

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
}
function history_job( 
    unit, title, txt, begin, end
){
    history(
        "job",
        "单位",
        "头衔",
        unit, title, txt, begin, end
    )
}
function history_edu(
    unit, title, txt, begin, end
){
    history(
        "edu",
        "学校",
        "专业",
         unit, title, txt, begin, end
    )
}
$(".history").delegate('.unit:last,.title:last', "change", function(){
    var val = $.trim(this.value);
    if(val.length&&val!=this.placeholder){
        window['history_'+(this.name.split("_")[0])]()
    }
})

$("#history_form").submit(function(){
    $("input[placeholder]").each(function(){
        if(this.value==this.placeholder){
            this.value=''
        }
    })
})
history_edu()
history_job()
})()
