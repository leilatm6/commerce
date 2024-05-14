document.addEventListener("DOMContentLoaded", function() {
    const dropdownItems = document.querySelectorAll(".dropdown-item");
    dropdownItems.forEach(function(item) {
    item.addEventListener("click", function(event) {
        event.preventDefault();
        categoryId = event.target.dataset.categoryId;
        if (categoryId !== undefined){
            fetch(`category/${categoryId}`)
                .then(response => response.text())
                    .then(html => { 
                        const tempElement = document.createElement('div');
                        tempElement.innerHTML = html;
                        const specificContent = tempElement.querySelector('#indexcontainer').innerHTML;
                        document.getElementById("index-content-container").innerHTML = specificContent;
                    })
                    .catch(error => {
                                console.error("Error fetching data:", error);
                            });
        }
        else{
            fetch(`/`)
            .then(response => response.text())
                .then(html => { 
                    const tempElement = document.createElement('div');
                    tempElement.innerHTML = html;
                    const specificContent = tempElement.querySelector('#indexcontainer').innerHTML;
                    document.getElementById("index-content-container").innerHTML = specificContent;
                    })
                    .catch(error => {
                                console.error("Error fetching data:", error);
                            });
        }



                });

    });
});

