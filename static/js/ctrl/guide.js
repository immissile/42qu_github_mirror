


function form(id){
    form_id=$("#form"+id)
    $(form_id).submit(function(){
        $(".errtip").hide()
        var self=$(this), btn=self.find("button[type=submit]"), errtip, error;
        $(btn.blur().attr("disabled",true).css({'background':"#fff","color":"#aaa"})[0].parentNode).after(
            '<span class="form_loading"/>'
        )
        $.post("/j/auth/guide/"+id,self.serialize(),function(o){
            error = o.error
            if(error){
                btn.attr('disabled',false).css({'background':'',"color":''});
                for(var i in error){
                    errtip = $("#errtip_"+i) 
                    errtip.html(error[i])
                    errtip.slideDown()
                }

                $(".form_loading").remove()
                return
            }  


            var next=$("#form"+(id+1));
            if(next[0]){

                self.slideUp()
                next.slideDown()
                next.find("input:first").focus().select()
            }else{
                window.location="/i/guide/pic"
            }
        })
        return false
    })
}
(function(){
$("button[type=submit]").attr('disabled',false);
$("input:first").focus().select()
for(var i=0;i<6;++i){
    form(i)
}
})()

$(function(){
    var j=2
    function job_now_label(elem){
        var id = uuid();
        elem.find('.job_now').attr('id',id).change(function(){
            var last = elem.find('.job_end');
            if(this.checked){
                last.hide()
                last.find("input[name=job_end]").val(0)
            }else{
                last.show()
            }
        })
        elem.find('.label_now').attr('for',id)
        return elem
    }

    $("#career_job").delegate('.unit:last,.title:last', "change", function(){
        var val = $.trim(this.value);
        if(val&&val.length&&val!=this.placeholder){
            career();
        }
    })

    var job_block = job_now_label($('.job_block'));

    function select_workday(name){
        var date=new Date(), year=date.getFullYear();
        select_span($(".job_"+name), "job_"+name, 0, year, year-99)
    }
    select_workday("begin")
    select_workday("end")

    var job_html = job_block.html()
    job_block.find('.job_now').attr('checked',true)
    job_block.find('.job_end').hide()
    job_block.find('input[name=job_now]').val(1)
    job_block.find('.x').remove()

    $('.add_job_a').click(function(){
        var block = $(this).parent();
        block.before(
            job_now_label($('<div class="job_more"/>').html(job_html))
        )
    })


    
    $('#txt').elastic()
    $('#mb1').show()
    $('.step_btn').click(function(){
        var num = parseInt($(this).attr('id').substr(4)) + 1
        $('#mb'+(num-1)).hide()
        $('#mb'+num).show()
    })


})

function job_x(e){
    $(e).parents(".job_more").remove()
}

(function(){
    var school_div=$("#school")
    school(school_div)
    $(".add_school_a").click(function(){
        school(school_div)
        $('.job_icon').remove()
        $('.part1').prepend('<span class="job_icon">■</span>')
        return false
    })
})()

/*
    var school_block = $(".school_block"),
        school_html = school_block.html();

    school_block.find(".x").remove()
    
    $('.add_school_a').click(function(){

        j++
    })
*/
