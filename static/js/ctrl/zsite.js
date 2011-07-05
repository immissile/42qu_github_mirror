$('#zsite_link a').click(function(){
    if(!$.cookie.get('S')){
        login()
        return false
    }else{
        this.target="_blank"
    }
})
