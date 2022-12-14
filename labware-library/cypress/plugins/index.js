// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************
const webpackPreprocessor = require('@cypress/webpack-preprocessor')
const createWebpackConfig = require('../../webpack.config')

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)

module.exports = async (on, config) => {
  // `on` is used to hook into various events Cypress emits
  // `config` is the resolved Cypress config
  const webpackOptions = await createWebpackConfig()
  on('file:preprocessor', webpackPreprocessor({ webpackOptions }))
}
