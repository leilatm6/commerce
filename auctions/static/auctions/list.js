document.addEventListener('DOMContentLoaded', function() {

    if (section == "bid"){
        document.getElementById('sectionbid').scrollIntoView({
            behavior: 'smooth'
        })
    }
    
    var textarea = document.getElementById('floatingTextarea')
    let commentbut = document.getElementById('commentbutton')
    const productid = commentbut.dataset.product;
    commentbut.addEventListener('click', (event)=>{
        event.preventDefault();
        
        console.log('hiiiiiiiiiiiiiiigiiiiiiiiiiii')
        fetch('/createcomment',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({id: productid, textarea: textarea.value})
        })
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
    })

    let closebut = document.getElementById('closeauction')
    if (closebut){
        closebut.addEventListener('click', (event)=>{
            event.preventDefault();
            const productid = closebut.dataset.product;
            fetch('/closelist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({id: productid})
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
    document.getElementById('floatingTextarea').addEventListener('keyup',(event)=>{
        if (textarea.value.length === 0 ){
            commentbutton.disabled = true;
        }
        else{
            commentbutton.disabled = false
        }

    })
    


});