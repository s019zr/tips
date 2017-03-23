/**
 * Created by Mikael Lindahl on 2017-03-20.
 */

'use strict';

var debug = require('debug')('tips:tips_python_adapter:index');
var PythonShell = require('python-shell');
var path = require('path');
var Promise = require('bluebird');


function run(options){

    return new Promise((resolve, reject)=>{

        debug('run')

        var pyshell = new PythonShell( options.file,
            {
                pythonPath:process.env.PYTHON_EXECUTABLE,
                scriptPath:path.join(__dirname,'./python'),
                args:options.arguments
            });

        var result=[];
        // sends a message to the Python script via stdin
        // pyshell.send(options.arguments.join(' '));

        pyshell.on('message', function (message) {
            // received a message sent from the Python script (a simple "print" statement)
            debug(message);

            result.push(message)

        });

        // end the input stream and allow the process to exit
        pyshell.end(function (err) {
            if (err) reject( err );
            debug('finished');

            resolve(result)

        });

    })
}

module.exports={

    "run":run

};