define [], ->
  console.log 'hello?'
  class Router extends Backbone.Router
    routes:
      '': 'home'

    initialize: ->
      console.log 'initializsing'

    home: ->
      console.log 'Displaying home!'