(function(){
    function load(ico_list){
        var t=ico_list.shift();
        ico_list.push(t);
        $('#zsite_ico').tmpl([t]).appendTo("#zsite_list");
    }

     zsite_ico_list = function(ico_list){
        for(var i=0;i<12;++i){
            load(ico_list)
        }
        function _(){
            var t = $('#zsite_list .zsite_ico:first')
            t.slideUp(500, function(){
                $(this).remove()
                load(ico_list)
                setTimeout( _ , 2000)
            })
        }
        setTimeout( _ , 800)
    }
})()



