window.addEventListener('DOMContentLoaded', (event) => {
  document.getElementById('btn_check').addEventListener('click',
    function () {
      var xhttp = new XMLHttpRequest();
      var url = 'http://localhost:5000/get-url';
      var url_to_check = document.getElementById("url_text").value;
      var params = "url=" + url_to_check ;
      xhttp.open("POST", url, true);
      xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      xhttp.onreadystatechange = function () {
        //document.getElementById("btn_check").setAttribute("enabled");
        document.getElementById("btn_check").innerHTML = "Kiểm tra"
        if (this.readyState == 4 && this.status == 200) {
          var result = this.response
          if (result == 0) {
            document.getElementById("alert").innerHTML = "Cảnh báo phishing !!!"
            document.getElementById("alert").style.background = "red";

          } else if (result == 1){
            document.getElementById("alert").innerHTML = "An toàn"
            document.getElementById("alert").style.background = "#80ff80";
          }
        }
      };
      xhttp.send(params);
      document.getElementById("btn_check").innerHTML = "Đang kiểm tra"
    });
}
);
