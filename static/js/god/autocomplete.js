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
    auto_height();
    autocomplete_tag("#tags", JSON.parse(data.tags))
});

