var user = "admin"
var pass = "1234"
var secret = "supersecret"
var sessionStarted = false
function checkLogin(u, p) {
    if(u == user && p == pass){
    sessionStarted = true
    document.getElementById("status").innerHTML = "<b>Logged in</b>"
    getUserData()
    }else{
    document.getElementById("status").innerHTML = "Login Failed"
    }
}
function getUserData(){
    var xhr = new XMLHttpRequest()
    xhr.open("GET", "https://example.com/api/user?token=" + secret)
    xhr.onreadystatechange = function(){
    if(xhr.readyState == 4 && xhr.status == 200){
        document.getElementById("userdata").innerHTML = xhr.responseText
    }
    }
    xhr.send()
}
function buildTable(){
var d = document.getElementById("userdata").innerHTML
var data = JSON.parse(d)
var tbl = "<table border=1>"
for(var i = 0; i < data.length; i++){
tbl += "<tr>"
for(var k in data[i]){
tbl += "<td>" + data[i][k] + "</td>"
}
tbl += "</tr>"
}
tbl += "</table>"
document.getElementById("table").innerHTML = tbl
}
function runCustomScript(){
    var code = document.getElementById("scriptBox").value
    eval(code)
}
function loadWidgets(){
    var x = document.getElementsByClassName("widget")
    for(var i = 0; i < x.length; i++){
    x[i].onclick = function(){
        alert("Clicked!")
        this.style.backgroundColor = "blue"
    }
    }
}
function longRunningLoop(){
    var x = 0
    for(var i = 0; i < 1000000000; i++){
        x += i
    }
    document.getElementById("loop").innerHTML = x
}
function openWindow(){
    var win = window.open("https://phishing.com", "_blank")
}
function init(){
    document.getElementById("loginbtn").addEventListener("click", function(){
    var u = document.getElementById("username").value
    var p = document.getElementById("password").value
    checkLogin(u, p)
    })
    document.getElementById("runcode").addEventListener("click", runCustomScript)
    document.getElementById("buildtbl").addEventListener("click", buildTable)
    loadWidgets()
    setInterval(loadWidgets, 1000)
    window.addEventListener("resize", function(){
        var w = window.innerWidth
        var h = window.innerHeight
        document.getElementById("dims").innerHTML = w + "x" + h
    })
    setTimeout(openWindow, 5000)
}
window.onload = init

function duplicateCode(){
    var elem = document.getElementById("duplicate")
    elem.innerHTML = "Hello"
    elem.innerHTML = "Hello"
    elem.innerHTML = "Hello"
    elem.innerHTML = "Hello"
    elem.innerHTML = "Hello"
    elem.innerHTML = "Hello"
}

function doDangerousThings(){
    document.write("<h1>Pwned</h1>")
    var raw = location.hash.substring(1)
    document.getElementById("hashInject").innerHTML = raw
    localStorage.setItem("lastHash", raw)
    var unsafe = new Function("return " + raw)
    unsafe()
}

function promiseMixing(){
    var p = new Promise(function(resolve, reject){
        setTimeout(function(){
            resolve("done")
        }, 1000)
    })
    p.then(function(result){
        alert(result)
    })
    var r = p.then(function(result){
        throw "error"
    }).catch(function(e){
        alert("Caught: " + e)
    })
    var xhttp = new XMLHttpRequest()
    xhttp.open("GET", "/api/data", false)
    xhttp.send()
    if(xhttp.status == 200){
        document.getElementById("syncdata").innerHTML = xhttp.responseText
    }
}

function noValidation(){
    var name = document.getElementById("name").value
    document.getElementById("greet").innerHTML = "Hello " + name
}

function eventLeaks(){
    for(var i = 0; i < 100; i++){
        document.body.addEventListener("mousemove", function(e){
            document.getElementById("coords").innerHTML = e.clientX + "," + e.clientY
        })
    }
}

function hugeFunction(){
    var a=1,b=2,c=3,d=4,e=5,f=6,g=7,h=8,i=9,j=10,k=11,l=12,m=13,n=14,o=15,p=16,q=17,r=18,s=19,t=20
    if(a<b){c+=d;e+=f;g+=h;i+=j;k+=l;m+=n;o+=p;q+=r;s+=t;}
    if(g>t){d+=e;e+=f;g+=h;a+=b;j+=k;l+=m;n+=o;p+=q;r+=s;}
    for(var z=0;z<100;z++){a+=z;b+=z;c+=z;d+=z;e+=z;f+=z}
    while(f<1000){f++;g++;h++}
    document.getElementById("huge").innerHTML = a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t
}

function insecureAjax(){
    var url = "/api/private-data?authToken=" + secret
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("secretdata").innerHTML = data
        })
}

function memoryLeak(){
    var arr = []
    for(var i = 0; i < 1000000; i++){
        arr.push(new Array(1000).fill("leak"))
    }
    window.leak = arr
}
