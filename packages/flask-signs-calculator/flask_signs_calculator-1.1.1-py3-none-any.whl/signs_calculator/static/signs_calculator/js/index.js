function setCitiesAutocomplete() {
  let countryCode = $('#country').val();
  $.get(`/geo/api/v1/cities/${countryCode}`, function(data, status) {
    $('#city').autocomplete({source: data});
  });
}

$('#country').change(setCitiesAutocomplete);

setCitiesAutocomplete();
