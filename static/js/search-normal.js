document.getElementById('searchButton').addEventListener('click', function(event) {
    event.preventDefault();

    const origin = document.getElementById('origin').value;
    const end = document.getElementById('final-destination').value;
    const min_price = document.getElementById('min-price').value;
    const max_price = document.getElementById('max-price').value;
    const dept_date = document.getElementById('departure-date').value;
    const ret_date = document.getElementById('return-date').value;

    const query_string = `fromEntityId=${origin}&toEntityid=${end}&min_price=${min_price}&max_price=${max_price}&depart=${dept_date}&return_date=${ret_date}`;

    window.location.href = `search-result-normal-flight?${query_string}`;
})