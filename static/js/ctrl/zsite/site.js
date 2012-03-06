function sitefav(){
    if(!islogin())return;
    $.postJSON(
        '/j/fav',
        function(){
            $("#fav_a").text('设置').attr('href','/mark')
        }
    )
    fancybox_word(
        '备注 :',
        '/j/fav',
        function(){},
        function(){return 1} 
    )
}

