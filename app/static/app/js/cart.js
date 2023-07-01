var updataBtns = document.getElementsByClassName('update-cart')

for (i=0; i < updataBtns.length; i++){
    updataBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, 'action', action)
        if (user === "AnonymousUser"){
            console.log('user not logged in')
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('user logged in, susccess add')
    var url = '/update_item/'
    fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json
    })
    .then((data) => {
        console.log('data:',data)
        location.reload()
    })
}