(function(){
var book_query = $("#book_query").focus(),
    book_query_loading=$("#book_query_loading"),
    isbn = $("#isbn");

function book_query_begin(){
    book_query_loading.show()
    isbn.hide()
}
function book_query_end(){
    book_query_loading.hide()
    isbn.show()
    book_query.focus().select()
}

function douban_book_jsonp(url){
    book_query_begin()
    $.getJSON("http://api.douban.com/book/subject/"+url+"?alt=xd&callback=?", function(o){
        var data={};
        console.info(o)
        if(data.id){
            $.postJSON(
            "/book/new/douban", data, 
            function(book){
                window.location = "/book/new/"+book.id
            })
            return
        }
        alert("很遗憾 , 找不对应的图书  ...")
        book_query_end()
    });
}



function book_query_isbn(isbn){
    book_query_begin()
    $.getJSON("/j/book/isbn/"+isbn, function(o){
        if(o.id){
            window.location = "/book/"+o.id
        }else{
            douban_book_jsonp( 'isbn/'+isbn) 
        }
    })
};

$("#book_form").submit(function(){
    var val = $.trim(book_query.val()), isbn_val = val.replace("-","").replace(" ",""), len, jsonp;
    if(!val.length){
        return
    }
    if(/^\d+$/.test(isbn_val)){
        len = isbn_val.length;
        if(len!=10&&len!=13){
            alert(isbn_val+" 只有 "+len+" 位数字\nISBN编号 必须 为 10位 或 13位")
            book_query.focus().select()
        }
        book_query_isbn(isbn_val)
        return false
    }else{
        var keyword = 'book.douban.com/subject/',
            pos = val.indexOf(keyword)
        if(pos>=0){
            jsonp = val.slice(pos+keyword.length).split("/")[0]
            douban_book_jsonp(jsonp)
            return false
        }
    }
    alert(isbn.text())
    book_query.focus()
    return false
})
})()
