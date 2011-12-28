(function(){
var book_query = $("#book_query").focus(),
    book_query_loading=$("#book_query_loading"),
    isbn = $("#isbn");

function book_query_begin(){
    book_query_loading.show()
    isbn.hide()
    book_query.focus().select()
}
function book_query_end(){
    book_query_loading.hide()
    isbn.show()
}

function name_join(name_list){
    for(var i=0;i<name_list.length;++i){
        name_list[i] = name_list[i].replace(";","-")
    }
    return name_list.join(";")
}

function douban_book_jsonp(url){
    book_query_begin()
    $.getJSON("http://api.douban.com/book/subject/"+url+"?alt=xd&callback=?", function(o){
        if(o.id){
            var data={}, id = o.id['$t'].split("/");

            id=id[id.length-1]

            var i, r=[], t, key, value;

            t = o.author;
            if(t){ 
                for(i=0;i<t.length;++i){
                    r.push(t[i]['name']['$t'])
                }
                data.author = name_join(r);
            }

            t = o['db:attribute']
            if(t){ 
                for(i=0;i<t.length;++i){
                    key = t[i]['@name']
                    value = t[i]['$t']
                    if(key=='author')continue;
                    if(key=="isbn13")key='isbn';
                    if(key=='translator'){
                        if(!data[key]){
                            data[key]=[]
                        }
                        data[key].push(value)
                    }else{
                        data[key]=value
                    }
                }
            }
            if(data.translator){
                data.translator = name_join(data.translator)
            }
            t=o.summary
            if(t){
                data.txt = t['$t']
            }
            t=o.title
            if(t){
                data.title = t['$t']
            }

            t=o['gd:rating']
            if(t){
                data.rating = t['@average']
                data.rating_num = t['@numRaters']
            } 
            t = o['link']
            if(t){ 
                for(i=0;i<t.length;++i){
                    value = t[i]['@href']
                    key = t[i]['@rel']
                    if(key=='image'){
                        data.pic_id = value.split("spic/s")[1].slice(0,-4)
                    } 
                }
            }
            $.postJSON(
            "/book/new/douban/"+id, data, 
            function(book){
                window.location = "/book/new/"+book.id
            })
            return
        }
        alert("很遗憾 , 找不对应的图书  ...")
        book_query_end()
    })
}

function book_query_isbn(isbn){
    book_query_begin()
    $.getJSON("/j/book/isbn/"+isbn, function(o){
        if(o.id){
            window.location = "/book/lib/"+o.id
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
