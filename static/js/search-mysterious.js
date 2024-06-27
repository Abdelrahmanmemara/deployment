

document.getElementById('searchButton').addEventListener('click', function(event) {
    event.preventDefault();

    const origin = document.getElementById('origin').value;
    const min_price = document.getElementById('min-price').value;
    const max_price = document.getElementById('max-price').value;
    const dept_date = document.getElementById('departure-date').value;
    const ret_date = document.getElementById('return-date').value;

    const query_string = `fromEntityId=${origin}&min_price=${min_price}&max_price=${max_price}&depart=${dept_date}&return_date=${ret_date}`;

    console.log('Origin:', origin);
    console.log('Min Price:', min_price);
    console.log('Max Price:', max_price);
    console.log('Departure Date:', dept_date);
    console.log('Return Date:', ret_date);

    window.location.href = `search-result-mysterious-flight?${query_string}`;
})