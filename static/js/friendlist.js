$("#id_user").keyup(function () {
  var user = $(this).val();

  $.ajax({
    url: "/show-users",
    data: {
      'user': user
    },
    dataType: 'json',
      success: function (data) {
       	html = ''
       	for(var i = 0; i < data.length; i++){
       		var id = data[i].pk;
       		var name = data[i].fields.username;
       		html = html + "<tr><td>"+name+"</td><td><a href='#' ><i class='fas fa-user-plus'></i></a></td></tr>"
      	}
       	document.getElementById('table_body').innerHTML = (html);
      }
  });
});