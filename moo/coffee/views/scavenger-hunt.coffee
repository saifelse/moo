define ['views/sky', 'models/puzzles'], (SkyView, puzzles) ->
  class ScavengerHuntView extends Backbone.View

    el: 'body'

    events:
      'change .chord input': 'handleChord'
      'click .js-red': 'handleRed'
      'click .js-blue': 'handleBlue'

    initialize: ->
      @puzzles = new puzzles.Collection()
      @skyView = new SkyView(el: @$('#sky'), collection: @puzzles)
      return

    handleChord: (e) ->
      console.log
      note = $(e.target).val()
      $(e.target).closest('.chord').find('.note').text(note)
      return

    handleRed: (e) ->
      e.preventDefault()
      alert('You chose correctly. The real origami rose had the URL to the scavenger hunt inside it. The password is HI. Onwards to Level 2!')
      return

    handleBlue: (e) ->
      e.preventDefault()
      alert('Try again!')
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
