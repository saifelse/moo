define ['views/sky', 'models/puzzles'], (SkyView, puzzles) ->
  class ScavengerHuntView extends Backbone.View
    el: 'body'
    initialize: ->
      @puzzles = new puzzles.Collection()
      @skyView = new SkyView(el: @$('#sky'), collection: @puzzles)

    render: ->
      @skyView.render()
      @
