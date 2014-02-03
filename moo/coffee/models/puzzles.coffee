define [], () ->
  class PuzzleModel extends Backbone.Model
    defaults: ->
      name: null
      solve_url: null
      level: null
      solved: null
      length: null
      metakey: null
      password: null

    submitPassword: (password) ->
      $.ajax(
        type: 'POST'
        url: @get('solve_url')
        data: {'password': password.toUpperCase()}
        dataType: 'json'
      ).done((result) =>
        # Update the current puzle.
        if result.puzzle
          @set(@parse(result.puzzle))
        # Add the next puzzle.
        if result.next_puzzle
          nextPuzzle = new PuzzleModel()
          nextPuzzle.set(nextPuzzle.parse(result.next_puzzle))
          @collection.add(nextPuzzle)
        alert(result.responseJSON.message)
      )


  class PuzzleCollection extends Backbone.Collection
    url: '/api/puzzles'
    model: PuzzleModel

  {
    Collection: PuzzleCollection
    Model: PuzzleModel
  }
