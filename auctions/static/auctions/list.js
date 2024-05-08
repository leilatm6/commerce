


document.addEventListener('DOMContentLoaded', function() {
    console.log(section)
    if (section == "bid"){
        document.getElementById('sectionbid').scrollIntoView({
            behavior: 'smooth'
        })
    }
    


    let closebut = document.getElementById('closeauction')
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
            console.log(data);
            const modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
            modal.hide();
            // Refresh the page
            window.location.reload();
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    });
});


