odoo.define('fleet_tracking.feed_vehicle_in_dropdown', function (require) {
'use strict';
      // debugger;

var publicWidget = require('web.public.widget');
// var my_model = new Model('fleet_tracking.fleet.vehicle.car.model');

publicWidget.registry.FeedVehicleInDropdown = publicWidget.Widget.extend({
    template: 'fleet_tracking.contract_booking',
    /*xmlDependencies : ['fleet_tracking/views/homepage_view.xml'],*/
    selector: '.mybutton',
    events: {
        'click .mysubmit': '_getlocation',
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */

    _getlocation: function () {
  //       const status = document.querySelector('#status');
  // const mapLink = document.querySelector('#map-link');

  // mapLink.href = '';
  // mapLink.textContent = '';
        //debugger;
        // this._rpc({
        //     model : 'fleet.vehicle.brand',
        //     method : 'abc',
        // })


        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(success);
        }else{
            console.log("not supported")
        }

        function success(position){
            const latitude  = position.coords.latitude;
            const longitude = position.coords.longitude;
            console.log("latitude="+latitude)
            console.log("longitude="+longitude)
        }
        this._rpc({
                model: 'fleet.vehicle.brand',
                method: 'abc',
                args:[]
            });

    },

});
});