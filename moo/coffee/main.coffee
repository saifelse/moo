require.config
  urlArgs: "bust=#{(new Date()).getTime()}"
  paths:
    jade: '../lib/jade/jade'
    jquery: '../lib/jquery/jquery.min'
    underscore: '../lib/underscore/underscore'
    backbone: '../lib/backbone/backbone'
    bootstrap: '../lib/bootstrap/js/bootstrap'
  shim:
    jquery:
      exports: '$'
    underscore:
      exports: '_'
    backbone:
      deps: ['underscore']
    bootstrap:
      deps: ['jquery']
    router:
      deps: ['backbone', 'bootstrap']

require ['router'], (Router) ->
  new Router()
  Backbone.history.start({pushState: true})
