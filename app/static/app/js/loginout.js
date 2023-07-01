var div = document.getElementById('log-infor')
var li = document.getElementById('log-regis')
var liin = document.getElementById('log-in')

if (user === "AnonymousUser"){
    div.style.display = 'none'
    li.style.display = ''
    liin.style.display = ''
}
else{
    div.style.display = ''
    li.style.display = 'none'
    liin.style.display = 'none'
}