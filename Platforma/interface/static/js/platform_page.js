// access_control

$(document).ready(function() {

	var enableWait = false;

	function updates()
	{
		if (enableWait)
			updateWait();
	}

	var updatePipe = setInterval(updates, 1000);

	function requestEnterQueue()
	{
		var response = {status:"ok"}

		return response
	}

	var i = 10 // @test
	function checkQueue()
	{
		var response = {queueSize: 10, position: i}

		if (i != 1)
			i--;

		return response
	}


	function clickEnter()
	{
		alert("ENTER QUEUE");

		if (requestEnterQueue().status == "ok")
		{
			display("#wait")
			enableWait = true
		}
	}


	function clickAccess()
	{
		window.location.href = window.conf.location
	}


	function updateWait()
	{
		var data = checkQueue();

		if (data.position == 1)
		{
			display("#access")
		} else if (data.position == -1)
		{
			display("#enter")
		} else if (data.position > 1)
		{
			$("#wait").text("Wait..." + "(" + data.position + "/" + data.queueSize + ")")
		}
	}


	function display(name)
	{
		switch(name)
		{
			case "#wait":
				$("#wait").css({"display": "block"})
				$("#access").css({"display": "none"})
				$("#enter").css({"display": "none"})
				break;
			case "#access":
				$("#wait").css({"display": "none"})
				$("#access").css({"display": "block"})
				$("#enter").css({"display": "none"})
				break;
			case "#enter":
				$("#wait").css({"display": "none"})
				$("#access").css({"display": "none"})
				$("#enter").css({"display": "block"})
		}
	}


	$("#enter").click(clickEnter)
	$("#access").click(clickAccess)
})