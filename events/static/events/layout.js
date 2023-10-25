document.addEventListener("DOMContentLoaded", function() {
    const element=document.getElementById("datetimepicker1");
    element.style.display="none";
    const cal=document.getElementById("calender");
    cal.addEventListener("click",function(){
        element.style.display="block";
        const input = document.getElementById("datepicker");
        const picker = new Pikaday({
            field: input,
            format: "MM/DD/YYYY", // Customize the date format as needed
            yearRange: [1900, new Date().getFullYear()], // Set the range of years
            // You can customize other options as well
        });
        picker.show();
        input.addEventListener("change",function(){
            element.style.display="none";
            console.log(input.value);
            const str=input.value.split(" ");
            console.log(str);
            const dsss=document.getElementById("container");
            dsss.style.display="none";
            const cardss=document.getElementById("showwcards");
            cardss.innerHTML="<h2>Events🧾</h2>";
            cardss.style.display="block";
            fetch("/get_events", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken") 
                },
                body: JSON.stringify({
                    date: input.value,
                })
            }).then(response => response.json()).then(result => {
                result.events.forEach(event => {
                console.log(result);
                const card=document.createElement('div');
                card.setAttribute('class','card_body');
                card.setAttribute('data-name',event.title);
                card.setAttribute('data-custom-property1',event.description);
                card.setAttribute('data-custom-property2',event.category);
                card.setAttribute('data-custom-property3',event.date);
                card.innerHTML=`<h3>${event.title}</h3>
                <span>
                    <img src="${event.image}" alt="${event.title}">
                </span>
                <p>Ticket Price: ₹${event.ticket_price}/-</p>
                <p>Club: ${event.club}</p>
                <a href="/event/${event.id}"  class="btn btn-primary" >View</a>`;
                cardss.append(card);
             });
            }).catch(error => {
                console.log("Error:", error);
            });
            })
        });
     });

     

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
    

