// access_control

$(document).ready(function() {

	var enableWait = false;

	function updates()
	{
		if (enableWait)
			updateWait();
	}

	var updatePipe = setInterval(updates, 5000);

	function clickEnter()
	{
		 $.ajax
		 ({
		 	type: "GET",
		 	url: '/ServicePlatform?eid=' + window.conf.id + '&t=token',
		 	dataType: 'json',
		 	async: false,
		 	success: function (resultData) {

		 		if (resultData.error != undefined)
		 		{
		 			alert(resultData.error)
		 			return ;
		 		}

		 		var token = resultData.token_value;

		 		//console.log(token)
		 		window.conf.token = token

		 		if (token != null)
		 		{
		 			display("#wait")
		 			enableWait = true // mislim da je visak
		 		} else
		 		{
		 			alert("Trenutno nije moguce pristupiti u red, pokusajte kasnije!")
		 		}
		 	}
		 })
	}


	function clickAccess()
	{
		window.location.href = window.conf.location + "/?stoken=" + window.conf.token
	}


	function updateWait()
	{
		$.ajax
		 ({
		 type: "GET",
		 url: '/ServicePlatform?eid=' + window.conf.id + '&t=info&token=' + window.conf.token,
		 dataType: 'json',
		 async: false,
		 success: function (resultData) {
		 	if (resultData.error != undefined)
		 	{
		 		alert(resultData.error)

		 		return ;
		 	}

		 	var position = resultData.value.position + 1
		 	var queue = resultData.value.queue

		 	console.log(resultData)

		 	if (position == 1)
		 	{
		 		display("#access")
		 		enableWait = false // mozda nepotrebno
		 	} else if (position == 0)
		 	{
		 		display("#enter")
		 		enableWait = false // mozda nepotrebno
		 	} else if (position > 1)
		 	{
		 		$("#wait").text("Wait..." + "(" + position + "/" + queue + ")")
		 	}
		 }
		 })
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