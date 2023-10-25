document.addEventListener('DOMContentLoaded', function() {
    const element=document.getElementById('buy_button');
   const wishlister=document.getElementById('wishlist');
   wishlister.addEventListener('click', function() {
       console.log('wishlist button clicked');
       const users=document.getElementById(cards)
       try{
       if (users.dataset.user !== null){
       fetch('/wishlist', {
           method: 'POST',
           headers: {
               "Content-Type": "application/json",
               "X-CSRFToken": getCookie("csrftoken") 
           },
           body: JSON.stringify({
               id: element.dataset.id,
           })
       }).then(response => response.json()).then(result => {
           console.log(result);
           alert(result.message);
           if (result.message === 'Added to wishlist') {
               document.getElementById('wishlist').style.fill='red';
           } else {
               document.getElementById('wishlist').style.fill='black';
           }
       }).catch(error => {
           console.log('Error:', error);
       });
       window.location.reload();
    }
}catch(error){
    console.log("catched error");
    window.location.href="/login";
}
    
   });

   const buy=document.getElementById('buy_button');
   buy.onclick=function(){
       console.log('buy button clicked');
       const users=document.getElementById(cards)
       try{
        if(users.dataset.user !== null){
            fetch('/orders',{
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken") 
                },
                body: JSON.stringify({
                    id: buy.dataset.id,
                    quantity: 1
                })
            }).then(response => response.json()).then(result => {
                console.log(result);
                alert(result.message);
            }).catch(error => {
                console.log('Error:', error);
            });
        }
       }catch(error){
        console.log("catched error");
        window.location.href="/login";
       }
   }

});


// Get the CSRF token from the cookie
function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       var cookies = document.cookie.split(';');
       for (var i = 0; i < cookies.length; i++) {
           var cookie = cookies[i].trim();
           // Search for the CSRF cookie name
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}

