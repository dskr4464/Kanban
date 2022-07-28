function changefunction() {
    var isChecked = document.getElementById('Switch{{ y.card_id | tojson | safe }}').checked;

    if(isChecked){
      document.getElementById('header{{ y.card_id | tojson | safe }}').style.backgroundColor = 'green' ;
      var x = new XMLHttpRequest();
      x.open("POST", '/user/{{ user.user_id | tojson | safe }}/{{ y.card_id | tojson | safe }}/1/flag', true);
      x.setRequestHeader('Content-Type', 'application/json');
      x.send(JSON.stringify({
          value: '1'
      }));
    } else {
      document.getElementById('header{{ y.card_id | tojson | safe }}').style.backgroundColor = 'yellow' ;
      var x = new XMLHttpRequest();
      x.open("POST", '/user/{{ user.user_id | tojson | safe }}/{{ y.card_id | tojson | safe }}/0/flag', true);
      x.setRequestHeader('Content-Type', 'application/json');
      x.send(JSON.stringify({
          value: '0'
      }));
      }
      
  }
  function loaded() {
    var x = '{{ y.completed_flag | tojson | safe }}';
      console.log(x);
    if(x==1){
      document.getElementById('header{{ y.card_id | tojson | safe }}').style.backgroundColor = 'green' ;
    } else {
      document.getElementById('header{{ y.card_id | tojson | safe }}').style.backgroundColor = 'yellow' ;
      }

  }         

                                  function validate3(event){
                                    var a = document.getElementById("vname{{ y.card_id | tojson | safe }}").value;
                                    if(a!=""){
                                    event.preventDefault();
                                    var url = "/user/"+{{user.user_id}}+"/find/"+a;
                                  
                                    fetch(url).then(function(response) {
                                      console.log(response.status);
                                      if(response.status==200){
                                        console.log(1);
                                        event.target.onclick  = null;
                                        event.target.click();
                                      }
                                      else{
                                        console.log(-1);
                                        var x = document.getElementById("c2name{{ y.card_id | tojson | safe }}");
                                        x.innerHTML = "Please enter a valid list name";
                                      }
                                    });
                                  }
                                  }
                                  function validate4(event){
                                    var a = document.getElementById("input{{ x.list_id | tojson | safe}}").value;
                                    if(a!=""){
                                    event.preventDefault();
                                    var url = "/user/"+{{user.user_id}}+"/find/"+a;
                                  
                                    fetch(url).then(function(response) {
                                      console.log(response.status);
                                      if(response.status==202){
                                        console.log(1);
                                        event.target.onclick  = null;
                                        event.target.click();
                                      }
                                      else{
                                        console.log(-1);
                                        var x = document.getElementById("c3name{{ x.list_id | tojson | safe}}");
                                        x.innerHTML = "Please enter a valid list name";
                                      }
                                    });
                                  }
                                  }
                                  function validate2(event){
                                    var a = document.getElementById("input").value;
                                    if(a!=""){
                                    event.preventDefault();
                                    var url = "/user/"+{{user.user_id}}+"/find/"+a;
                                  
                                    fetch(url).then(function(response) {
                                      console.log(response.status);
                                      if(response.status==202){
                                        console.log(1);
                                        event.target.onclick  = null;
                                        event.target.click();
                                      }
                                      else{
                                        console.log(-1);
                                        var x = document.getElementById("bname");
                                        x.innerHTML = "Please enter a valid list name";
                                      }
                                    });
                                  }
                                  }
                                  function validate1(event){
                                    var a = document.getElementById("myinput{{ x.list_id | tojson | safe }}").value;
                                    if(a!=""){
                                    event.preventDefault();
                                    var url = "/user/"+{{user.user_id}}+"/find/"+a;
                                  
                                    fetch(url).then(function(response) {
                                      console.log(response.status);
                                      if(response.status==200){
                                        console.log(1);
                                        event.target.onclick  = null;
                                        event.target.click();
                                      }
                                      else{
                                        console.log(-1);
                                        var x = document.getElementById("cname{{ x.list_id | tojson | safe }}");
                                        x.innerHTML = "Please enter a valid list name";
                                      }
                                    });
                                  }
                                  }