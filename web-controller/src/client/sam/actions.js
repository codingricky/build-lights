'use strict'

import findIndex from 'lodash.findindex'
import * as state from './state'

function setInProgressState () {
  let currentState = JSON.parse(window.localStorage.getItem('currentState'))
  currentState.saveInProgress = true
  window.localStorage.setItem('currentState', JSON.stringify(currentState))
  state.render(currentState)
}

function persistState (payload) {
  const requestOpts = {
    method: 'PUT',
    body: JSON.stringify(payload),
    headers: { 'Content-Type': 'application/json' }
  }

  fetch('/model', requestOpts)
    .then(res => res.json())
    .then(json => { state.render(state.represent(json)) })
    .catch(err => { state.render(state.represent(err)) })

  return false
}

export function selectCiTool (ciTool) {
  let currentState = JSON.parse(window.localStorage.getItem('currentState'))
  const toolIdx = findIndex(currentState, { name: 'ci server' })
  currentState[toolIdx].configuration.tool = ciTool
  window.localStorage.setItem('currentState', JSON.stringify(currentState))
  state.render(currentState)
}

export function reorderJob (a, b) {
  let currentState = JSON.parse(window.localStorage.getItem('currentState'))
  const toolIdx = findIndex(currentState, { name: 'jobs to monitor' })
  const jobs = currentState[toolIdx].configuration.items

  jobs[a.index] = { name: b.name, active: b.active }
  jobs[b.index] = { name: a.name, active: a.active }

  window.localStorage.setItem('currentState', JSON.stringify(currentState))
  state.render(currentState)
}

export function autoDiscoverJobs () {
  setInProgressState()
  return persistState({ autoDiscoverJobs: true })
}

export function switchToTab (tabName, present) {
  return persistState({ tabChange: tabName })
}

export function dismissAlert (model) {
  state.render(model)
  return false
}

export function reboot () {
  fetch('/reboot')
    .then(res => res.json())
    .then(json => { state.render(state.represent(json)) })
    .catch(err => { state.render(state.represent(err)) })

  return false
}

export function shutdown () {
  fetch('/shutdown')
    .then(res => res.json())
    .then(json => { state.render(state.represent(json)) })
    .catch(err => { state.render(state.represent(err)) })

  return false
}

export function upgrade () {
  setInProgressState()

  fetch('/upgrade')
    .then(res => res.json())
    .then(json => { state.render(state.represent(json)) })
    .catch(err => { state.render(state.represent(err)) })

  return false
}

export function completeDeviceAction (model) {
  if (model.reboot) {
    location.reload()
  } else {
    model.completed = true
    state.render(model)
  }
}

export function save (data, present) {
  setInProgressState()
  return persistState(data)
}
