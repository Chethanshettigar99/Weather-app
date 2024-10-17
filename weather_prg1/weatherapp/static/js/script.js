function showDetails(date) {
    var detailsElement = document.getElementById('details-' + date);
    var allDetails = document.getElementsByClassName('forecast-details');

    for (var i = 0; i < allDetails.length; i++) {
        if (allDetails[i] !== detailsElement) {
            allDetails[i].style.display = 'none';
        }
    }

    detailsElement.style.display = detailsElement.style.display === 'none' ? 'block' : 'none';
}
