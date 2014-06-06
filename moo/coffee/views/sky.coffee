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

      @collection.fetch()
        .done (e) =>
          lastPuzzle = @collection.reject((puzzle) -> puzzle.get('solved')).pop() || @collection.models[@collection.length - 1]
          lastPuzzle?.open()
          return
      @
