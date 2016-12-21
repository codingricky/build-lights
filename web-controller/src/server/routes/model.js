'use strict'

const fs = require('fs')
const logger = require('winston')
const fetch = require('node-fetch')
const findIndex = require('lodash.findindex')
const fsOpts = { encoding: 'utf8' }

function restartLights () {
  const lights = fetch('http://localhost:9001/index.html?processname=light_controller&action=restart')
  const server = fetch('http://localhost:9001/index.html?processname=light_controller_server&action=restart')
  return Promise.all([server, lights])
}

module.exports = (router, configFile, lightConfigFile) => {
  router.get('/model', (req, res) => {
    const configuration = fs.readFileSync(configFile, fsOpts)
    res.json(JSON.parse(configuration))
  })

  router.put('/model', (req, res) => {
    const requestData = req.body || {}
    let model = JSON.parse(fs.readFileSync(configFile, fsOpts))

    if (requestData.tabChange && model.selectedTool !== requestData.tabChange) {
      logger.info('Updating active tab. Payload: "%j"', requestData)
      model.selectedTool = requestData.tabChange
    }

    if (requestData.autoDiscoverJobs) {
      const jobsIdx = findIndex(model.tools, { name: 'jobs to monitor' })
      const jobs = model.tools[jobsIdx].configuration.items

      fetch('http://localhost:8005/jobs').then((res) => {
        return res.json()
      }).then((discoveredJobNames) => {
        discoveredJobNames.forEach((discoveredJobName) => {
          if (!jobs.find((job) => { return job.name === discoveredJobName })) {
            jobs.push({name: discoveredJobName, active: false})
          }
        })
        res.json(model)
      })
      return
    }

    if (requestData.save) {
      logger.info('About to save a configuration. Payload: "%j"', requestData)
      const moduleService = require(`../services/${requestData.save}`)
      moduleService.persist(requestData.payload, lightConfigFile)
      moduleService.mutateModel(model, requestData.payload)
      model.lastUpdated = new Date().toJSON()
    }

    fs.writeFileSync(configFile, JSON.stringify(model, null, 2))
    logger.info('Committed configuration to file.')

    if (requestData.save) {
      if (process.env['DISABLE_RESTART_ON_SAVE'] === 'true') {
        model.result = { success: true, message: 'Configuration successfully persisted.' }
        res.json(model)
      } else {
        restartLights().then(() => {
          model.result = { success: true, message: 'Configuration successfully persisted.' }
          res.json(model)
        }).catch(err => {
          logger.error(err)
          model.result = { success: false, message: 'Configuration successfully persisted, but unable to restart lights.' }
          res.json(model)
        })
      }
    } else {
      res.json(model)
    }
  })
}
