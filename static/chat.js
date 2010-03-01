(function($) {
	var nick;
	
	$(function() {
		$('#nick').focus();
		$('#register').submit(function() {
			nick = $('#nick').val();
			
			var ws = new WebSocket('ws://localhost:8000/message');
			ws.onopen = function() {
				ws.send('nick: ' + nick);
			};
			ws.onmessage = function(e) {
				var message = e.data;
				if (message.length > 9 && message.slice(0, 9) == 'new_user:') {
					message = message.slice(9).trim();
					$('#online_users').append('<div id="' + message +'">' + message + '</div>');
				} else if(message.length > 12 && message.slice(0, 12) == 'remove_user:') {
					var remove_nick = message.slice(12).trim();
					$('#' + remove_nick).remove();
				} else {
					$('#chat').append('<div>' + e.data + '</div>').scrollTop($('#chat').innerHeight());
				}
			};
			
			$(window).bind('beforeunload', function() {
				ws.send('close');
			});
			
			$('#register').remove();
			$('body').prepend('<h1>Hello: ' + nick + '!</h1><div id="chat" /><div id="online_users" /><div class="clear" /><form id="message_form"><input type="text" name="message" id="message" /><input type="submit" value="Send"></form>');
			$('#message').focus();
			$('#message_form').submit(function() {
				ws.send('message:' + $('#message').val());
				$('#message').val('').focus();
				
				return false;
			});
			
			return false;
		});
	});
})(jQuery);
