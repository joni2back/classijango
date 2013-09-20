$(function() {

	var fields = {};
    fields.city = $('#contact_city');
    fields.cityId = $('#id_contact_city');

    fields.city.typeahead({
        items: 15,
        minLength: 3,
        source: function (query, process) {
            return $.post('/api/json/location/cities/', {"cityName": query}, function (data) {
                fields.city.citiesName = [];
                fields.city.citiesId = {};
                $.each(data, function (i, city) {
                    fields.city.citiesName.push(city.name);
                    fields.city.citiesId[city.name] = city.id;
                });
                return process(fields.city.citiesName);
            });
        }
        ,updater: function (item) {
            var value = fields.city.citiesId[item];
            fields.cityId.val(value);
            return item;
        }
    });

});