function load_tag(id, prefix){ 
    var data;
    prefix+=id;

    refresh_data = function(r)
    {
        if(data===0){
            alert("没有内容了")
        }
        if(data){
            var btn=$("#nobtn,#okbtn");
            btn.hide(function(){
                setTimeout(btn.show(1000),1500)
            });
            $("#editwrapper").html($("#render_txt").tmpl(data));

if(data.author_rm){
    $("#author_rm").attr('checked',data.author_rm);
}

            autocomplete_tag("#tag_id_list", data.tag_id_list)
            //var txt=$("#txt")
//            txt.height(txt[0].scrollHeight);

            window.scrollTo(0, 0);
            $('#txt').css('height',($(window).height()-210) + 'px')

        }
        data = r;
    }


    $("#nobtn").live('click',function(){
        $.postJSON(
            prefix+'/pass/'+$("#feed_id").val(),
            refresh_data
        );
        $("#editform").remove()
    });

    
    $("#okbtn").live('click',function(){
            if($("input:radio:checked").val()){
                
                var post_data = $("#editform").serialize();
                $.postJSON(prefix+'/1',post_data ,refresh_data);
                $("#editform").remove()
            }else{
                alert("请选择类型");
            }
    });

    $(function(){
        $.fancybox.showActivity()
        $.getJSON(prefix+'/0',function(r){
            data=r
            if(data){
                $.getJSON(prefix+'/1', function(r){
                    refresh_data(r);
                    $.fancybox.hideActivity();
                }) 
            }else{
                alert("没有内容了")
                $.fancybox.hideActivity();
            }
        })
    })
}


