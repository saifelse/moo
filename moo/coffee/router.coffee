define ['views/scavenger-hunt'], (ScavengerHuntView) ->

  class Router extends Backbone.Router
    routes:
      '': 'home'

    home: ->
      new ScavengerHuntView().render()
