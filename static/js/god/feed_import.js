function load_tag(id){ 
    var data, prefix='/feed_import/'+id;

    function refresh_data(r)
    {
        if(data===0){
            alert("没有内容了")
        }
        if(data){
            $("#editwrapper").html($("#render_txt").tmpl(data));
            $("#author_rm").attr('checked',data.author_rm);
            autocomplete_tag("#tag_id_list", data.tag_id_list)
            //var txt=$("#txt")
//            txt.height(txt[0].scrollHeight);

            window.scrollTo(0, 0);
            $('#txt').css('height',($(window).height()-240) + 'px')

        }
        data = r;
    }



    $("#nobtn").click(function(){
        $.postJSON(
            prefix+'/rm/'+$("#feed_id").val(),
            refresh_data
        );
    });

    
    $("#okbtn").click(function(){
            if($("input:radio:checked").val()){
                var post_data = $("#editform").serialize();
                $.postJSON(prefix+'/next',post_data ,refresh_data);
            }else{
                alert("请选择类型");
            }
    });


    $.getJSON(prefix+'/0',function(r){
        data=r
        if(data){
            $.getJSON(prefix+'/1', refresh_data) 
        }else{
            alert("没有内容了")
        }
    })

}


