
(function(){
    function parse_result(result){
        console.info(result)
        return result
    }
    feed_page("/j/site/feed/", "#site_feed", parse_result);

})();
