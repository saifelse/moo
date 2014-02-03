define ['jade!templates/level-row'], (LevelRowTemplate) ->
  class LevelRowView extends Backbone.View
    tagName: 'tr'
    template: LevelRowTemplate

    initialize: ->
      @listenTo(@model, 'change', @render)

    updateSolveStatus: ->
      if @model.get('solved')
        @$el.addClass('solved')
        password = @model.get('password')
        @$('input[type="text"]')
          .prop('disabled', @model.get('solved'))
          .each (i) ->
            $(@).val(password[i])
     

    events: ->
      'keydown input[type="text"]': 'handleBack'
      'input input[type="text"]': 'moveToNext'
      'click input[type="text"]': 'selectInput'
      'submit form.submit-form': 'submitPassword'

    submitPassword: (e) ->
      password = $.makeArray(@$('input').map(-> $(@).val())).join('')
      @model
        .submitPassword(password)
        .fail((resp) =>
          alert(resp.responseJSON.message)
          @$('input').each(-> $(@).val(''))
          @$('input:first').focus()
        )

      return false

    selectInput: (e) ->
      $(e.target).select()
      return

    handleBack: (e) ->
      val = $(e.target).val()
      if e.which == 8
        if val.length == 0
          prevInput = $(e.target).prev()
          prevInput.focus()
          prevInput.select()     
          e.preventDefault()
      return

    moveToNext: (e) ->
      val = $(e.target).val()
      prevInput = $(e.target).prev()
      nextInput = $(e.target).next()
      if val.length
        if nextInput.is('[type="text"]')
          nextInput.focus()
          nextInput.select()
      else
        prevInput.focus()
        prevInput.select()
      return

    render: ->
      @$el.empty()

      levelNumber = @model.get('level')
      levelName = @model.get('name')
      levelAnswer = ('' for i in [0...@model.get('length')])
      metakey = @model.get('metakey')
      @$el.append(@template(levelNumber: levelNumber, name: levelName, answer: levelAnswer, metakey: metakey))
      @updateSolveStatus()
      @
