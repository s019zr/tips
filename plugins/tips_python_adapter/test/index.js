/**
 * Created by Mikael Lindahl on 2017-03-20.
 */

'use strict';

'use strict';


let Code = require( 'code' );   // assertion library
let Lab = require( 'lab' );
let debug = require( 'debug' )('tips:tips_python_adapter:test:index');
let adapter = require('../index');
let path = require('path')

require('dotenv').config({
    path:'./testenv'
});

let lab = exports.lab = Lab.script();


lab.experiment( 'test tips python adapter', ()=> {


    lab.test( 'skapinfra', function ( done ) {

        let options = {
            arguments: [path.join(__dirname, '/data/T17.tdf')],
            file: 'SkapaInfra.py'
        };

        debug( 'test' )

        adapter.run( options )
            .then( result => {

                debug( result )
                done()

            } ).catch( err => {

            console.error( err )
            done()
        } )
    })
});