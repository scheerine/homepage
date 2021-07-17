const { merge } = require('webpack-merge');
const config = require('./webpack.common.js');


const devSassConfig = merge(config.sassConfig, {
    mode: 'development',
    devtool: 'inline-source-map',
})


module.exports = [
    devSassConfig,
]

