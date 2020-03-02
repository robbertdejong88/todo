$("#id_user").keyup(function () {
  var user = $(this).val();

  $.ajax({
    url: url_show_users,
    data: {
      'user': user
    },
    dataType: 'json',
      success: function (data) {
        html = ''
        for(var i = 0; i < data.length; i++){
          var id = data[i].pk;
          var name = data[i].fields.username;
          html = html + "<tr><td>"+name+"</td><td><a href='#' id='addfriend' uid='"+id+"'><i class='fas fa-user-plus'></i></a></td></tr>"
        }
        document.getElementById('table_body').innerHTML = (html);
      }
  });
});




$("body").on('click', '#addfriend',function (e) {
  var value = $(this).attr("uid");
  
  $.ajax({
        url: url_add_user,
        type: "post", // or "get"
        data: value,
        success: function(data) {

            alert(data.result);
            document.getElementById("id_user").focus();
            document.getElementById("id_user").select();
        }});

});