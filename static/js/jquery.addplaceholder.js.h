/*!
 * 'addPlaceholder' Plugin for jQuery
 *
 * @author Ilia Draznin
 * @link http://iliadraznin.com/2011/02/jquery-placeholder-plugin/
 * @created 19-02-2011
 * @updated 06-04-2011
 * @version 1.0.3
 *
 * Description:
 * jQuery plugin that adds "placeholder" functionality (like in Chrome) to browsers that 
 * don't support it natively (like Firefox 3.6 or lower, or IE naturally)
 * 
 * Usage:
 * $(selector).addPlaceholder(options);
 */
(function($){

	// add placeholder support check to jQuery.support
	// idea from March Gortz https://gist.github.com/373672
	$.extend($.support, { placeholder: !!('placeholder' in document.createElement('input')) });

	$.fn.addPlaceholder = function(options){
		var settings = {
			'class': 'placeholder',		// name of the class you want to use for placeholder styles
			'allowspaces': false,		// if true doesn't trim value strings so "  " input would NOT be replaced by placeholder (i.e. it's considered valid)
			'dopass': true,				// these two allow you to ignore certain fields, it's a small speed optimization
			'dotextarea': true,
			'checkafill': false			// if true there's a periodic check in case something auto-filled the password fields
		};
		
		return this.each(function(){
			// if browser supports placeholder stop the function
			if ($.support.placeholder) return false;
			
			// get the options if there are any
			$.extend( settings, options );
			
			// tag must be either input or textarea, if 'dotextarea' is true, otherwise move to next element
			// using this.tagName instead of $(this).is() because it's faster
			if ( !( this.tagName.toLowerCase()=='input' || (settings['dotextarea'] && this.tagName.toLowerCase()=='textarea') ) ) return true;
			
			// finally let's get $(this) and do one last test for placeholder value
			var $this = $(this),
				ph = this.getAttribute('placeholder'),
				ispass = $this.is('input[type=password]');		// this is used twice so I'm assigning it to a variable
			
			if (!ph) return true;
			
			// so, we have a legit tag and it has a placeholder value, let's get to work
			
			// if the input is a password field and 'dopass' is true use passPlacehold()
			if (settings['dopass'] && ispass) {
				passPlacehold($this, ph);
			}
			// in case 'dopass' was false double check it's not a password field and then
			// for both textarea and regular input the same function applies
			else if (!ispass) {
				inputPlacehold($this, ph)
			}
		});
		
		function inputPlacehold(el, ph) {
			// set as placeholder if value is empty or is equal to placeholder text
			// then use class as flag (instead of checking value)
			if ( valueEmpty(el.val()) || el.val()==ph ) {
				el.val(ph);
				el.addClass(settings['class']);
			}
			
			// setup the events for the field
			el.focusin(function(){
				if (el.hasClass(settings['class'])) {
					el.removeClass(settings['class']);
					el.val('');
				}
			});
			el.focusout(function(){
				if ( valueEmpty(el.val()) ) {
					el.val(ph);
					el.addClass(settings['class']);
				}
			});
		}
		
		function passPlacehold(el, ph) {
			el.addClass(settings['class']);
			// setup the initial placeholder, i.e. span
			var span = $('<span/>',{
				'class': el.attr('class')+' '+settings['class'],	// 'inherit' class from the input field + the placeholder class
				text: ph,
				css: {
					border:		'none',					// since inherited styles from input, "clean" them for the span: remove border
					cursor:		'text',					// give text cursor so it looks like part of the input field
					background:	'transparent',			// clear background to be transparent
					position:	'absolute',				// position the span appropriately
					top:		el.position().top,
					left:		el.position().left,
					lineHeight: el.height()+3+'px',		// needs adjustment due to extra "natural" padding of input fields
					paddingLeft:parseFloat(el.css('paddingLeft'))+2+'px'	// ditto as above
				}
			}).insertAfter(el);
			
			// setup the events for the password placeholder
			el.focusin(function(){
				if (el.hasClass(settings['class'])) {
					span.hide();
					el.removeClass(settings['class']);
				}
			});
			el.focusout(function(){
				if ( valueEmpty(el.val()) ) {
					span.show();
					el.addClass(settings['class']);
				}
			});
			
			if (settings['checkafill']) {
				// periodically check the password field for content
				// in case an auto form filler has kicked in and filled it
				// setInterval replaced by self calling function with setTimeout
				// thanks to Paul Irish for the tip http://paulirish.com/2010/10-things-i-learned-from-the-jquery-source/
				(function checkPass(){
					if (!valueEmpty(el.val()) && el.hasClass(settings['class'])) {
						el.focusin();
					}
					setTimeout(checkPass, 250);
				})();
			}
		}
		
		// does a "smart" check to see if value is empty givem allowance for multiple spaces
		function valueEmpty( value ) {
			return settings['allowspaces'] ? value==='' : $.trim(value)==='';
		}
	};
})(jQuery);