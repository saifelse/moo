define ['views/level-row'], (LevelRowView) ->
  class SkyView extends Backbone.View
    initialize: ->
      @listenTo(@collection, 'add', @addLevelRow)

    addLevelRow: (model, collection, options) ->
      console.log 'ADDING LEVEL ROW'
      @$('table tbody').append(new LevelRowView(model: model).render().el)

    render: ->
      $tbody = @$('table tbody')
      $tbody.empty()

      # TODO: show loading message.

      @collection.fetch()
        .done (e) =>
          console.log @collection
          lastPuzzle = @collection.reject((puzzle) -> puzzle.get('solved')).pop()
          lastPuzzle?.open()
          return
      @
