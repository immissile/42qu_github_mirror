$('#zsite_link').click(function(){
    if(!$.cookie.get('S')){
        login()
        return false
    }
})
