define ['views/scavenger-hunt'], (ScavengerHuntView) ->
  console.log 'hello?'
  class Router extends Backbone.Router
    routes:
      '': 'home'

    home: ->
      new ScavengerHuntView().render()