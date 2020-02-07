odoo.define('fleet_tracking.feed_vehicle_in_dropdown', function (require) {
'use strict';
      // debugger;

var publicWidget = require('web.public.widget');

publicWidget.registry.FeedVehicleInDropdown = publicWidget.Widget.extend({
    template: 'fleet_tracking.odometer',
    /*xmlDependencies : ['fleet_tracking/views/homepage_view.xml'],*/
    selector: '.mybutton',
    events: {
        'click .mysubmit': '_onfeeddata',
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */

    _onfeeddata: function () {
        
        //debugger;
        console.log("*****************")

    },

});
});