var updatebtns = document.getElementsByClassName('update-cart')

for(var i=0;i< updatebtns.length  ;i++){
    updatebtns[i].addEventListener('click', function(){
        var productId = this.dataset.product 
        var action  = this.dataset.action
        console.log('productId  : ' ,  productId   , 'Action  : ' , action)

        console.log('User  : ' , user)
        if(user=='AnonymousUser'){
            console.log('Logged in failed')
        }else{
            // console.log('User logged in!! Sending data')
            updateUserOrder(productId , action)
        }
    })
}

// function updateUserOrder(productId , action){
//     console.log('User logged in!! Sending data')
//     var url = 'update_item/'

//     fetch(url , {
//         method:'POST', 
//         header:{
//             'Content-Type':'application/json',
//             'X-CSRFToken':csrftoken,
//         },
//         body:JSON.stringify({'productId ': productId , 'Action'  : action})
//     })

//     .then((response) => {
//         return response.json()
//     })

//     .then((response) => {
//         console.log('data: ',data)
//     })
// }
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
    .then((data) => {  // Changed response to data
        console.log('data: ', data);
        location.reload()
    })
}
