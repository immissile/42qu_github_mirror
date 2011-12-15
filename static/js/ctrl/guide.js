
$("button[type=submit]").attr('disabled',false);
$("input:first").focus().select()


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
            }else{
                //location="/"
            }
        })
        return false
    })
}
form(1)
form(2)
form(3)
form(4)

$(function(){
    var j=2
    function job_now_label(elem){
        var id = uuid();
        elem.find('.job_now').attr('id',id).change(function(){
            var last = elem.find('.job_end'),
                job_now = elem.find('input[name=job_now]')
            if(this.checked){
                job_now.val(1)
                last.hide()
            }else{
                last.show()
                job_now.val(0)
            }
        })
        elem.find('.label_now').attr('for',id)
        return elem
    }

    var job_block = job_now_label($('.job_block'));
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
        return false
    })
})()

/*
    var school_block = $(".school_block"),
        school_html = school_block.html();

    school_block.find(".x").remove()
    
    $('.add_school_a').click(function(){
        var icon = '<span class="job_icon">■</span>'
        if(!$('.part1').find('.job_icon')[0]){
            $('.part1').prepend($(icon))
        }
        var block = $('<div class="school_block"/>').html(school_html)
        $(this).parent().before(block)

        block.find('.part1').prepend($(icon))

        $('.school_select:last').attr('id','school_select'+j)
        $('.dep:last').attr('id','dep'+j)
        $('input[name=school_id]:last').attr('id','school_id'+j)

        j++
    })
*/
