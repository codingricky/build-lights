import babel from 'rollup-plugin-babel'
import postcss from 'rollup-plugin-postcss'
import commonjs from 'rollup-plugin-commonjs'
import resolve from 'rollup-plugin-node-resolve'

// PostCSS plugins
import stylelint from 'stylelint'
import nested from 'postcss-nested'
import atImport from 'postcss-import'
import cssnext from 'postcss-cssnext'
import autoprefixer from 'autoprefixer'
import reporter from 'postcss-reporter'
import simplevars from 'postcss-simple-vars'

import stylelintConfiguration from 'stylelint-config-standard'

export default {
  entry: 'src/client/app.js',
  dest: 'src/server/public/js/bundle.js',
  format: 'iife',
  plugins: [
    postcss({
      plugins: [
        stylelint({
          config: stylelintConfiguration,
          configOverrides: { rules: { indentation: 4 } }
        }),
        atImport(),
        simplevars(),
        nested(),
        autoprefixer({ browsers: 'last 2 versions' }),
        cssnext({ warnForDuplicates: false }),
        reporter({ clearMessages: true })
      ],
      combineStyleTags: true
    }),
    resolve({
      main: true,
      jsnext: true,
      browser: true
    }),
    commonjs(),
    babel({
      babelrc: false,
      exclude: 'node_modules/**',
      plugins: [ 'inferno', 'syntax-jsx' ],
      presets: [ [ 'es2015', { modules: false } ] ]
    })
  ]
}
