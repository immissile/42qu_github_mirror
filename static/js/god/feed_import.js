$(function(){
    var data = $.parseJSON($("#site_data").html());
    
    function refresh_data(r)
    {
        $("#author_rm").attr('checked',data.author_rm);
        data = r||{};
    }
    function auto_height(){
        $("#txt").height($("#txt")[0].scrollHeight);
        window.scrollTo(0, 0);
    }

    $("#editwrapper").html($("#render_txt").tmpl(data));

    $.getJSON('/feed_import/next',refresh_data)

    $("#nobtn").click(function(){
        var post_data = $("#editform").serialize();
        $("#editwrapper").html($("#render_txt").tmpl(data));
        $.postJSON('/feed_import/rm',post_data ,refresh_data);
        auto_height();
    });

    $("#okbtn").click(function(){
            if($("input:radio:checked").val()){
            var post_data = $("#editform").serialize();
            $("#editwrapper").html($("#render_txt").tmpl(data));
            $.postJSON('/feed_import/next',post_data ,refresh_data);
                auto_height();
            }else{
            alert("请选择类型");
            }
    });

    auto_height();
    autocomplete_tag("#tag_id_list", data.tag_id_list)
});

