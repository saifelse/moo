define ['views/sky', 'models/puzzles'], (SkyView, puzzles) ->
  class ScavengerHuntView extends Backbone.View

    el: 'body'

    initialize: ->
      @puzzles = new puzzles.Collection()
      @skyView = new SkyView(el: @$('#sky'), collection: @puzzles)
      return

    registerListeners: ->
      @listenTo @puzzles, 'open', @open
      return

    open: (model) ->
      @$('#puzzle .title').text("Level #{model.get('level')}: #{model.get('name')}")
      @$('#puzzle .content').html(model.get('html'))
      return

    render: ->
      @registerListeners()
      @skyView.render()
      @
