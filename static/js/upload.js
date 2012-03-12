function paras(d) {
    var e = {};
    if (d.indexOf("?") == -1) {
        return {};
    }
    var f = d.split("?")[1].split("&");
        for (var c = 0; c < f.length; c++) {
            if (f[c].indexOf("=") != -1) {
            var b = f[c].split("=");
            e[b[0] + ""] = b[1] + "";
        }
    }
    return e;
}

jQuery.extend({
    createUploadIframe: function(id, uri){
      var frameId = 'jUploadFrame' + id, src = "";
      if(window.ActiveXObject) {
        if(typeof uri== 'boolean'){
            src = 'javascript:false';
        }   
        else if(typeof uri== 'string'){
            src = uri; 
        }   
      }   
      return $('<iframe src="' + src + '" id="' + frameId + '" name="' + frameId + '" style="position:absolute;top:-9999px;left:-9999px;"></iframe>').appendTo('body'); 
    }, 
    createUploadForm: function(id, fileElementId,extra)
    {
        var formId = 'jUploadForm' + id;
        var fileId = 'jUploadFile' + id;
        var form = $('<form  action="" method="POST" name="' + formId + '" id="' + formId + '" enctype="multipart/form-data"></form>'); 
        var oldElement = $('#' + fileElementId);
        var newElement = $(oldElement).clone();
        oldElement.attr('id', fileId).before(newElement);
        oldElement.appendTo(form);
        if(extra != 'undefined'){
            for (var fieldName in extra){
                $('<input value="'+extra[fieldName]+'" name="'+fieldName+'"/>') .appendTo(form);
            }
        }
        $(form).css('position', 'absolute').css('top', '-1200px').css('left', '-1200px').appendTo('body');   
        return form;
    },

    ajaxFileUpload: function(s) {
        s = jQuery.extend({}, jQuery.ajaxSettings, s);
        if(!s.allowType.test(($('#'+s.fileElementId)[0].value||'').toLowerCase())){
            s.begin(12);
            return false;
        }
        var id = new Date().getTime()
        var form = jQuery.createUploadForm(id, s.fileElementId,s.extra);
        var io = jQuery.createUploadIframe(id, s.secureuri);
        var frameId = 'jUploadFrame' + id;
        var formId = 'jUploadForm' + id;        
        if ( s.global && ! jQuery.active++ )
        {
            jQuery.event.trigger( "ajaxStart" );
        }
        if (s.begin) s.begin('');
        var requestDone = false;
        var xml = {};
        if ( s.global )
            jQuery.event.trigger("ajaxSend", [xml, s]);
        var uploadCallback = function(isTimeout) {          

            var io = document.getElementById(frameId);
            if(io.contentWindow)
            {
                xml.responseText = io.contentWindow.document.body?io.contentWindow.document.body.innerHTML:null;
                xml.responseXML = io.contentWindow.document.XMLDocument?io.contentWindow.document.XMLDocument:io.contentWindow.document;
                xml.responsePar = paras(io.contentWindow.location.href);
            }else if(io.contentDocument) {
                xml.responseText = io.contentDocument.document.body?io.contentDocument.document.body.innerHTML:null;
                xml.responseXML = io.contentDocument.document.XMLDocument?io.contentDocument.document.XMLDocument:io.contentDocument.document;
                xml.responsePar = paras(io.contentDocument.location.href);
            }                       

            if ( xml || isTimeout == "timeout")
            {               
                requestDone = true;
                var status;
                    status = isTimeout != "timeout" ? "success" : "error";
                    if ( status != "error" ) {
                        var data = jQuery.uploadHttpData( xml, s.dataType );
                        if ( s.success )
                            s.success( data, status );
                        if( s.global )
                            jQuery.event.trigger( "ajaxSuccess", [xml, s] );
                    } else{
                        jQuery.handleError(s, xml, status, 'timeout');
                        $(io).remove();
                        $(form).remove();
                    }

                if( s.global )
                    jQuery.event.trigger( "ajaxComplete", [xml, s] );

                if ( s.global && ! --jQuery.active )
                    jQuery.event.trigger( "ajaxStop" );

                if ( s.complete )
                    s.complete(xml, status);

                jQuery(io).unbind()

                setTimeout(function() {
                    if($(io) != []) $(io).remove();
                    if($(form) != []) $(form).remove(); 
                }, 200);
                xml = null;
            }
        }

        if ( s.timeout > 0 )
        {
            var timeoutHandler = setTimeout(function(){
                if( !requestDone ) uploadCallback( "timeout" );
            }, s.timeout);
        }
        try {
            var io = $('#' + frameId);
            var form = $('#' + formId).attr('action', s.url).attr('target', frameId).submit();

        } catch(e)
        {           
            jQuery.handleError(s, xml, null, e);
        }
        if(window.attachEvent){
            document.getElementById(frameId).attachEvent('onload', uploadCallback);
        }
        else{
            document.getElementById(frameId).addEventListener('load', uploadCallback, false);
        }       
        return {abort: function (){
            try{
                $(io).remove();$(form).remove();
                clearTimeout(timeoutHandler);
            }catch(e){}
        }}; 

    },
    uploadHttpData: function( r, type ) {
        var data = r.responseText
        if(data.indexOf(">")>0){
            data=data.substring(data.indexOf(">")+1)
            data=data.substring(0,data.indexOf("<"))
        }
        eval( "data = " + data );
        return data;
    }
})



