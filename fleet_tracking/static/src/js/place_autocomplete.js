/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
*/
odoo.define('fleet_tracking.place_autocomplete', function(require){

    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');
    var MapWidget = require('fleet_tracking.map_widget');


    var place_autocomplete = basic_fields.FieldChar.extend({
        init: function(parent, name, record, options){
            this._super.apply(this, arguments);
            this.lat = 23.1954836;
            this.lng = 72.62693209999999;
            console.log("----")
    //     if(navigator.geolocation){
    //         navigator.geolocation.getCurrentPosition(success);
    //     }else{
    //         console.log("not supported")
    //     }

    //     function success(position){
    //         var latitude  = position.coords.latitude;
    //         var longitude = position.coords.longitude;

    //          var la = parseFloat(latitude);
    // var ln = parseFloat(longitude);
    //             console.log("latitude="+la)
    //         console.log("longitude="+ln)
    //         this.lat = eval(la);
    //         this.lng = eval(ln);
    //     }

        },
        start: function(){
            var self = this;
            console.log("----1")

            return this._super.apply(this, arguments).then(function () {
                self.t = setInterval(function () {
                    if (typeof google != 'undefined') {
                        self.on_ready();
                    }
                }, 1000);
            });
        },
        on_ready: function(){
            var self = this;
            console.log("----2")

            if(self.t){
                clearInterval(self.t);
            }

            if (!self.$input) {
                return;
            }

            var map_widget = new MapWidget(self);
            map_widget.insertAfter(self.$input);

            // init gmap marker position
            var geocoder = new google.maps.Geocoder;
            geocoder.geocode({'address': self.$input.val()}, function (results, status) {
                if (status === 'OK') {
                    self.lat = results[0].geometry.location.lat();
                    self.lng = results[0].geometry.location.lng();
                    map_widget.lat = self.lat;
                    map_widget.lng = self.lng;
                }
            });

            var autocomplete = new google.maps.places.Autocomplete((self.$input[0]), {types: ['geocode']});

            autocomplete.addListener('place_changed', function (){
                var place = autocomplete.getPlace();
                
                if(!place.geometry || !place.geometry.location){
                    return;
                }

                var location = place.geometry.location;

                console.log("+++"+location.lat());
                console.log("+++"+location.lng());
                self.lat = location.lat();
                self.lng = location.lng();
                // update gmap
                map_widget.update_marker(self.lat, self.lng);
            });

        },
        update_place: function (lat, lng) {
        debugger;
            
            var self = this;
            if (lat === this.lat && lng === this.lng) {
                return;
            }
            console.log("+++1=="+lat);
            console.log("+++1=="+lng);
            this.lat = lat;
            this.lng = lng;
            // console.log( self.$el.filter('.latitude')[0].value)
             // self.$el.filter('.latitude')
            var geocoder = new google.maps.Geocoder;
            var latLng = new google.maps.LatLng(lat, lng);
            geocoder.geocode({'location': latLng}, function (results, status) {
                if (status === 'OK') {
                    if (self.$input) {
                         console.log("+++1=="+results[0].formatted_address);

                        self.$input.val(results[0].formatted_address);
                        self._doAction();
                    }
                }
            });
        }
    });

    registry.add('place_autocomplete', place_autocomplete);
});