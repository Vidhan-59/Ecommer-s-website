var updatebtns = document.getElementsByClassName('update-cart')

for(var i=0;i< updatebtns.length  ;i++){
    // console.log('hey')
    updatebtns[i].addEventListener('click', function(){
        var productId = this.dataset.product 
        var action  = this.dataset.action
        console.log('productId  : ' ,  productId   , 'Action  : ' , action)

        console.log('User  : ' , user)
        if(user=='AnonymousUser'){
            addCookieItem(productId , action)
        }else{
            updateUserOrder(productId , action)
        }
    })
}
function addCookieItem(productId , action){
    // console.log('Logged in failed...') 
    
    console.log("hello")
    if(action == 'add'){
        if(cart[productId]==undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log("Cart  :", cart)
    document.cookie =  'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}


function updateUserOrder(productId , action){
    console.log('User logged in!! Sending data');
    var url = '/update_item/';

    fetch(url , {
        method: 'POST', 
        headers: {  // Corrected 'header' to 'headers'
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'Action': action })  // Corrected 'productId ' to 'productId'
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data: ', data);
        location.reload()
    })
}
