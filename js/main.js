$ = require('jquery');

console.log("Running summit scraper version 3.");


$.ajax("./../data/summitpost.json", {
    dataType: "json",
    success: function(data) {
        d = JSON.parse(data)
        console.log(d);
    },
    beforeSend: function() {
        console.log("Sending request.")
    },
    error: function(xhr, status, error) {
        console.log(xhr.responseText)
        console.log(status)
        console.log(error)
        console.log("error")
    }
})