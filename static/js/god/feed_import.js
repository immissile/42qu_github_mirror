function load_tag(id){ 
    var data, txt=$("#txt"),prefix='/feed_import/'+id;

    function refresh_data(r)
    {
        if(data===0){
            alert("没有内容了")
        }
        if(data){
            $("#author_rm").attr('checked',data.author_rm);
            autocomplete_tag("#tag_id_list", data.tag_id_list)
            $("#editwrapper").html($("#render_txt").tmpl(data));
            txt.height(txt[0].scrollHeight);
            window.scrollTo(0, 0);
        }
        data = r;
    }



    $("#nobtn").click(function(){
        var post_data = $("#editform").serialize();
        $.postJSON('/feed_import/rm',post_data ,refresh_data);
    });

    $("#okbtn").click(function(){
            if($("input:radio:checked").val()){
                var post_data = $("#editform").serialize();
                $.postJSON('/feed_import/1',post_data ,refresh_data);
            }else{
                alert("请选择类型");
            }
    });

    auto_height();

    $.getJSON(prefix+'/0',function(r){
        data=r
        if(data){
            $.getJSON(prefix+'/1', refresh_data) 
        }
    })

}
