document.addEventListener('DOMContentLoaded', function() {
  

    if (section == "bid"){
        document.getElementById('sectionbid').scrollIntoView({
            behavior: 'smooth'
        })
    }
    //Comment Section
    var textarea = document.getElementById('floatingTextarea')
    let commentbut = document.getElementById('commentbutton')
    commentbut.addEventListener('click', (event)=>{
        event.preventDefault();
        fetch('/createcomment',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({id: product_id, textarea: textarea.value})
        })
        .then(response => response.json())
        .then(data => {
            window.location.reload();   
        })
    })

    document.getElementById('floatingTextarea').addEventListener('keyup',(event)=>{
        if (textarea.value.length === 0 ){
            commentbutton.disabled = true;
        }
        else{
            commentbutton.disabled = false
        }

    })


    //CloseAuction
    let closebut = document.getElementById('closeauction')
    if (closebut){
        closebut.addEventListener('click', (event)=>{
            event.preventDefault();
            fetch('/closelist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({id: product_id})
            })
            .then(response => response.json())
            .then(data => {
                //console.log(data);
                const modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
                modal.hide();
                // Refresh the page
                window.location.reload();
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        });
    }


//watchlist
let watchlistbut = document.getElementById("watchlistbutton")
watchlistbut.addEventListener('click',(event)=>{
    event.preventDefault()
    fetch('/watchlist',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({id: product_id})     
    })
    .then(response => response.json())
    .then(data => {
        console.log(data) 
        watchlistbut.innerHTML =data.iswatchlist? `watchlist <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" style ="color:red" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
      </svg>`:`watchlist <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" style ="color:red" viewBox="0 0 16 16">
      <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
    </svg>`
        
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });

})

})