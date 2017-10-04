#!/usr/bin/env node

var port = 3000;
var express = require('express');
var serveStatic = require('serve-static');
var bodyParser = require('body-parser');
var Highcharts = require('highcharts');
var app = express();

app.use(express.static(__dirname + '/public'));
app.use(express.static(__dirname + '/bower_components'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
//app.use(db.establish(config.db_config));

app.listen(port, function() {
    console.log('Server listening on port ' + port + '.');
});

