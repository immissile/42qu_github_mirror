
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

    $('.add_job_a').click(function(){
        var block = $(this).parent();
        block.before(
            job_now_label($('<div class="job_more"/>').html(job_html))
        )
    })
    $('.school_select').live('focus',pop_school)
    $('#txt').elastic()
    $('#mb1').show()
    $('.step_btn').click(function(){
        var num = parseInt($(this).attr('id').substr(4)) + 1
        $('#mb'+(num-1)).hide()
        $('#mb'+num).show()
    })
    $('.school_year').prepend('<option value="">入学年份</option>')
    for(var i=2011;i>1899;i--){
        $('.school_year, .job_begin_year, .job_end_year').append('<option value='+i+'>'+i+'</option>')
    }
    for(var i=1;i<=12;i++){
        $('.job_begin_month, .job_end_month').append('<option value='+i+'>'+i+'</option>')
    }
    var part1 = $('.part1').html(),
    part2 = $('.part2').html()
    $('.part1').append('<input type="hidden" name="univ_id" id="univ_id1" value="" />')
    $('.add_school_a').click(function(){
        var icon = '<span class="job_icon">■</span>'
        if(!$('.part1').find('.job_icon')[0]){
            $('.part1').prepend($(icon))
        }
        var block = $(this).parent()
        block.before('<p>'+icon+part1+'<input type="hidden" name="univ_id" id="univ_id'+j+'" value="" /></p>')
        block.before('<p>'+part2+'</p>')
        $('.school_select:last').attr('id','school_select'+j)
        $('.dep:last').attr('id','dep'+j)
        j++
    })
})
