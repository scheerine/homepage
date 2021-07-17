const { merge } = require('webpack-merge');
const config = require('./webpack.common.js');


const prodSassConfig = merge(config.sassConfig, {
    mode: 'production',
    devtool: 'source-map',
})


module.exports = [
    prodSassConfig,
]

