

function connect() {
	ws =  new WebSocket(((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + "/ws");

	ws.onopen = function() {
		console.log("[open] Connection established");
	};
  
	ws.onmessage = async function(e) {
		console.log(`[message] Data received from server: ${e.data}`);
        $("#text").text(e.data)
	};
  
	ws.onclose = function(e) {
		if (e.wasClean) {
			console.log(`[close] Connection closed cleanly, code=${e.code} reason=${e.reason}`);
		} else {
			// e.g. server process killed or network down
			// event.code is usually 1006 in this case
			console.log('[close] Connection died');
		}	  setTimeout(function() {
		connect();
	  }, 1000);
	};
  
	ws.onerror = function(err) {
	  console.error('[error] Socket encountered error: ', err.message, 'Closing socket');
	  ws.close();
	};
}


$( document ).ready(function() {
    connect();
});