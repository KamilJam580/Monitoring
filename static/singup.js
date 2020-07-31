$(document).ready(function(){
    var user = 'xx';
    var pas = '123';
    alert(user);
	$('#button').click(function(e){
		user = $('#login').val();
		pass = $('#password').val();
		$.ajax({
			url: '/camerasPreview',
			data: {
			    login: user,
			    password: pass
			},
			type: 'GET',
			success: function(response){
			    $("#camerasPanel").html(response);
			    $("#loginPanel").text("Logged as: " + user);
			},
			error: function (request, status, error) {
                alert(error);
             }
		});
		e.preventDefault();
	});

	$('#showLoginB').click(function(e){
	    $("#showLogin").text(user);
	});
});