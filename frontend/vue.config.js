module.exports = {
  publicPath: '/',
  configureWebpack: {
    devtool: 'source-map'
  },
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      const env = args[0]['process.env']
      args[0]['process.env'] = {
        ...env,
        VUE_APP_GOOGLE_MAPS_API_KEY: JSON.stringify(process.env.VUE_APP_GOOGLE_MAPS_API_KEY),
        VUE_APP_WEATHER_API_KEY: JSON.stringify(process.env.VUE_APP_WEATHER_API_KEY),
        VUE_APP_API_URL: JSON.stringify(process.env.VUE_APP_API_URL)
      }
      return args
    })
  }
} 