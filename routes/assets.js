


'use strict';

const debug = require( 'debug' )( 'breakpad:crash_dump.js' )


module.exports = [

    // This route is required for serving assets referenced from our html files
    {
        method: 'GET',
        path: '/',
        handler: function ( request, reply ) {

            reply.view( 'index' );

        }
    },

    // This route is required for serving assets referenced from our html files
    {
        method: 'GET',
        path: '/{files*}',
        handler: {
            directory: {
                path: 'public'
            }
        }
    },

];
